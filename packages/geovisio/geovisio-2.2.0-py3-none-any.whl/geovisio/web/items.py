import io
import json
import logging
import os
from typing import Optional
from urllib.parse import unquote
from PIL import Image
from psycopg.types.json import Jsonb
from werkzeug.datastructures import MultiDict
from uuid import UUID
from geovisio import errors, utils
from geovisio.utils import auth
from geovisio.web.params import (
    as_latitude,
    as_longitude,
    as_uuid,
    parse_datetime,
    parse_datetime_interval,
    parse_bbox,
    parse_list,
)

import psycopg
from psycopg.rows import dict_row
from psycopg.sql import SQL
from geovisio.web.utils import (
    accountIdOrDefault,
    cleanNoneInList,
    dbTsToStac,
    get_license_link,
    get_root_link,
    removeNoneInDict,
    STAC_VERSION,
)
from flask import current_app, request, url_for, Blueprint
from geopic_tag_reader.writer import writePictureMetadata, PictureMetadata

from geovisio.workers import runner_pictures

bp = Blueprint("stac_items", __name__, url_prefix="/api")


def dbPictureToStacItem(seqId, dbPic):
    """Transforms a picture extracted from database into a STAC Item

    Parameters
    ----------
    seqId : uuid
        Associated sequence ID
    dbSeq : dict
        A row from pictures table in database (with id, geojson, ts, heading, cols, rows, width, height, prevpic, nextpic, prevpicgeojson, nextpicgeojson fields)

    Returns
    -------
    object
        The equivalent in STAC Item format
    """

    item = removeNoneInDict(
        {
            "type": "Feature",
            "stac_version": STAC_VERSION,
            "stac_extensions": [
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",  # "view:" fields
                "https://stac-extensions.github.io/perspective-imagery/v1.0.0/schema.json",  # "pers:" fields
            ],
            "id": str(dbPic["id"]),
            "geometry": dbPic["geojson"],
            "bbox": dbPic["geojson"]["coordinates"] + dbPic["geojson"]["coordinates"],
            "providers": [
                {"name": dbPic["account_name"], "roles": ["producer"]},
            ],
            "properties": {
                "datetime": dbTsToStac(dbPic["ts"]),
                "created": dbTsToStac(dbPic["processed_at"]),
                # TODO : add "updated" TS for last edit time of metadata
                "license": current_app.config["API_PICTURES_LICENSE_SPDX_ID"],
                "view:azimuth": dbPic["heading"],
                "pers:interior_orientation": removeNoneInDict(
                    {
                        "camera_manufacturer": dbPic["metadata"].get("make"),
                        "camera_model": dbPic["metadata"].get("model"),
                        "focal_length": dbPic["metadata"].get("focal_length"),
                        "field_of_view": dbPic["metadata"].get("field_of_view"),
                    }
                )
                if "metadata" in dbPic
                and len([True for f in dbPic["metadata"] if f in ["make", "model", "focal_length", "field_of_view"]]) > 0
                else {},
                "geovisio:status": dbPic.get("status"),
                "geovisio:producer": dbPic["account_name"],
                "geovisio:image": _getHDJpgPictureURL(dbPic["id"], dbPic.get("status")),
                "geovisio:thumbnail": _getThumbJpgPictureURL(dbPic["id"], dbPic.get("status")),
            },
            "links": cleanNoneInList(
                [
                    get_root_link(),
                    {
                        "rel": "parent",
                        "type": "application/json",
                        "href": url_for("stac_collections.getCollection", _external=True, collectionId=seqId),
                    },
                    {
                        "rel": "self",
                        "type": "application/geo+json",
                        "href": url_for("stac_items.getCollectionItem", _external=True, collectionId=seqId, itemId=dbPic["id"]),
                    },
                    {
                        "rel": "collection",
                        "type": "application/json",
                        "href": url_for("stac_collections.getCollection", _external=True, collectionId=seqId),
                    },
                    get_license_link(),
                ]
            ),
            "assets": {
                "hd": {
                    "title": "HD picture",
                    "description": "Highest resolution available of this picture",
                    "roles": ["data"],
                    "type": "image/jpeg",
                    "href": _getHDJpgPictureURL(dbPic["id"], status=dbPic.get("status")),
                },
                "sd": {
                    "title": "SD picture",
                    "description": "Picture in standard definition (fixed width of 2048px)",
                    "roles": ["visual"],
                    "type": "image/jpeg",
                    "href": _getSDJpgPictureURL(dbPic["id"], status=dbPic.get("status")),
                },
                "thumb": {
                    "title": "Thumbnail",
                    "description": "Picture in low definition (fixed width of 500px)",
                    "roles": ["thumbnail"],
                    "type": "image/jpeg",
                    "href": _getThumbJpgPictureURL(dbPic["id"], status=dbPic.get("status")),
                },
            },
            "collection": str(seqId),
        }
    )

    # Next / previous links if any
    if "nextpic" in dbPic and dbPic["nextpic"] is not None:
        item["links"].append(
            {
                "rel": "next",
                "type": "application/geo+json",
                "geometry": dbPic["nextpicgeojson"],
                "id": dbPic["nextpic"],
                "href": url_for("stac_items.getCollectionItem", _external=True, collectionId=seqId, itemId=dbPic["nextpic"]),
            }
        )

    if "prevpic" in dbPic and dbPic["prevpic"] is not None:
        item["links"].append(
            {
                "rel": "prev",
                "type": "application/geo+json",
                "geometry": dbPic["prevpicgeojson"],
                "id": dbPic["prevpic"],
                "href": url_for("stac_items.getCollectionItem", _external=True, collectionId=seqId, itemId=dbPic["prevpic"]),
            }
        )

    #
    # Picture type-specific properties
    #

    # Equirectangular
    if dbPic["metadata"]["type"] == "equirectangular":
        item["stac_extensions"].append("https://stac-extensions.github.io/tiled-assets/v1.0.0/schema.json")  # "tiles:" fields

        item["properties"]["tiles:tile_matrix_sets"] = {
            "geovisio": {
                "type": "TileMatrixSetType",
                "title": "GeoVisio tile matrix for picture " + str(dbPic["id"]),
                "identifier": "geovisio-" + str(dbPic["id"]),
                "tileMatrix": [
                    {
                        "type": "TileMatrixType",
                        "identifier": "0",
                        "scaleDenominator": 1,
                        "topLeftCorner": [0, 0],
                        "tileWidth": dbPic["metadata"]["width"] / dbPic["metadata"]["cols"],
                        "tileHeight": dbPic["metadata"]["height"] / dbPic["metadata"]["rows"],
                        "matrixWidth": dbPic["metadata"]["cols"],
                        "matrixHeight": dbPic["metadata"]["rows"],
                    }
                ],
            }
        }

        item["asset_templates"] = {
            "tiles": {
                "title": "HD tiled picture",
                "description": "Highest resolution available of this picture, as tiles",
                "roles": ["data"],
                "type": "image/jpeg",
                "href": _getTilesJpgPictureURL(dbPic["id"], status=dbPic.get("status")),
            }
        }

    return item


def get_first_rank_of_page(rankToHave: int, limit: Optional[int]) -> int:
    """if there is a limit, we try to emulate a page, so we'll return the nth page that should contain this picture
    Note: the ranks starts from 1
    >>> get_first_rank_of_page(3, 2)
    3
    >>> get_first_rank_of_page(4, 2)
    3
    >>> get_first_rank_of_page(3, None)
    3
    >>> get_first_rank_of_page(123, 10)
    121
    >>> get_first_rank_of_page(10, 10)
    1
    >>> get_first_rank_of_page(10, 100)
    1
    """
    if not limit:
        return rankToHave

    return int((rankToHave - 1) / limit) * limit + 1


@bp.route("/collections/<uuid:collectionId>/items", methods=["GET"])
def getCollectionItems(collectionId):
    """List items of a single collection
    ---
    tags:
        - Sequences
    parameters:
        - name: collectionId
          in: path
          description: ID of collection to retrieve
          required: true
          schema:
            type: string
        - name: limit
          in: query
          description: Number of items that should be present in response. Unlimited by default.
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 10000
        - name: startAfterRank
          in: query
          description: Position of last received picture in sequence. Response will start with the following picture.
          required: false
          schema:
            type: integer
            minimum: 1
        - name: withPicture
          in: query
          description: Used in the pagination context, if present, the api will return the given picture in the results.
            Can be used in the same time as the `limit` parameter, but not with the `startAfterRank` parameter.
          required: false
          schema:
            type: string
            format: uuid
    responses:
        200:
            description: the items list
            content:
                application/geo+json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollectionItems'
    """

    account = auth.get_current_account()

    params = {
        "seq": collectionId,
        # Only the owner of an account can view pictures not 'ready'
        "account": account.id if account is not None else None,
    }

    args = request.args
    limit = args.get("limit")
    startAfterRank = args.get("startAfterRank")
    withPicture = args.get("withPicture")

    filters = [
        SQL("sp.seq_id = %(seq)s"),
        SQL("(p.status = 'ready' OR p.account_id = %(account)s)"),
        SQL("(s.status = 'ready' OR s.account_id = %(account)s)"),
    ]

    # Check if limit is valid
    sql_limit = SQL("")
    if limit is not None:
        try:
            limit = int(limit)
            if limit < 1 or limit > 10000:
                raise errors.InvalidAPIUsage("limit parameter should be an integer between 1 and 10000", status_code=400)
        except ValueError:
            raise errors.InvalidAPIUsage("limit parameter should be a valid, positive integer (between 1 and 10000)", status_code=400)
        sql_limit = SQL("LIMIT %(limit)s")
        params["limit"] = limit

    if withPicture and startAfterRank:
        raise errors.InvalidAPIUsage(f"`startAfterRank` and `withPicture` are mutually exclusive parameters")

    # Check if rank is valid
    if startAfterRank is not None:
        try:
            startAfterRank = int(startAfterRank)
            if startAfterRank < 1:
                raise errors.InvalidAPIUsage("startAfterRank parameter should be a positive integer (starting from 1)", status_code=400)
        except ValueError:
            raise errors.InvalidAPIUsage("startAfterRank parameter should be a valid, positive integer", status_code=400)

        filters.append(SQL("rank > %(start_after_rank)s"))
        params["start_after_rank"] = startAfterRank

    paginated = startAfterRank is not None or limit is not None or withPicture is not None

    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            # check on sequence
            seqMeta = cursor.execute(
                "SELECT s.id "
                + (", MAX(sp.rank) AS max_rank, MIN(sp.rank) AS min_rank " if paginated else "")
                + "FROM sequences s "
                + ("LEFT JOIN sequences_pictures sp ON sp.seq_id = s.id " if paginated else "")
                + "WHERE s.id = %(seq)s AND (s.status = 'ready' OR s.account_id = %(account)s) "
                + ("GROUP BY s.id" if paginated else ""),
                params,
            ).fetchone()

            if seqMeta is None:
                raise errors.InvalidAPIUsage("Collection doesn't exist", status_code=404)

            maxRank = seqMeta.get("max_rank")

            if startAfterRank is not None and startAfterRank >= maxRank:
                raise errors.InvalidAPIUsage(f"No more items in this collection (last available rank is {maxRank})", status_code=404)

            if withPicture is not None:
                withPicture = as_uuid(withPicture, "withPicture should be a valid UUID")
                pic = cursor.execute(
                    "SELECT rank FROM pictures p JOIN sequences_pictures sp ON sp.pic_id = p.id WHERE p.id = %(id)s AND sp.seq_id = %(seq)s",
                    params={"id": withPicture, "seq": collectionId},
                ).fetchone()
                if not pic:
                    raise errors.InvalidAPIUsage(f"Picture with id {withPicture} does not exists")
                rank = get_first_rank_of_page(pic["rank"], limit)

                filters.append(SQL("rank >= %(start_after_rank)s"))
                params["start_after_rank"] = rank

            query = SQL(
                """
				SELECT
					p.id, p.ts, p.heading, p.metadata, p.processed_at, p.status,
					ST_AsGeoJSON(p.geom)::json AS geojson,
					a.name AS account_name,
                    sp.rank,
					CASE WHEN LAG(p.status) OVER othpics = 'ready' THEN LAG(p.id) OVER othpics END AS prevpic,
					CASE WHEN LAG(p.status) OVER othpics = 'ready' THEN ST_AsGeoJSON(LAG(p.geom) OVER othpics)::json END AS prevpicgeojson,
					CASE WHEN LEAD(p.status) OVER othpics = 'ready' THEN LEAD(p.id) OVER othpics END AS nextpic,
					CASE WHEN LEAD(p.status) OVER othpics = 'ready' THEN ST_AsGeoJSON(LEAD(p.geom) OVER othpics)::json END AS nextpicgeojson
				FROM sequences_pictures sp
				JOIN pictures p ON sp.pic_id = p.id
				JOIN accounts a ON a.id = p.account_id
				JOIN sequences s ON s.id = sp.seq_id
				WHERE
    				{filter}
				WINDOW othpics AS (PARTITION BY sp.seq_id ORDER BY sp.rank)
				ORDER BY rank
                {limit}
                """
            ).format(filter=SQL(" AND ").join(filters), limit=sql_limit)

            records = cursor.execute(query, params)

            min_query_rank, max_query_rank = None, None
            items = []
            for dbPic in records:
                if not min_query_rank:
                    min_query_rank = dbPic["rank"]
                max_query_rank = dbPic["rank"]
                items.append(dbPictureToStacItem(collectionId, dbPic))

            links = [
                get_root_link(),
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": url_for("stac_collections.getCollection", _external=True, collectionId=collectionId),
                },
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": url_for(
                        "stac_items.getCollectionItems",
                        _external=True,
                        collectionId=collectionId,
                        limit=limit,
                        startAfterRank=startAfterRank,
                    ),
                },
            ]

            if paginated and items:
                links.append(
                    {
                        "rel": "first",
                        "type": "application/geo+json",
                        "href": url_for("stac_items.getCollectionItems", _external=True, collectionId=collectionId, limit=limit),
                    }
                )
                if min_query_rank:
                    has_item_before = min_query_rank > seqMeta["min_rank"]
                    if has_item_before:
                        # Previous page link
                        #   - If limit is set, rank is current - limit -1
                        #   - If no limit is set, rank is 0 (none)
                        prevRank = min_query_rank - limit - 1 if limit is not None else 0
                        if prevRank < 1:
                            prevRank = None
                        links.append(
                            {
                                "rel": "prev",
                                "type": "application/geo+json",
                                "href": url_for(
                                    "stac_items.getCollectionItems",
                                    _external=True,
                                    collectionId=collectionId,
                                    limit=limit,
                                    startAfterRank=prevRank,
                                ),
                            }
                        )

                has_item_after = max_query_rank < seqMeta["max_rank"]
                if has_item_after:
                    links.append(
                        {
                            "rel": "next",
                            "type": "application/geo+json",
                            "href": url_for(
                                "stac_items.getCollectionItems",
                                _external=True,
                                collectionId=collectionId,
                                limit=limit,
                                startAfterRank=max_query_rank,
                            ),
                        }
                    )

                # Last page link
                #   - If this page is the last one, rank equals to rank given by user
                #   - Otherwise, rank equals max rank - limit

                lastPageRank = startAfterRank
                if limit is not None:
                    if seqMeta["max_rank"] > max_query_rank:
                        lastPageRank = seqMeta["max_rank"] - limit
                        if lastPageRank < max_query_rank:
                            lastPageRank = max_query_rank

                links.append(
                    {
                        "rel": "last",
                        "type": "application/geo+json",
                        "href": url_for(
                            "stac_items.getCollectionItems",
                            _external=True,
                            collectionId=collectionId,
                            limit=limit,
                            startAfterRank=lastPageRank,
                        ),
                    }
                )

            return (
                {
                    "type": "FeatureCollection",
                    "features": items,
                    "links": links,
                },
                200,
                {"Content-Type": "application/geo+json"},
            )


def _getPictureItemById(collectionId, itemId):
    """Get a picture metadata by its ID and collection ID

    ---
    tags:
        - Pictures
    parameters:
        - name: collectionId
          in: path
          description: ID of collection to retrieve
          required: true
          schema:
            type: string
        - name: itemId
          in: path
          description: ID of item to retrieve
          required: true
          schema:
            type: string
    """
    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            # Check if there is a logged user
            account = auth.get_current_account()
            accountId = account.id if account else None

            # Get rank + position of wanted picture
            record = cursor.execute(
                """
				SELECT
    				p.id, sp.rank, ST_AsGeoJSON(p.geom)::json AS geojson, p.heading, p.ts, p.metadata, p.processed_at, p.status, accounts.name AS account_name,
					spl.prevpic, spl.prevpicgeojson, spl.nextpic, spl.nextpicgeojson
				FROM pictures p
				JOIN sequences_pictures sp ON sp.pic_id = p.id
				JOIN accounts ON p.account_id = accounts.id
				JOIN sequences s ON sp.seq_id = s.id
				LEFT JOIN (
					SELECT
						p.id,
						LAG(p.id) OVER othpics AS prevpic,
						ST_AsGeoJSON(LAG(p.geom) OVER othpics)::json AS prevpicgeojson,
						LEAD(p.id) OVER othpics AS nextpic,
						ST_AsGeoJSON(LEAD(p.geom) OVER othpics)::json AS nextpicgeojson
					FROM pictures p
					JOIN sequences_pictures sp ON p.id = sp.pic_id
					WHERE
						sp.seq_id = %(seq)s
						AND (p.account_id = %(acc)s OR p.status != 'hidden')
					WINDOW othpics AS (PARTITION BY sp.seq_id ORDER BY sp.rank)
				) spl ON p.id = spl.id
				WHERE sp.seq_id = %(seq)s
					AND p.id = %(pic)s
					AND (p.account_id = %(acc)s OR p.status != 'hidden')
					AND (s.account_id = %(acc)s OR s.status != 'hidden')
				""",
                {"seq": collectionId, "pic": itemId, "acc": accountId},
            ).fetchone()

            if record is None:
                return None

            return dbPictureToStacItem(collectionId, record)


@bp.route("/collections/<uuid:collectionId>/items/<uuid:itemId>")
def getCollectionItem(collectionId, itemId):
    """Get a single item from a collection
    ---
    tags:
        - Pictures
    parameters:
        - name: collectionId
          in: path
          description: ID of collection to retrieve
          required: true
          schema:
            type: string
        - name: itemId
          in: path
          description: ID of item to retrieve
          required: true
          schema:
            type: string
    responses:
        102:
            description: the item (which is still under process)
            content:
                application/geo+json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioItem'
        200:
            description: the wanted item
            content:
                application/geo+json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioItem'
    """

    stacItem = _getPictureItemById(collectionId, itemId)
    if stacItem is None:
        raise errors.InvalidAPIUsage("Item doesn't exist", status_code=404)

    account = auth.get_current_account()
    picStatusToHttpCode = {
        "preparing": 102,
        "preparing-derivates": 102,
        "preparing-blur": 102,
        "waiting-for-process": 102,
        "ready": 200,
        "hidden": 200 if account else 404,
        "broken": 500,
    }
    return stacItem, picStatusToHttpCode[stacItem["properties"]["geovisio:status"]], {"Content-Type": "application/geo+json"}


@bp.route("/search", methods=["GET", "POST"])
def searchItems():
    """Search through all available items
    ---
    tags:
        - Pictures
    get:
        parameters:
            - $ref: '#/components/parameters/STAC_bbox'
            - $ref: '#/components/parameters/STAC_intersects'
            - $ref: '#/components/parameters/STAC_datetime'
            - $ref: '#/components/parameters/STAC_limit'
            - $ref: '#/components/parameters/STAC_ids'
            - $ref: '#/components/parameters/STAC_collectionsArray'
    post:
        requestBody:
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/STACItemSearchBody'
    responses:
        200:
            $ref: '#/components/responses/STAC_search'
    """

    account = auth.get_current_account()
    accountId = account.id if account is not None else None
    sqlWhere = ["(p.status = 'ready' OR p.account_id = %(account)s)", "(s.status = 'ready' OR s.account_id = %(account)s)"]
    sqlParams = {"account": accountId}
    sqlSubQueryWhere = ["(p.status = 'ready'OR p.account_id = %(account)s)"]

    #
    # Parameters parsing and verification
    #

    # Method + content-type
    args = None
    if request.method == "GET":
        args = request.args
    elif request.method == "POST":
        if request.headers.get("Content-Type") == "application/json":
            args = MultiDict(request.json)
        else:
            raise errors.InvalidAPIUsage("Search using POST method should have a JSON body", status_code=400)

    # Limit
    if args.get("limit") is not None:
        limit = args.get("limit", type=int)
        if limit is None or limit < 1 or limit > 10000:
            raise errors.InvalidAPIUsage("Parameter limit must be either empty or a number between 1 and 10000", status_code=400)
        else:
            sqlParams["limit"] = limit
    else:
        sqlParams["limit"] = 10000

    # Bounding box
    bboxarg = parse_bbox(args.getlist("bbox"))
    if bboxarg is not None:
        sqlWhere.append("p.geom && ST_MakeEnvelope(%(minx)s, %(miny)s, %(maxx)s, %(maxy)s, 4326)")
        sqlParams["minx"] = bboxarg[0]
        sqlParams["miny"] = bboxarg[1]
        sqlParams["maxx"] = bboxarg[2]
        sqlParams["maxy"] = bboxarg[3]

    # Datetime
    min_dt, max_dt = parse_datetime_interval(args.get("datetime"))
    if min_dt is not None:
        sqlWhere.append("p.ts >= %(mints)s::timestamp with time zone")
        sqlParams["mints"] = min_dt

    if max_dt is not None:
        sqlWhere.append("p.ts <= %(maxts)s::timestamp with time zone")
        sqlParams["maxts"] = max_dt

    # Intersects
    if args.get("intersects") is not None:
        try:
            intersects = json.loads(args.get("intersects"))
            if intersects["type"] == "Point":
                sqlWhere.append("ST_DWithin(p.geom::geography, ST_GeomFromGeoJSON(%(geom)s)::geography, 0.01)")
            else:
                sqlWhere.append("p.geom && ST_GeomFromGeoJSON(%(geom)s)")
                sqlWhere.append("ST_Intersects(p.geom, ST_GeomFromGeoJSON(%(geom)s))")
            sqlParams["geom"] = Jsonb(intersects)
        except:
            raise errors.InvalidAPIUsage("Parameter intersects should contain a valid GeoJSON Geometry (not a Feature)", status_code=400)

    # Ids
    if args.get("ids") is not None:
        sqlWhere.append("p.id = ANY(%(ids)s)")
        try:
            sqlParams["ids"] = [UUID(j) for j in parse_list(args.get("ids"), "ids")]
        except:
            raise errors.InvalidAPIUsage("Parameter ids should be a JSON array of strings", status_code=400)

    # Collections
    if args.get("collections") is not None:
        sqlWhere.append("sp.seq_id = ANY(%(collections)s)")

        # custom subquery filtering to help PG query plan
        sqlSubQueryWhere.append("sp.seq_id = ANY(%(collections)s)")

        try:
            sqlParams["collections"] = [UUID(j) for j in parse_list(args["collections"], "collections")]
        except:
            raise errors.InvalidAPIUsage("Parameter collections should be a JSON array of strings", status_code=400)

    # To speed up search, if it's a search by id and on only one id, we use the same code as /collections/:cid/items/:id
    if args.get("ids") is not None and args:
        ids = parse_list(args.get("ids"), "ids")
        if len(ids) == 1:
            picture_id = ids[0]

            with psycopg.connect(current_app.config["DB_URL"]) as conn, conn.cursor() as cursor:
                seq = cursor.execute("SELECT seq_id FROM sequences_pictures WHERE pic_id = %s", [picture_id]).fetchone()
                if not seq:
                    raise errors.InvalidAPIUsage("Picture doesn't exist", status_code=404)

                item = _getPictureItemById(seq[0], UUID(picture_id))
                features = [item] if item else []
                return (
                    {"type": "FeatureCollection", "features": features, "links": [get_root_link()]},
                    200,
                    {"Content-Type": "application/geo+json"},
                )

    #
    # Database query
    #

    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row, options="-c statement_timeout=30000") as conn:
        with conn.cursor() as cursor:
            query = (
                """
				SELECT
					p.id, p.ts, p.heading, p.metadata, p.processed_at,
					ST_AsGeoJSON(p.geom)::json AS geojson,
					sp.seq_id,
					spl.prevpic, spl.prevpicgeojson, spl.nextpic, spl.nextpicgeojson,
					accounts.name AS account_name
				FROM pictures p
				LEFT JOIN sequences_pictures sp ON p.id = sp.pic_id
				LEFT JOIN sequences s ON s.id = sp.seq_id
				LEFT JOIN accounts ON p.account_id = accounts.id
				LEFT JOIN (
					SELECT
						p.id,
						LAG(p.id) OVER othpics AS prevpic,
						ST_AsGeoJSON(LAG(p.geom) OVER othpics)::json AS prevpicgeojson,
						LEAD(p.id) OVER othpics AS nextpic,
						ST_AsGeoJSON(LEAD(p.geom) OVER othpics)::json AS nextpicgeojson
					FROM pictures p
					JOIN sequences_pictures sp ON p.id = sp.pic_id
					WHERE
					"""
                + " AND ".join(sqlSubQueryWhere)
                + """
					WINDOW othpics AS (PARTITION BY sp.seq_id ORDER BY sp.rank)
				) spl ON p.id = spl.id
				WHERE
				"""
                + " AND ".join(sqlWhere)
                + """
				LIMIT %(limit)s
			"""
            )
            records = cursor.execute(query, sqlParams)

            items = [dbPictureToStacItem(str(dbPic["seq_id"]), dbPic) for dbPic in records]

            return (
                {
                    "type": "FeatureCollection",
                    "features": items,
                    "links": [
                        get_root_link(),
                    ],
                },
                200,
                {"Content-Type": "application/geo+json"},
            )


@bp.route("/collections/<uuid:collectionId>/items", methods=["POST"])
@auth.login_required_by_setting("API_FORCE_AUTH_ON_UPLOAD")
def postCollectionItem(collectionId, account=None):
    """Add a new picture in a given sequence
    ---
    tags:
        - Upload
    parameters:
        - name: collectionId
          in: path
          description: ID of sequence to add this picture into
          required: true
          schema:
            type: string
    requestBody:
        content:
            multipart/form-data:
                schema:
                    $ref: '#/components/schemas/GeoVisioPostItem'
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        202:
            description: the added picture metadata
            content:
                application/geo+json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioItem'
    """

    if not request.headers.get("Content-Type", "").startswith("multipart/form-data"):
        raise errors.InvalidAPIUsage("Content type should be multipart/form-data", status_code=415)

    # Check if position was given
    if request.form.get("position") is None:
        raise errors.InvalidAPIUsage('Missing "position" parameter', status_code=400)
    else:
        try:
            position = int(request.form.get("position"))
            if position <= 0:
                raise ValueError()
        except ValueError:
            raise errors.InvalidAPIUsage("Position in sequence should be a positive integer", status_code=400)

    # Check if datetime was given
    ext_mtd = PictureMetadata()
    if request.form.get("override_capture_time") is not None:
        ext_mtd.capture_time = parse_datetime(
            request.form.get("override_capture_time"),
            error="Parameter `override_capture_time` is not a valid datetime, it should be an iso formated datetime (like '2017-07-21T17:32:28Z').",
        )

    lon, lat = request.form.get("override_longitude"), request.form.get("override_latitude")
    if lon is not None or lat is not None:
        if lat is None:
            raise errors.InvalidAPIUsage("Longitude cannot be overridden alone, override_latitude also needs to be set")
        if lon is None:
            raise errors.InvalidAPIUsage("Latitude cannot be overridden alone, override_longitude also needs to be set")
        lon = as_longitude(lon, error=f"For parameter `override_longitude`, `{lon}` is not a valid longitude")
        lat = as_latitude(lat, error=f"For parameter `override_latitude`, `{lat}` is not a valid latitude")
        ext_mtd.longitude = lon
        ext_mtd.latitude = lat

    # Check if picture blurring status is valid
    if request.form.get("isBlurred") is None or request.form.get("isBlurred") in ["true", "false"]:
        isBlurred = request.form.get("isBlurred") == "true"
    else:
        raise errors.InvalidAPIUsage("Picture blur status should be either unset, true or false", status_code=400)

    # Check if a picture file was given
    if "picture" not in request.files:
        raise errors.InvalidAPIUsage("No picture file was sent", status_code=400)
    else:
        picture = request.files["picture"]

        # Check file validity
        if not (picture.filename != "" and "." in picture.filename and picture.filename.rsplit(".", 1)[1].lower() in ["jpg", "jpeg"]):
            raise errors.InvalidAPIUsage("Picture file is either missing or in an unsupported format (should be jpg)", status_code=400)

    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            # Check if sequence exists
            seq = cursor.execute("SELECT id FROM sequences WHERE id = %s", [collectionId]).fetchone()
            if not seq or len(seq) != 1:
                raise errors.InvalidAPIUsage(f"Sequence {collectionId} wasn't found in database", status_code=404)

            # Compute various metadata
            accountId = accountIdOrDefault(account)
            raw_pic = picture.read()
            filesize = len(raw_pic)

            additionalMetadata = {
                "blurredByAuthor": isBlurred,
                "originalFileName": os.path.basename(picture.filename),
                "originalFileSize": filesize,
            }

            # Update picture metadata if needed
            updated_picture = io.BytesIO(writePictureMetadata(raw_pic, ext_mtd))
            pillowPicture = Image.open(updated_picture)

            # Insert picture into database
            try:
                picId = utils.pictures.insertNewPictureInDatabase(
                    conn, collectionId, position, pillowPicture, accountId, additionalMetadata
                )
            except utils.pictures.PicturePositionConflict:
                raise errors.InvalidAPIUsage("Picture at given position already exist", status_code=409)
            except utils.pictures.MetadataReadingError as e:
                raise errors.InvalidAPIUsage("Impossible to parse picture metadata", payload={"details": {"error": e.details}})

            # Save file into appropriate filesystem
            try:
                updated_picture.seek(0)  # Allows re-reading picture
                utils.pictures.saveRawPicture(picId, updated_picture, isBlurred)
            except:
                logging.exception("Picture wasn't correctly saved in filesystem")
                raise errors.InvalidAPIUsage("Picture wasn't correctly saved in filesystem", status_code=500)

            conn.commit()

            runner_pictures.background_processor.process_pictures()

            # Return picture metadata
            return (
                getCollectionItem(collectionId, picId)[0],
                202,
                {
                    "Content-Type": "application/json",
                    "Access-Control-Expose-Headers": "Location",  # Needed for allowing web browsers access Location header
                    "Location": url_for("stac_items.getCollectionItem", _external=True, collectionId=collectionId, itemId=picId),
                },
            )


@bp.route("/collections/<uuid:collectionId>/items/<uuid:itemId>", methods=["PATCH"])
@auth.login_required()
def patchCollectionItem(collectionId, itemId, account):
    """Edits properties of an existing picture
    ---
    tags:
        - Editing
    parameters:
        - name: collectionId
          in: path
          description: ID of sequence the picture belongs to
          required: true
          schema:
            type: string
        - name: itemId
          in: path
          description: ID of picture to edit
          required: true
          schema:
            type: string
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/GeoVisioPatchItem'
            application/x-www-form-urlencoded:
                schema:
                    $ref: '#/components/schemas/GeoVisioPatchItem'
            multipart/form-data:
                schema:
                    $ref: '#/components/schemas/GeoVisioPatchItem'
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        200:
            description: the wanted item
            content:
                application/geo+json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioItem'
    """

    # Parse received parameters
    metadata = {}
    content_type = (request.headers.get("Content-Type") or "").split(";")[0]
    if content_type == "application/json":
        metadata["visible"] = request.json.get("visible")
    elif content_type in ["multipart/form-data", "application/x-www-form-urlencoded"]:
        metadata["visible"] = request.form.get("visible")

    # Check if visibility param is valid
    if metadata.get("visible") is None:
        # /!\ As visible is the only editable thing for now, we can return if it's null
        # The line below may be removed when other parameters will be available for patching
        # Otherwise, you might want to do: visible = None
        return getCollectionItem(collectionId, itemId)

    elif metadata.get("visible") in ["true", "false"]:
        visible = metadata.get("visible") == "true"
    else:
        raise errors.InvalidAPIUsage("Picture visibility parameter (visible) should be either unset, true or false", status_code=400)

    # Check if picture exists and if given account is authorized to edit
    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            pic = cursor.execute("SELECT status, account_id FROM pictures WHERE id = %s", [itemId]).fetchone()

            # Picture not found
            if not pic:
                raise errors.InvalidAPIUsage(f"Picture {itemId} wasn't found in database", status_code=404)

            # Account associated to picture doesn't match current user
            if account is not None and account.id != str(pic[1]):
                raise errors.InvalidAPIUsage("You're not authorized to edit this picture", status_code=403)

            # Let's edit this picture
            oldStatus = pic[0]
            newStatus = None

            if visible is not None:
                if visible is True and oldStatus == "hidden":
                    newStatus = "ready"
                elif visible is False and oldStatus == "ready":
                    newStatus = "hidden"
                elif (visible is True and oldStatus == "ready") or (visible is False and oldStatus == "hidden"):
                    newStatus = oldStatus

                    # /!\ As visible is the only editable thing for now, we can return if it's unchanged
                    # The line below may be removed when other parameters will be available for patching
                    return getCollectionItem(collectionId, itemId)

                else:
                    # Picture is in a preparing/broken/... state so no edit possible
                    raise errors.InvalidAPIUsage(
                        f"Picture {itemId} is in {oldStatus} state, its visibility can't be changed for now", status_code=400
                    )

            if newStatus:
                cursor.execute("UPDATE pictures SET status = %s WHERE id = %s", [newStatus, itemId])
                conn.commit()

            # Redirect response to a classic GET
            return getCollectionItem(collectionId, itemId)


@bp.route("/collections/<uuid:collectionId>/items/<uuid:itemId>", methods=["DELETE"])
@auth.login_required()
def deleteCollectionItem(collectionId, itemId, account):
    """Delete an existing picture
    ---
    tags:
        - Editing
    parameters:
        - name: collectionId
          in: path
          description: ID of sequence the picture belongs to
          required: true
          schema:
            type: string
        - name: itemId
          in: path
          description: ID of picture to edit
          required: true
          schema:
            type: string
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        204:
            description: The object has been correctly deleted
    """

    # Check if picture exists and if given account is authorized to edit
    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            pic = cursor.execute("SELECT status, account_id FROM pictures WHERE id = %s", [itemId]).fetchone()

            # Picture not found
            if not pic:
                raise errors.InvalidAPIUsage(f"Picture {itemId} wasn't found in database", status_code=404)

            # Account associated to picture doesn't match current user
            if account is not None and account.id != str(pic[1]):
                raise errors.InvalidAPIUsage("You're not authorized to edit this picture", status_code=403)

            cursor.execute("DELETE FROM pictures WHERE id = %s", [itemId])

            # delete images
            utils.pictures.removeAllFiles(itemId)

            conn.commit()

            return "", 204


def _getHDJpgPictureURL(picId: str, status: Optional[str]):
    external_url = utils.pictures.getPublicHDPictureExternalUrl(picId, format="jpg")
    if external_url and status == "ready":  # we always serve non ready pictures through the API to be able to check permission:
        return external_url
    return url_for("pictures.getPictureHD", _external=True, pictureId=picId, format="jpg")


def _getSDJpgPictureURL(picId: str, status: Optional[str]):
    external_url = utils.pictures.getPublicDerivatePictureExternalUrl(picId, format="jpg", derivateFileName="sd.jpg")
    if external_url and status == "ready":  # we always serve non ready pictures through the API to be able to check permission:
        return external_url
    return url_for("pictures.getPictureSD", _external=True, pictureId=picId, format="jpg")


def _getThumbJpgPictureURL(picId: str, status: Optional[str]):
    external_url = utils.pictures.getPublicDerivatePictureExternalUrl(picId, format="jpg", derivateFileName="thumb.jpg")
    if external_url and status == "ready":  # we always serve non ready pictures through the API to be able to check permission
        return external_url
    return url_for("pictures.getPictureThumb", _external=True, pictureId=picId, format="jpg")


def _getTilesJpgPictureURL(picId: str, status: Optional[str]):
    external_url = utils.pictures.getPublicDerivatePictureExternalUrl(picId, format="jpg", derivateFileName="tiles/{TileCol}_{TileRow}.jpg")
    if external_url and status == "ready":  # we always serve non ready pictures through the API to be able to check permission:
        return external_url
    return unquote(url_for("pictures.getPictureTile", _external=True, pictureId=picId, format="jpg", col="{TileCol}", row="{TileRow}"))
