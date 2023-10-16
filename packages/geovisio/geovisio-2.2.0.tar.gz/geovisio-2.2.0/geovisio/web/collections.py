import logging
from geovisio import errors, utils
from geovisio.utils import auth
from geovisio.web.params import parse_datetime, parse_datetime_interval, parse_bbox
from geovisio.web.rss import dbSequencesToGeoRSS
import psycopg
from psycopg.rows import dict_row
from psycopg.sql import SQL
import datetime
from flask import current_app, request, url_for, Blueprint
from geovisio.web.utils import (
    STAC_VERSION,
    accountIdOrDefault,
    cleanNoneInDict,
    cleanNoneInList,
    dbTsToStac,
    get_license_link,
    get_root_link,
    removeNoneInDict,
)
from geovisio.workers import runner_pictures
import geovisio.utils.sequences

bp = Blueprint("stac_collections", __name__, url_prefix="/api")


def dbSequenceToStacCollection(dbSeq, description="A sequence of geolocated pictures"):
    """Transforms a sequence extracted from database into a STAC Collection

    Parameters
    ----------
    dbSeq : dict
        A row from sequences table in database (with id, name, minx, miny, maxx, maxy, mints, maxts fields)
    request
    current_app

    Returns
    -------
    object
        The equivalent in STAC Collection format
    """
    mints, maxts, insertedAt, updatedAt = dbSeq.get("mints"), dbSeq.get("maxts"), dbSeq.get("inserted_at"), dbSeq.get("updated_at")
    return removeNoneInDict(
        {
            "type": "Collection",
            "stac_version": STAC_VERSION,
            "stac_extensions": ["https://stac-extensions.github.io/stats/v0.2.0/schema.json"],  # For stats: fields
            "id": str(dbSeq["id"]),
            "title": str(dbSeq["name"]),
            "description": description,
            "keywords": ["pictures", str(dbSeq["name"])],
            "license": current_app.config["API_PICTURES_LICENSE_SPDX_ID"],
            "created": dbTsToStac(insertedAt),
            "updated": dbTsToStac(updatedAt),
            "geovisio:status": dbSeq.get("status"),
            "providers": [
                {"name": dbSeq["account_name"], "roles": ["producer"]},
            ],
            "extent": {
                "spatial": {"bbox": [[dbSeq["minx"] or -180.0, dbSeq["miny"] or -90.0, dbSeq["maxx"] or 180.0, dbSeq["maxy"] or 90.0]]},
                "temporal": {
                    "interval": [
                        [
                            dbTsToStac(mints),
                            dbTsToStac(maxts),
                        ]
                    ]
                },
            },
            "summaries": cleanNoneInDict({"pers:interior_orientation": dbSeq.get("metas")}),
            "stats:items": removeNoneInDict({"count": dbSeq.get("nbpic")}),
            "links": cleanNoneInList(
                [
                    {
                        "rel": "items",
                        "type": "application/geo+json",
                        "title": "Pictures in this sequence",
                        "href": url_for("stac_items.getCollectionItems", _external=True, collectionId=dbSeq["id"]),
                    },
                    {
                        "rel": "parent",
                        "type": "application/json",
                        "title": "Instance catalog",
                        "href": url_for("stac.getLanding", _external=True),
                    },
                    get_root_link(),
                    {
                        "rel": "self",
                        "type": "application/json",
                        "title": "Metadata of this sequence",
                        "href": url_for("stac_collections.getCollection", _external=True, collectionId=dbSeq["id"]),
                    },
                    get_license_link(),
                ]
            ),
        }
    )


SEQUENCES_DEFAULT_FETCH = 100
SEQUENCES_MAX_FETCH = 1000


@bp.route("/collections")
def getAllCollections():
    """List available collections
    ---
    tags:
        - Sequences
    parameters:
        - name: limit
          in: query
          description: Estimated number of items that should be present in response. Defaults to 100. Note that response can contain a bit more or a bit less responses due to internal mechanisms.
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 1000
        - name: created_after
          in: query
          description: Filter for collection uploaded after this date. To filter by capture date, use datetime instead.
          required: false
          schema:
            type: string
            format: date-time
        - name: created_before
          in: query
          description: Filter for collection uploaded before this date. To filter by capture date, use datetime instead.
          required: false
          schema:
            type: string
            format: date-time
        - name: format
          in: query
          description: Expected output format (STAC JSON or RSS XML)
          required: false
          schema:
            type: string
            enum: [rss, json]
            default: json
        - $ref: '#/components/parameters/STAC_bbox'
        - name: datetime
          in: query
          required: false
          schema:
            type: string
          explode: false
          description: >-
            Filter sequence by capture date. To filter by upload date, use created_before and created_after instead.

            You can filter by a single date or a date interval, open or closed.

            Adhere to RFC 3339. Open intervals are expressed using double-dots.

            This endpoint will only answer based on date (not time) value, even
            if time can be set in query (for STAC compatibility purposes).

            Examples:

            * A date-time: "2018-02-12"

            * A closed interval: "2018-02-12/2018-03-18"

            * Open intervals: "2018-02-12/.." or "../2018-03-18"

    responses:
        200:
            description: the list of available collections
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollections'
                application/rss+xml:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollectionsRSS'
    """

    args = request.args
    insertSort = "ASC"
    params: dict = {}
    seq_filter = [SQL("s.status = 'ready'")]

    # Datetime
    min_dt, max_dt = parse_datetime_interval(args.get("datetime"))
    if min_dt is not None:
        seq_filter.append(SQL("s.computed_capture_date >= %(cmindate)s::date"))
        params["cmindate"] = min_dt
    if max_dt is not None:
        seq_filter.append(SQL("s.computed_capture_date <= %(cmaxdate)s::date"))
        params["cmaxdate"] = max_dt

    # Expected output format
    format = args["format"] if args.get("format") in ["rss", "json"] else "json"
    if (
        args.get("format") is None
        and request.accept_mimetypes.best_match(["application/json", "application/rss+xml"], "application/json") == "application/rss+xml"
    ):
        format = "rss"

    if format == "rss":
        insertSort = "DESC"

    # Check if limit is valid
    limit = args.get("limit", SEQUENCES_DEFAULT_FETCH)
    try:
        limit = int(limit)
    except ValueError:
        raise errors.InvalidAPIUsage(f"limit parameter should be a valid, positive integer (between 1 and {SEQUENCES_MAX_FETCH})")
    if limit < 1 or limit > SEQUENCES_MAX_FETCH:
        raise errors.InvalidAPIUsage(f"limit parameter should be an integer between 1 and {SEQUENCES_MAX_FETCH}")
    params["limit"] = limit

    # Bounding box
    bboxarg = parse_bbox(args.get("bbox"))
    if bboxarg is not None:
        seq_filter.append(SQL("s.geom && ST_MakeEnvelope(%(minx)s, %(miny)s, %(maxx)s, %(maxy)s, 4326)"))
        params["minx"] = bboxarg[0]
        params["miny"] = bboxarg[1]
        params["maxx"] = bboxarg[2]
        params["maxy"] = bboxarg[3]

    # Prepare request
    fields = SQL(
        """
        s.id,
        s.metadata->>'title' AS name,
        ST_XMin(s.geom) AS minx,
        ST_YMin(s.geom) AS miny,
        ST_XMax(s.geom) AS maxx,
        ST_YMax(s.geom) AS maxy,
        accounts.name AS account_name,
        s.inserted_at,
        s.updated_at,
        ST_X(ST_PointN(s.geom, 1)) AS x1,
        ST_Y(ST_PointN(s.geom, 1)) AS y1,
        s.computed_capture_date
    """
    )

    sequence_table = SQL(
        """
        SELECT {fields}
        FROM sequences s
        JOIN accounts ON accounts.id = s.account_id
        WHERE {sequence_filter}
        ORDER BY s.inserted_at {insertSort}
        LIMIT %(limit)s
    """
    )

    # Created after/before
    created_after = args.get("created_after")
    created_before = args.get("created_before")

    if created_after:
        created_after = parse_datetime(created_after, error=f"Invalid `created_after` argument", fallback_as_UTC=True)
        seq_filter.append(SQL("s.inserted_at > %(created_after)s::timestamp with time zone"))
        params["created_after"] = created_after

    if created_before:
        created_before = parse_datetime(created_before, error=f"Invalid `created_before` argument", fallback_as_UTC=True)
        seq_filter.append(SQL("s.inserted_at < %(created_before)s::timestamp with time zone"))
        params["created_before"] = created_before

        if not created_after:
            # If there is only a created_before parameter, we want all last collections that have been created before the date
            sequence_table = SQL(
                """SELECT * FROM (
                    SELECT {fields}
                        FROM sequences s 
                        JOIN accounts ON accounts.id = s.account_id
                        WHERE {sequence_filter}
                        ORDER BY s.inserted_at DESC
                        LIMIT %(limit)s
                    ) s
                    ORDER BY s.inserted_at {insertSort}
                """
            )

    paginated = limit is not None or created_after is not None or created_before is not None

    sequence_table = sequence_table.format(sequence_filter=SQL(" AND ").join(seq_filter), fields=fields, insertSort=SQL(insertSort))
    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            stats = cursor.execute("SELECT min(inserted_at) as min, max(inserted_at) as max FROM sequences").fetchone()
            inserted_at_bound = (stats["min"], stats["max"]) if stats is not None else (None, None)

            if inserted_at_bound[1] and created_after and created_after > inserted_at_bound[1]:
                raise errors.InvalidAPIUsage(f"There is no collection created after {created_after}")
            if inserted_at_bound[0] and created_before and created_before < inserted_at_bound[0]:
                raise errors.InvalidAPIUsage(f"There is no collection created before {created_before}")

            query = SQL(
                """
                SELECT *
                    FROM (
                        {sequence_table}
                    ) s
                LEFT JOIN LATERAL (
                        SELECT MIN(p.ts) as mints,
                                MAX(p.ts) as maxts,
                                COUNT(p.*) AS nbpic
                        FROM sequences_pictures sp
                                JOIN pictures p ON sp.pic_id = p.id
                        WHERE p.status = 'ready'
                                AND sp.seq_id = s.id
                        GROUP BY sp.seq_id
                ) sub ON true;
                """
            ).format(sequence_table=sequence_table)
            records = cursor.execute(
                query,
                params,
            ).fetchall()

            # RSS results
            if format == "rss":
                return (dbSequencesToGeoRSS(records).rss(), 200, {"Content-Type": "text/xml"})

            # STAC JSON results
            else:
                collections = []
                min_inserted_at = None
                max_inserted_at = None
                for dbSeq in records:
                    if min_inserted_at is None:
                        min_inserted_at = dbSeq["inserted_at"]
                    max_inserted_at = dbSeq["inserted_at"]
                    collections.append(dbSequenceToStacCollection(dbSeq))

                # Compute paginated links
                links = [
                    get_root_link(),
                    {"rel": "parent", "type": "application/json", "href": url_for("stac.getLanding", _external=True)},
                    {
                        "rel": "self",
                        "type": "application/json",
                        "href": url_for(
                            "stac_collections.getAllCollections",
                            _external=True,
                            limit=args.get("limit"),
                            created_after=args.get("created_after"),
                        ),
                    },
                ]

                links.append(
                    {
                        "rel": "first",
                        "type": "application/json",
                        "href": url_for("stac_collections.getAllCollections", _external=True, limit=limit),
                    }
                )
                if paginated:
                    if inserted_at_bound[1]:
                        links.append(
                            {
                                "rel": "last",
                                "type": "application/json",
                                "href": url_for(
                                    "stac_collections.getAllCollections",
                                    _external=True,
                                    limit=limit,
                                    created_before=dbTsToStac(inserted_at_bound[1] + datetime.timedelta(seconds=1)),
                                ),
                            }
                        )

                has_more_sequences_before = min_inserted_at > inserted_at_bound[0] if inserted_at_bound[0] and min_inserted_at else False
                if has_more_sequences_before:
                    links.append(
                        {
                            "rel": "prev",
                            "type": "application/json",
                            "href": url_for(
                                "stac_collections.getAllCollections",
                                _external=True,
                                limit=limit,
                                created_before=dbTsToStac(min_inserted_at),
                            ),
                        }
                    )

                has_more_sequences_after = max_inserted_at < inserted_at_bound[1] if inserted_at_bound[1] and max_inserted_at else False
                if has_more_sequences_after:
                    links.append(
                        {
                            "rel": "next",
                            "type": "application/json",
                            "href": url_for(
                                "stac_collections.getAllCollections", _external=True, limit=limit, created_after=dbTsToStac(max_inserted_at)
                            ),
                        }
                    )

                return (
                    {
                        "collections": collections,
                        "links": links,
                    },
                    200,
                    {"Content-Type": "application/json"},
                )


@bp.route("/collections/<uuid:collectionId>")
def getCollection(collectionId):
    """Retrieve metadata of a single collection
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
    responses:
        200:
            description: the collection metadata
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollection'
    """

    account = auth.get_current_account()

    params = {
        "id": collectionId,
        # Only the owner of an account can view sequence not 'ready'
        "account": account.id if account is not None else None,
    }

    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            record = cursor.execute(
                """
				SELECT
					s.id, s.metadata->>'title' AS name,
					ST_XMin(s.geom) AS minx,
					ST_YMin(s.geom) AS miny,
					ST_XMax(s.geom) AS maxx,
					ST_YMax(s.geom) AS maxy,
					s.status,
     			accounts.name AS account_name,
     			s.inserted_at,
     			s.updated_at,
					a.*
				FROM sequences s
				JOIN accounts ON s.account_id = accounts.id, (
					SELECT
						MIN(ts) as mints,
						MAX(ts) as maxts,
						array_agg(DISTINCT jsonb_build_object(
							'make', metadata->>'make',
							'model', metadata->>'model',
							'focal_length', metadata->>'focal_length',
							'field_of_view', metadata->>'field_of_view'
						)) AS metas,
						COUNT(*) AS nbpic
					FROM pictures p
					JOIN sequences_pictures sp ON sp.seq_id = %(id)s AND sp.pic_id = p.id
				) a
				WHERE s.id = %(id)s
					AND (s.status != 'hidden' OR s.account_id = %(account)s)
			""",
                params,
            ).fetchone()

            if record is None:
                raise errors.InvalidAPIUsage("Collection doesn't exist", status_code=404)

            return (
                dbSequenceToStacCollection(record),
                200,
                {
                    "Content-Type": "application/json",
                },
            )


@bp.route("/collections/<uuid:collectionId>/thumb.jpg", methods=["GET"])
def getCollectionThumbnail(collectionId):
    """Get the thumbnail representing a single collection
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
    responses:
        200:
            description: 500px wide ready-for-display image
            content:
                image/jpeg:
                    schema:
                        type: string
                        format: binary
    """
    account = auth.get_current_account()

    params = {
        "seq": collectionId,
        # Only the owner of an account can view pictures not 'ready'
        "account": account.id if account is not None else None,
    }

    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            records = cursor.execute(
                """
				SELECT
					sp.pic_id
				FROM sequences_pictures sp
				JOIN pictures p ON sp.pic_id = p.id
				JOIN sequences s ON sp.seq_id = s.id
				WHERE
					sp.seq_id = %(seq)s
					AND (p.status = 'ready' OR p.account_id = %(account)s)
					AND (s.status = 'ready' OR s.account_id = %(account)s)
				LIMIT 1
			""",
                params,
            ).fetchone()

            if records is None:
                raise errors.InvalidAPIUsage("Impossible to find a thumbnail for the collection", status_code=404)

            return utils.pictures.sendThumbnail(records["pic_id"], "jpg")


@bp.route("/collections", methods=["POST"])
@auth.login_required_by_setting("API_FORCE_AUTH_ON_UPLOAD")
def postCollection(account=None):
    """Create a new sequence
    ---
    tags:
        - Upload
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/GeoVisioPostCollection'
            application/x-www-form-urlencoded:
                schema:
                    $ref: '#/components/schemas/GeoVisioPostCollection'
            multipart/form-data:
                schema:
                    $ref: '#/components/schemas/GeoVisioPostCollection'
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        200:
            description: the collection metadata
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollection'
    """

    # Parse received parameters
    metadata = {}
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        metadata["title"] = request.json.get("title")
    elif content_type in ["multipart/form-data", "application/x-www-form-urlencoded"]:
        metadata["title"] = request.form.get("title")

    metadata = removeNoneInDict(metadata)

    # Create sequence folder
    accountId = accountIdOrDefault(account)
    seqId = geovisio.utils.sequences.createSequence(metadata, accountId)

    # Return created sequence
    return (
        getCollection(seqId)[0],
        200,
        {
            "Content-Type": "application/json",
            "Access-Control-Expose-Headers": "Location",  # Needed for allowing web browsers access Location header
            "Location": url_for("stac_collections.getCollection", _external=True, collectionId=seqId),
        },
    )


@bp.route("/collections/<uuid:collectionId>", methods=["PATCH"])
@auth.login_required()
def patchCollection(collectionId, account):
    """Edits properties of an existing collection
    ---
    tags:
        - Editing
    parameters:
        - name: collectionId
          in: path
          description: The sequence ID
          required: true
          schema:
            type: string
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/GeoVisioPatchCollection'
            application/x-www-form-urlencoded:
                schema:
                    $ref: '#/components/schemas/GeoVisioPatchCollection'
            multipart/form-data:
                schema:
                    $ref: '#/components/schemas/GeoVisioPatchCollection'
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        200:
            description: the wanted collection
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollection'
    """

    # Parse received parameters
    metadata = {}
    content_type = (request.headers.get("Content-Type") or "").split(";")[0]
    if content_type == "application/json":
        metadata["visible"] = request.json.get("visible")
    elif content_type in ["multipart/form-data", "application/x-www-form-urlencoded"]:
        metadata["visible"] = request.form.get("visible")

    # Check if visibility param is valid
    visible = metadata.get("visible")
    if visible is not None:
        if visible in ["true", "false"]:
            visible = visible == "true"
        else:
            raise errors.InvalidAPIUsage("Picture visibility parameter (visible) should be either unset, true or false", status_code=400)

    if visible is None:
        # /!\ As visible is the only editable thing for now, we can return if it's null
        # The line below may be removed when other parameters will be available for patching
        return getCollection(collectionId)

    # Check if sequence exists and if given account is authorized to edit
    with psycopg.connect(current_app.config["DB_URL"]) as conn, conn.cursor() as cursor:
        seq = cursor.execute("SELECT status, account_id FROM sequences WHERE id = %s", [collectionId]).fetchone()

        # Sequence not found
        if not seq:
            raise errors.InvalidAPIUsage(f"Sequence {collectionId} wasn't found in database", status_code=404)

        # Account associated to sequence doesn't match current user
        if account is not None and account.id != str(seq[1]):
            raise errors.InvalidAPIUsage("You're not authorized to edit this sequence", status_code=403)

        # Let's edit this picture
        oldStatus = seq[0]

        if visible is not None:
            if oldStatus not in ["ready", "hidden"]:
                # Sequence is in a preparing/broken/... state so no edit possible
                raise errors.InvalidAPIUsage(
                    f"Sequence {collectionId} is in {oldStatus} state, its visibility can't be changed for now", status_code=400
                )

            newStatus = "ready" if visible is True else "hidden"

            if newStatus != oldStatus:
                cursor.execute("UPDATE sequences SET status = %s WHERE id = %s", [newStatus, collectionId])
                conn.commit()

        # Redirect response to a classic GET
        return getCollection(collectionId)


@bp.route("/collections/<uuid:collectionId>", methods=["DELETE"])
@auth.login_required()
def deleteCollection(collectionId, account):
    """Delete a collection and all the associated pictures
    The associated images will be hidden right away and deleted asynchronously
    ---
    tags:
        - Editing
    parameters:
        - name: collectionId
          in: path
          description: ID of the collection
          required: true
          schema:
            type: string
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        204:
            description: The collection has been correctly deleted
    """

    # Check if collection exists and if given account is authorized to edit
    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            sequence = cursor.execute("SELECT status, account_id FROM sequences WHERE id = %s", [collectionId]).fetchone()

            # sequence not found
            if not sequence:
                raise errors.InvalidAPIUsage(f"Collection {collectionId} wasn't found in database", status_code=404)

            # Account associated to sequence doesn't match current user
            if account is not None and account.id != str(sequence[1]):
                raise errors.InvalidAPIUsage("You're not authorized to edit this sequence", status_code=403)

            logging.info(f"Asking for deletion of sequence {collectionId} and all its pictures")

            # mark all the pictures as waiting for deletion for async removal as this can be quite long if the storage is slow if there are lots of pictures
            nb_updated = cursor.execute(
                """
                WITH pic2rm AS (
                        SELECT pic_id FROM sequences_pictures WHERE seq_id = %(seq)s
                ),
                picWithoutOtherSeq AS (
                    SELECT pic_id FROM pic2rm
                    EXCEPT
                    SELECT pic_id FROM sequences_pictures WHERE pic_id IN (SELECT pic_id FROM pic2rm) AND seq_id != %(seq)s
                ),
                -- Add async task to delete all picture
                pic_insertion AS (
                    INSERT INTO pictures_to_process(picture_id, task)
                        SELECT pic_id, 'delete' FROM picWithoutOtherSeq
                    ON CONFLICT (picture_id) DO UPDATE SET task = 'delete'
                )
                UPDATE pictures SET status = 'waiting-for-delete' WHERE id IN (SELECT pic_id FROM picWithoutOtherSeq)
			""",
                {"seq": collectionId},
            ).rowcount

            cursor.execute("DELETE FROM sequences WHERE id = %s", [collectionId])
            conn.commit()

            # add background task if needed, to really delete pictures
            for _ in range(nb_updated):
                runner_pictures.background_processor.process_pictures()

            return "", 204


@bp.route("/collections/<uuid:collectionId>/geovisio_status")
def getCollectionImportStatus(collectionId):
    """Retrieve import status of all pictures in sequence
    ---
    tags:
        - Upload
    parameters:
        - name: collectionId
          in: path
          description: ID of collection to retrieve
          required: true
          schema:
            type: string
    responses:
        200:
            description: the pictures statuses
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollectionImportStatus'
    """

    account = auth.get_current_account()
    params = {"seq_id": collectionId, "account": account.id if account is not None else None}
    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            sequence_status = cursor.execute(
                """
			WITH items AS (
				SELECT p.id, p.status, sp.rank, sp.seq_id, p.process_error, p.nb_errors, p.processed_at
				FROM sequences_pictures sp
				JOIN pictures p on sp.pic_id = p.id
				JOIN sequences s on sp.seq_id = s.id
				WHERE
    				sp.seq_id = %(seq_id)s
        			AND (p.status != 'hidden' OR p.account_id = %(account)s)
        			AND (s.status != 'hidden' OR s.account_id = %(account)s)
				ORDER BY sp.rank
			)
			SELECT json_build_object(
					'status', s.status,
					'items', json_agg(
							json_build_object(
									'id', i.id,
									'status', i.status,
									'process_error', i.process_error,
									'nb_errors', i.nb_errors,
									'processed_at', i.processed_at,
									'rank', i.rank
							)
					)
			) AS sequence
			FROM items i
			JOIN sequences s on i.seq_id = s.id
			GROUP by s.id;
			""",
                params,
            ).fetchall()

            if len(sequence_status) == 0:
                raise errors.InvalidAPIUsage("Sequence is either empty or doesn't exists", status_code=404)

            return sequence_status[0]["sequence"]


@bp.route("/users/<uuid:userId>/collection")
@auth.isUserIdMatchingCurrentAccount()
def getUserCollection(userId, userIdMatchesAccount=False):
    """Retrieves an collection of the user list collections

    It's quite the same as "/users/<uuid:userId>/catalog/" but with additional information, as a STAC collection have more metadatas than STAC catalogs.
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
            description: the Collection listing all sequences associated to given user
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollectionOfCollection'
    """

    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            userName = cursor.execute("SELECT name FROM accounts WHERE id = %s", [userId]).fetchone()

            if not userName:
                raise errors.InvalidAPIUsage(f"Impossible to find user {userId}")
            userName = userName["name"]
            sqlSequencesConds = [SQL("s.account_id = %s")]

            if not userIdMatchesAccount:
                sqlSequencesConds.append(SQL("s.status = 'ready'"))
                sqlSequencesConds.append(SQL("p.status = 'ready'"))

            meta_collection = cursor.execute(
                SQL(
                    """SELECT
					COUNT(sp.pic_id) AS nbpic,
					MIN(p.ts) AS mints,
					MAX(p.ts) AS maxts,
					MIN(GREATEST(-180, ST_X(p.geom))) AS minx,
					MIN(GREATEST(-90, ST_Y(p.geom))) AS miny,
					MAX(LEAST(180, ST_X(p.geom))) AS maxx,
					MAX(LEAST(90, ST_Y(p.geom))) AS maxy,
                    MIN(s.inserted_at) AS inserted_at,
                    MAX(s.updated_at) AS updated_at
				FROM sequences s
				LEFT JOIN sequences_pictures sp ON s.id = sp.seq_id
				LEFT JOIN pictures p on sp.pic_id = p.id
				WHERE {filter}
			"""
                ).format(filter=SQL(" AND ").join(sqlSequencesConds)),
                [userId],
            ).fetchone()

            if not meta_collection:
                raise errors.InvalidAPIUsage(f"No data loaded for user {userId}", 404)

            sqlSequences = SQL(
                """
				SELECT
					s.id,
					COUNT(sp.pic_id) AS nbpic,
					s.status,
					s.metadata->>'title' AS title,
                    s.inserted_at AS created,
                    s.updated_at AS updated,
					MIN(p.ts) AS mints,
					MAX(p.ts) AS maxts,
                    ST_XMin(s.geom) AS minx,
                    ST_YMin(s.geom) AS miny,
                    ST_XMax(s.geom) AS maxx,
                    ST_YMax(s.geom) AS maxy
				FROM sequences s
				LEFT JOIN sequences_pictures sp ON s.id = sp.seq_id
				LEFT JOIN pictures p on sp.pic_id = p.id
				WHERE {filter}
				GROUP BY s.id
			"""
            ).format(filter=SQL(" AND ").join(sqlSequencesConds))

            sequences_links = [
                removeNoneInDict(
                    {
                        "id": s["id"],
                        "title": s["title"],
                        "rel": "child",
                        "href": url_for("stac_collections.getCollection", _external=True, collectionId=s["id"]),
                        "stats:items": {"count": s["nbpic"]},
                        "created": dbTsToStac(s["created"]),
                        "updated": dbTsToStac(s["updated"]),
                        "extent": {
                            "temporal": {
                                "interval": [
                                    [
                                        dbTsToStac(s["mints"]),
                                        dbTsToStac(s["maxts"]),
                                    ]
                                ]
                            },
                            "spatial": {"bbox": [[s["minx"] or -180.0, s["miny"] or -90.0, s["maxx"] or 180.0, s["maxy"] or 90.0]]},
                        },
                        "geovisio:status": s["status"] if userIdMatchesAccount else None,
                    }
                )
                for s in cursor.execute(sqlSequences, [userId]).fetchall()
            ]

            meta_collection.update(
                {
                    "id": f"user:{userId}",
                    "name": f"{userName}'s sequences",
                    "account_name": userName,
                }
            )
            collection = dbSequenceToStacCollection(meta_collection, description=f"List of all sequences of user {userName}")

            # add all sub collections as links
            collection["links"].extend(sequences_links)

            # and we update the self link since it's not a collection mapped directly to a sequence
            self = next(l for l in collection["links"] if l["rel"] == "self")
            self["href"] = url_for("stac_collections.getUserCollection", _external=True, userId=str(userId))

            collection["stac_extensions"].append(
                "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json"
            )  # for `updated`/`created` fields in links

            return (collection, 200, {"Content-Type": "application/json"})
