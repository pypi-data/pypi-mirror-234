import psycopg
from psycopg.sql import SQL
from flask import Blueprint, current_app, request, url_for
from geovisio import errors
from geovisio.utils import auth
from geovisio.web.utils import STAC_VERSION, cleanNoneInList, cleanNoneInDict, dbTsToStac, get_license_link, get_root_link, removeNoneInDict

CONFORMANCE_LIST = [
    "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core",
    "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson",
    "http://www.opengis.net/spec/ogcapi-common-2/1.0/conf/simple-query",
    f"https://api.stacspec.org/v{STAC_VERSION}/core",
    f"https://api.stacspec.org/v{STAC_VERSION}/browseable",
    f"https://api.stacspec.org/v{STAC_VERSION}/collections",
    f"https://api.stacspec.org/v{STAC_VERSION}/ogcapi-features",
    f"https://api.stacspec.org/v{STAC_VERSION}/item-search",
    f"https://api.stacspec.org/v{STAC_VERSION}/collection-search",
]

bp = Blueprint("stac", __name__, url_prefix="/api")


@bp.route("/")
def getLanding():
    """Retrieves API resources list
    ---
    tags:
        - Metadata
    responses:
        200:
            description: the Catalog listing resources available in this API. A non-standard "extent" property is also available (note that this may evolve in the future)
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioLanding'
    """

    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            spatial_xmin, spatial_ymin, spatial_xmax, spatial_ymax, temporal_min, temporal_max = cursor.execute(
                """
				SELECT
					GREATEST(-180, ST_XMin(ST_EstimatedExtent('pictures', 'geom'))),
					GREATEST(-90, ST_YMin(ST_EstimatedExtent('pictures', 'geom'))),
					LEAST(180, ST_XMax(ST_EstimatedExtent('pictures', 'geom'))),
					LEAST(90, ST_YMax(ST_EstimatedExtent('pictures', 'geom'))),
					MIN(ts), MAX(ts)
				FROM pictures
			"""
            ).fetchone()

            extent = (
                cleanNoneInDict(
                    {
                        "spatial": {"bbox": [[spatial_xmin, spatial_ymin, spatial_xmax, spatial_ymax]]}
                        if spatial_xmin is not None
                        else None,
                        "temporal": {"interval": [[dbTsToStac(temporal_min), dbTsToStac(temporal_max)]]}
                        if temporal_min is not None
                        else None,
                    }
                )
                if spatial_xmin is not None or temporal_min is not None
                else None
            )

            sequences = [
                {"rel": "child", "title": f'User "{s[1]}" sequences', "href": url_for("stac.getUserCatalog", userId=s[0], _external=True)}
                for s in cursor.execute(
                    """
					SELECT DISTINCT s.account_id, a.name
					FROM sequences s
					JOIN accounts a ON s.account_id = a.id
				"""
                ).fetchall()
            ]

            catalog = dbSequencesToStacCatalog(
                "geovisio",
                "GeoVisio STAC API",
                "This catalog list all geolocated pictures available in this GeoVisio instance",
                sequences,
                request,
                extent,
            )

            mapUrl = (
                url_for("map.getTile", x="111", y="222", z="333", format="mvt", _external=True)
                .replace("111", "{x}")
                .replace("222", "{y}")
                .replace("333", "{z}")
            )

            if "stac_extensions" not in catalog:
                catalog["stac_extensions"] = []

            catalog["stac_extensions"] += ["https://stac-extensions.github.io/web-map-links/v1.0.0/schema.json"]

            catalog["links"] += cleanNoneInList(
                [
                    {"rel": "service-desc", "type": "application/json", "href": url_for("flasgger.swagger", _external=True)},
                    {"rel": "service-doc", "type": "text/html", "href": url_for("flasgger.apidocs", _external=True)},
                    {"rel": "conformance", "type": "application/json", "href": url_for("stac.getConformance", _external=True)},
                    {"rel": "data", "type": "application/json", "href": url_for("stac_collections.getAllCollections", _external=True)},
                    {
                        "rel": "data",
                        "type": "application/rss+xml",
                        "href": url_for("stac_collections.getAllCollections", _external=True, format="rss"),
                    },
                    {"rel": "search", "type": "application/geo+json", "href": url_for("stac_items.searchItems", _external=True)},
                    {
                        "rel": "xyz",
                        "type": "application/vnd.mapbox-vector-tile",
                        "href": mapUrl,
                        "title": "Pictures and sequences vector tiles",
                    },
                    {
                        "rel": "collection-preview",
                        "type": "image/jpeg",
                        "href": url_for("stac_collections.getCollectionThumbnail", collectionId="{id}", _external=True),
                        "title": "Thumbnail URL for a given sequence",
                    },
                    {
                        "rel": "item-preview",
                        "type": "image/jpeg",
                        "href": url_for("pictures.getPictureThumb", pictureId="{id}", format="jpg", _external=True),
                        "title": "Thumbnail URL for a given picture",
                    },
                    get_license_link(),
                ]
            )

            return catalog, 200, {"Content-Type": "application/json"}

        raise errors.InvalidAPIUsage("Failed to connect to database", status_code=500)

    raise errors.InvalidAPIUsage("Failed to connect to database", status_code=500)


@bp.route("/conformance")
def getConformance():
    """List definitions this API conforms to
    ---
    tags:
        - Metadata
    responses:
        200:
            description: the list of definitions this API conforms to
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/STACConformance'
    """

    return {"conformsTo": CONFORMANCE_LIST}, 200, {"Content-Type": "application/json"}


def dbSequencesToStacCatalog(id, title, description, sequences, request, extent=None, **selfUrlValues):
    """Transforms a set of sequences into a STAC Catalog

    Parameters
    ----------
    id : str
        The catalog ID
    title : str
        The catalog name
    description : str
        The catalog description
    sequences : list
        List of sequences as STAC child links
    request
    current_app
    extent : dict
        Spatial and temporal extent of the catalog, in STAC format
    selfRoute : str
        API route to access this catalog (defaults to empty, for root catalog)

    Returns
    -------
    object
            The equivalent in STAC Catalog format
    """

    return removeNoneInDict(
        {
            "stac_version": STAC_VERSION,
            "id": id,
            "title": title,
            "description": description,
            "type": "Catalog",
            "conformsTo": CONFORMANCE_LIST,
            "extent": extent,
            "links": [
                {"rel": "self", "type": "application/json", "href": url_for(request.endpoint, _external=True, **selfUrlValues)},
                get_root_link(),
            ]
            + sequences,
        }
    )


def dbSequencesToStacCollection(id, title, description, sequences, request, extent=None, **selfUrlValues):
    """Transforms a set of sequences into a STAC Collection

    Parameters
    ----------
    id : str
        The collection ID
    title : str
        The collection name
    description : str
        The collection description
    sequences : list
        List of sequences as STAC child links
    request
    current_app
    extent : dict
        Spatial and temporal extent of the catalog, in STAC format
    selfRoute : str
        API route to access this collection (defaults to empty, for root catalog)

    Returns
    -------
    object
            The equivalent in STAC Collection format
    """

    return removeNoneInDict(
        {
            "stac_version": STAC_VERSION,
            "id": id,
            "title": title,
            "description": description,
            "type": "Collection",
            "conformsTo": CONFORMANCE_LIST,
            "extent": extent,
            "links": [
                {"rel": "self", "type": "application/json", "href": url_for(request.endpoint, _external=True, **selfUrlValues)},
                get_root_link(),
            ]
            + sequences,
        }
    )


@bp.route("/users/<uuid:userId>/catalog/")
@auth.isUserIdMatchingCurrentAccount()
def getUserCatalog(userId, userIdMatchesAccount=False):
    """Retrieves an user list of sequences (catalog)
    ---
    tags:
        - Sequences
        - Users
    parameters:
        - name: userId
          in: path
          description: User ID
          required: true
          schema:
            type: string
    responses:
        200:
            description: the Catalog listing all sequences associated to given user
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCatalog'
    """

    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            userName = cursor.execute("SELECT name FROM accounts WHERE id = %s", [userId]).fetchone()

            if not userName:
                raise errors.InvalidAPIUsage(f"Impossible to find user {userId}")
            userName = userName[0]
            sqlSequencesConds = ["s.account_id = %s"]

            if not userIdMatchesAccount:
                sqlSequencesConds.append("s.status = 'ready'")
                sqlSequencesConds.append("p.status = 'ready'")

            sqlSequences = (
                """
				SELECT
					s.id,
					COUNT(sp.pic_id) AS nb_pics,
					s.status,
					s.metadata->>'title' AS title,
					MIN(p.ts) AS mints,
					MAX(p.ts) AS maxts
				FROM sequences s
				LEFT JOIN sequences_pictures sp ON s.id = sp.seq_id
				LEFT JOIN pictures p on sp.pic_id = p.id
				WHERE """
                + " AND ".join(sqlSequencesConds)
                + """
				GROUP BY s.id
			"""
            )

            sequences = [
                removeNoneInDict(
                    {
                        "id": s[0],
                        "title": s[3],
                        "rel": "child",
                        "href": url_for("stac_collections.getCollection", _external=True, collectionId=s[0]),
                        "stats:items": {"count": s[1]},
                        "extent": {
                            "temporal": {
                                "interval": [
                                    [
                                        dbTsToStac(s[4]),
                                        dbTsToStac(s[5]),
                                    ]
                                ]
                            }
                        },
                        "geovisio:status": s[2] if userIdMatchesAccount else None,
                    }
                )
                for s in cursor.execute(sqlSequences, [userId]).fetchall()
            ]

            return (
                dbSequencesToStacCatalog(
                    f"user:{userId}",
                    f"{userName}'s sequences",
                    f"List of all sequences of user {userName}",
                    sequences,
                    request,
                    userId=str(userId),
                ),
                200,
                {"Content-Type": "application/json"},
            )
