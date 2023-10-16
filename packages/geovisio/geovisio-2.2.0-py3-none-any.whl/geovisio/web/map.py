# Some parts of code here are heavily inspired from Paul Ramsey's work
# See for reference : https://github.com/pramsey/minimal-mvt

import psycopg
import io
import typing
from flask import Blueprint, current_app, send_file
from geovisio.utils import auth
from geovisio import errors

bp = Blueprint("map", __name__, url_prefix="/api/map")


def isTileValid(z, x, y, format):
    """Check if tile parameters are valid

    Parameters
    ----------
    z : number
            Zoom level
    x : number
            X coordinate
    y : number
            Y coordinate
    format : string
            Tile format

    Returns
    -------
    boolean
            True if parameters are OK, raises InvalidAPIUsage exceptions otherwise
    """
    if z is None or x is None or y is None or format is None:
        raise errors.InvalidAPIUsage("One of required parameter is empty", status_code=404)
    if format not in ["pbf", "mvt"]:
        raise errors.InvalidAPIUsage("Tile format is invalid, should be either pbf or mvt", status_code=400)

    size = 2**z
    if x >= size or y >= size:
        raise errors.InvalidAPIUsage("X or Y parameter is out of bounds", status_code=404)
    if x < 0 or y < 0:
        raise errors.InvalidAPIUsage("X or Y parameter is out of bounds", status_code=404)
    if z < 0 or z > 14:
        raise errors.InvalidAPIUsage("Z parameter is out of bounds (should be 0-14)", status_code=404)

    return True


@bp.route("/<int:z>/<int:x>/<int:y>.<format>")
def getTile(z: int, x: int, y: int, format: str):
    """Get pictures and sequences as vector tiles

    Vector tiles contains possibly two layers : sequences and pictures.

    Layer "sequences":
      - Available on all zoom levels
      - Available properties (all levels)
        - id (sequence ID)
      - Other properties (available on zoom levels >= 13)
        - account_id
        - model (camera make and model)
        - type (flat or equirectangular)
        - date (capture date, as YYYY-MM-DD)

    Layer "pictures":
      - Available on zoom levels >= 13
      - Available properties:
        - id (picture ID)
        - account_id
        - ts (picture date/time)
        - heading (picture heading in degrees)
            - sequences (list of sequences ID this pictures belongs to)
        - type (flat or equirectangular)
        - model (camera make and model)
    ---
    tags:
        - Map
        - Pictures
        - Sequences
    parameters:
        - name: z
          in: path
          description: Zoom level (6 to 14)
          required: true
          schema:
            type: number
        - name: x
          in: path
          description: X coordinate
          required: true
          schema:
            type: number
        - name: y
          in: path
          description: Y coordinate
          required: true
          schema:
            type: number
        - name: format
          in: path
          description: Tile format (mvt, pbf)
          required: true
          schema:
            type: string
    responses:
        200:
            description: Sequences vector tile
            content:
                application/vnd.mapbox-vector-tile:
                    schema:
                        type: string
                        format: binary
    """

    if isTileValid(z, x, y, format):
        with psycopg.connect(current_app.config["DB_URL"], options="-c statement_timeout=10000") as conn:
            with conn.cursor() as cursor:
                query, params = _get_query(z, x, y)
                res = cursor.execute(query, params).fetchone()

                if not res:
                    raise errors.InternalError("Impossible to get tile")

                res = res[0]
                return send_file(io.BytesIO(res), mimetype="application/vnd.mapbox-vector-tile")


def _get_query(z: int, x: int, y: int) -> typing.Tuple[str, dict]:
    """Returns appropriate SQL query according to given zoom"""

    account = auth.get_current_account()
    accountId = account.id if account is not None else None

    params = {"x": x, "y": y, "z": z, "account": accountId}
    if z >= 13:
        query = """
SELECT mvtsequences.mvt || mvtpictures.mvt
FROM (
    SELECT ST_AsMVT(mvtgeomseqs.*, 'sequences') AS mvt
    FROM (
	SELECT
	    ST_AsMVTGeom(ST_Transform(geom, 3857), ST_TileEnvelope(%(z)s, %(x)s, %(y)s)) AS geom,
	    id, account_id,
	    NULLIF(status != 'ready', FALSE) AS hidden,
        computed_model AS model, computed_type AS type, computed_capture_date AS date
	FROM sequences
	WHERE
	    (status = 'ready' OR account_id = %(account)s)
	    AND geom && ST_Transform(ST_TileEnvelope(%(z)s, %(x)s, %(y)s), 4326)
    ) mvtgeomseqs
) mvtsequences,
(
    SELECT ST_AsMVT(mvtgeompics.*, 'pictures') AS mvt
    FROM (
	SELECT
	    ST_AsMVTGeom(ST_Transform(p.geom, 3857), ST_TileEnvelope(%(z)s, %(x)s, %(y)s)) AS geom,
	    p.id, p.ts, p.heading, p.account_id,
	    NULLIF(p.status != 'ready' OR s.status != 'ready', FALSE) AS hidden,
	    array_to_json(ARRAY_AGG(sp.seq_id)) AS sequences,
        p.metadata->>'type' AS type,
        TRIM(CONCAT(p.metadata->>'make', ' ', p.metadata->>'model')) AS model
	FROM pictures p
	LEFT JOIN sequences_pictures sp ON p.id = sp.pic_id
	LEFT JOIN sequences s ON s.id = sp.seq_id
	WHERE
	    (p.status = 'ready' OR p.account_id = %(account)s)
	    AND (s.status = 'ready' OR s.account_id = %(account)s)
	    AND p.geom && ST_Transform(ST_TileEnvelope(%(z)s, %(x)s, %(y)s), 4326)
	GROUP BY 1, 2, 3, 4, 5, 6
    ) mvtgeompics
) mvtpictures
"""

    elif z >= 7:
        query = """
SELECT ST_AsMVT(mvtsequences.*, 'sequences') AS mvt
FROM (
    SELECT
        ST_AsMVTGeom(ST_Transform(geom, 3857), ST_TileEnvelope(%(z)s, %(x)s, %(y)s)) AS geom,
        id, account_id,
        NULLIF(status != 'ready', FALSE) AS hidden,
        computed_model AS model, computed_type AS type, computed_capture_date AS date
    FROM sequences
    WHERE
        (status = 'ready' OR account_id = %(account)s)
        AND geom && ST_Transform(ST_TileEnvelope(%(z)s, %(x)s, %(y)s), 4326)
) mvtsequences
"""
    else:
        query = """
SELECT ST_AsMVT(mvtsequences.*, 'sequences') AS mvt
FROM (
    SELECT
        ST_AsMVTGeom(
            ST_Transform(geom, 3857),
            ST_TileEnvelope(%(z)s, %(x)s, %(y)s)
        ) AS geom,
        id,
        NULLIF(status != 'ready', FALSE) AS hidden
    FROM (
        SELECT ST_Simplify(geom, 0.01) AS geom, id, status
        FROM sequences
        WHERE
            (status = 'ready' OR account_id = %(account)s)
            AND geom && ST_Transform(ST_TileEnvelope(%(z)s, %(x)s, %(y)s), 4326)
    ) s
    WHERE geom IS NOT NULL
) mvtsequences
"""

    return query, params
