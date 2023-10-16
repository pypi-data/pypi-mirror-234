import re
import os
from uuid import UUID
from datetime import date, datetime
import psycopg
from pystac import ItemCollection, Item
from flask import json
import requests
import pytest
import psycopg
import math
from dateutil import tz
import itertools
from uuid import UUID
from urllib.parse import urlencode
import time
from PIL import Image
from geopic_tag_reader import reader
from geovisio import create_app
import geovisio.utils.pictures
import geovisio.web.collections
import geovisio.web.items
from . import conftest


@conftest.SEQ_IMGS
def test_items(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqId = cursor.execute("SELECT id FROM sequences LIMIT 1").fetchone()[0]

            response = client.get("/api/collections/" + str(seqId) + "/items")
            data = response.json

            assert response.status_code == 200

            assert data["type"] == "FeatureCollection"
            assert len(data["features"]) == 5
            assert len(data["links"]) == 3

            clc = ItemCollection.from_dict(data)
            assert len(clc) == 5

            # Check if items have next/prev picture info
            i = 0
            for item in clc:
                nbPrev = len([l for l in item.links if l.rel == "prev"])
                nbNext = len([l for l in item.links if l.rel == "next"])
                if i == 0:
                    assert nbPrev == 0
                    assert nbNext == 1
                elif i == len(clc) - 1:
                    assert nbPrev == 1
                    assert nbNext == 0
                else:
                    assert nbPrev == 1
                    assert nbNext == 1

                i += 1

            # Make one picture not available
            picHidden = data["features"][0]["id"]
            cursor.execute("UPDATE pictures SET status = 'hidden' WHERE id = %s", [picHidden])
            conn.commit()

            response = client.get("/api/collections/" + str(seqId) + "/items")
            data = response.json

            assert response.status_code == 200

            assert data["type"] == "FeatureCollection"
            assert len(data["features"]) == 4
            picIds = [f["id"] for f in data["features"]]
            assert picHidden not in picIds
            assert data["features"][0]["providers"] == [
                {"name": "Default account", "roles": ["producer"]},
            ]


@conftest.SEQ_IMGS
def test_items_pagination_classic(datafiles, initSequence, dburl):
    """Linear test case : get page one by one, consecutively"""

    client = initSequence(datafiles, preprocess=False)
    seq = conftest.getPictureIds(dburl)[0]
    picIds = [p.id for p in seq.pictures]

    # First page
    response = client.get(f"/api/collections/{seq.id}/items?limit=2")
    data = response.json

    assert response.status_code == 200
    assert data["type"] == "FeatureCollection"

    clc = ItemCollection.from_dict(data)
    assert len(clc) == 2

    assert clc[0].id == picIds[0]
    assert clc[1].id == picIds[1]

    links = clc.extra_fields["links"]
    assert len(links) == 6

    assert {l["rel"]: l["href"] for l in clc.extra_fields["links"]} == {
        "root": "http://localhost/api/",
        "parent": f"http://localhost/api/collections/{seq.id}",
        "self": f"http://localhost/api/collections/{seq.id}/items?limit=2",
        "first": f"http://localhost/api/collections/{seq.id}/items?limit=2",
        "last": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=3",
        "next": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=2",
    }

    # Second page
    response = client.get(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=2")
    data = response.json

    assert response.status_code == 200
    clc = ItemCollection.from_dict(data)
    assert len(clc) == 2
    links = clc.extra_fields["links"]
    assert len(links) == 7

    assert clc[0].id == picIds[2]
    assert clc[1].id == picIds[3]

    assert {l["rel"]: l["href"] for l in clc.extra_fields["links"]} == {
        "root": "http://localhost/api/",
        "parent": f"http://localhost/api/collections/{seq.id}",
        "self": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=2",
        "first": f"http://localhost/api/collections/{seq.id}/items?limit=2",
        "last": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=4",
        "prev": f"http://localhost/api/collections/{seq.id}/items?limit=2",
        "next": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=4",
    }
    # Third page
    response = client.get(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=4")
    data = response.json

    assert response.status_code == 200
    clc = ItemCollection.from_dict(data)
    assert len(clc) == 1
    links = clc.extra_fields["links"]
    assert len(links) == 6

    assert clc[0].id == picIds[4]

    assert {l["rel"]: l["href"] for l in clc.extra_fields["links"]} == {
        "root": "http://localhost/api/",
        "parent": f"http://localhost/api/collections/{seq.id}",
        "first": f"http://localhost/api/collections/{seq.id}/items?limit=2",
        "last": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=4",
        "prev": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=2",
        "self": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=4",
    }


@conftest.SEQ_IMGS
def test_items_pagination_nolimit(datafiles, initSequence, dburl):
    """Calling next without limit"""

    client = initSequence(datafiles, preprocess=False)
    seq = conftest.getPictureIds(dburl)[0]

    response = client.get(f"/api/collections/{seq.id}/items?startAfterRank=2")
    assert response.status_code == 200
    clc = ItemCollection.from_dict(response.json)
    assert len(clc) == 3
    links = clc.extra_fields["links"]
    assert len(links) == 6, [l["rel"] for l in links]

    assert clc[0].id == seq.pictures[2].id
    assert clc[1].id == seq.pictures[3].id
    assert clc[2].id == seq.pictures[4].id

    # we should have all the pagination links
    assert {l["rel"]: l["href"] for l in clc.extra_fields["links"]} == {
        "root": "http://localhost/api/",
        "parent": f"http://localhost/api/collections/{seq.id}",
        "first": f"http://localhost/api/collections/{seq.id}/items",
        "last": f"http://localhost/api/collections/{seq.id}/items?startAfterRank=2",
        "prev": f"http://localhost/api/collections/{seq.id}/items",
        "self": f"http://localhost/api/collections/{seq.id}/items?startAfterRank=2",
    }


@conftest.SEQ_IMGS
def test_items_pagination_outalimit(datafiles, initSequence, dburl):
    """Requests using invalid or out of limit values"""
    client = initSequence(datafiles, preprocess=False)
    seq = conftest.getPictureIds(dburl)[0]

    # Invalid limit
    for v in ["100000000000000000000", "prout", "-1"]:
        response = client.get("/api/collections/" + seq.id + "/items?limit=" + v)
        assert response.status_code == 400

    # Out of bounds next rank
    response = client.get("/api/collections/" + seq.id + "/items?startAfterRank=9000")
    assert response.status_code == 404
    assert response.json == {"message": "No more items in this collection (last available rank is 5)", "status_code": 404}

    # Remove everything
    with psycopg.connect(dburl, autocommit=True) as conn:
        conn.execute("DELETE FROM sequences_pictures")

    response = client.get("/api/collections/" + seq.id + "/items?limit=2")
    assert response.status_code == 200 and response.json["features"] == []


@conftest.SEQ_IMGS
def test_items_empty_collection(app, client, datafiles, initSequence, dburl, bobAccountToken):
    """Requests the items of an empty collection"""
    seq_location = conftest.createSequence(client, "a_sequence", jwtToken=bobAccountToken(app))
    seq_id = seq_location.split("/")[-1]

    # the collection is not ready (there is no pictures), so it is hidden by default
    response = client.get(f"/api/collections/{seq_id}/items")
    assert response.status_code == 404
    assert response.json == {"message": "Collection doesn't exist", "status_code": 404}

    # but bob see an empty collection
    response = client.get(f"/api/collections/{seq_id}/items", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert response.status_code == 200 and response.json["features"] == []


@conftest.SEQ_IMGS
def test_items_withPicture_no_limit(datafiles, initSequence, dburl):
    """Asking for a page with a specific picture in it"""

    client = initSequence(datafiles, preprocess=False)
    seq = conftest.getPictureIds(dburl)[0]
    pic_ids = [p.id for p in seq.pictures]

    response = client.get(f"/api/collections/{seq.id}/items?withPicture={seq.pictures[1].id}")
    assert response.status_code == 200
    clc = ItemCollection.from_dict(response.json)
    assert len(clc) == 4
    links = {l["rel"]: l["href"] for l in clc.extra_fields["links"]}
    # we should have all the pagination links
    assert links == {
        "root": "http://localhost/api/",
        "parent": f"http://localhost/api/collections/{seq.id}",
        "first": f"http://localhost/api/collections/{seq.id}/items",
        "last": f"http://localhost/api/collections/{seq.id}/items",
        "prev": f"http://localhost/api/collections/{seq.id}/items",
        "self": f"http://localhost/api/collections/{seq.id}/items",
    }

    assert [c.id for c in clc] == pic_ids[1:]


@conftest.SEQ_IMGS
def test_items_withPicture_with_limit(datafiles, initSequence, dburl):
    """
    Asking for a page with a specific picture in it with a limit, we should get the nth page with the picture
    There is 5 pics, if we ask for the fourth pic, with a limit=2, we should get a page with the third and the fourth pic
    """
    client = initSequence(datafiles, preprocess=False)
    seq = conftest.getPictureIds(dburl)[0]
    pic_ids = [p.id for p in seq.pictures]

    response = client.get(f"/api/collections/{seq.id}/items?withPicture={seq.pictures[3].id}&limit=2")
    assert response.status_code == 200
    clc = ItemCollection.from_dict(response.json)
    assert len(clc) == 2
    links = {l["rel"]: l["href"] for l in clc.extra_fields["links"]}
    # we should have all the pagination links
    assert links == {
        "root": "http://localhost/api/",
        "parent": f"http://localhost/api/collections/{seq.id}",
        "first": f"http://localhost/api/collections/{seq.id}/items?limit=2",
        "last": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=4",
        "next": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=4",
        "prev": f"http://localhost/api/collections/{seq.id}/items?limit=2",  # the prev link should be the 1st and 2nd pic, so the first page
        "self": f"http://localhost/api/collections/{seq.id}/items?limit=2",
    }

    assert [c.id for c in clc] == pic_ids[2:4]


@conftest.SEQ_IMGS
@conftest.SEQ_IMGS_FLAT
def test_items_withPicture_invalid(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    seqs = conftest.getPictureIds(dburl)

    response = client.get(f"/api/collections/{seqs[0].id}/items?withPicture=plop")
    assert response.status_code == 400
    assert response.json == {"message": "withPicture should be a valid UUID", "status_code": 400}

    response = client.get(f"/api/collections/{seqs[0].id}/items?withPicture=00000000-0000-0000-0000-000000000000")
    assert response.status_code == 400
    assert response.json == {"message": "Picture with id 00000000-0000-0000-0000-000000000000 does not exists", "status_code": 400}

    # asking for a picture in another collection should also trigger an error
    response = client.get(f"/api/collections/{seqs[0].id}/items?withPicture={seqs[1].pictures[0].id}")
    assert response.status_code == 400
    assert response.json == {"message": f"Picture with id {seqs[1].pictures[0].id} does not exists", "status_code": 400}


@conftest.SEQ_IMGS
def test_items_pagination_nonconsecutive(datafiles, initSequence, dburl):
    """Pagination over non-consecutive pictures ranks"""

    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seq = conftest.getPictureIds(dburl)[0]

            cursor.execute("DELETE FROM sequences_pictures WHERE rank IN (1, 3)")
            conn.commit()

    # Calling on sequence start
    response = client.get(f"/api/collections/{seq.id}/items?limit=2")

    assert response.status_code == 200
    clc = ItemCollection.from_dict(response.json)
    assert len(clc) == 2
    links = clc.extra_fields["links"]
    assert len(links) == 6

    assert clc[0].id == seq.pictures[1].id
    assert clc[1].id == seq.pictures[3].id

    assert {l["rel"]: l["href"] for l in clc.extra_fields["links"]} == {
        "root": "http://localhost/api/",
        "parent": f"http://localhost/api/collections/{seq.id}",
        "self": f"http://localhost/api/collections/{seq.id}/items?limit=2",
        "first": f"http://localhost/api/collections/{seq.id}/items?limit=2",
        "last": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=4",
        "next": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=4",
    }
    # Calling on the middle
    response = client.get(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=2")

    assert response.status_code == 200
    clc = ItemCollection.from_dict(response.json)
    assert len(clc) == 2
    links = clc.extra_fields["links"]
    assert len(links) == 6

    assert clc[0].id == seq.pictures[3].id
    assert clc[1].id == seq.pictures[4].id

    assert {l["rel"]: l["href"] for l in clc.extra_fields["links"]} == {
        "root": "http://localhost/api/",
        "parent": f"http://localhost/api/collections/{seq.id}",
        "self": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=2",
        "first": f"http://localhost/api/collections/{seq.id}/items?limit=2",
        "last": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=2",
        "prev": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=1",
    }


@conftest.SEQ_IMGS
def test_item(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqId, picId = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures WHERE rank = 1").fetchone()

            response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))

            assert response.status_code == 200
            data = response.json

            assert data["type"] == "Feature"
            assert data["geometry"]["type"] == "Point"
            assert len(str(data["id"])) > 0
            assert re.match(r"^2021-07-29T", data["properties"]["datetime"])
            assert data["properties"]["view:azimuth"] >= 0
            assert data["properties"]["view:azimuth"] <= 360
            assert re.match(
                r"^https?://.*/api/pictures/" + str(picId) + r"/tiled/\{TileCol\}_\{TileRow\}.jpg$",
                data["asset_templates"]["tiles"]["href"],
            )
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/hd.jpg$", data["assets"]["hd"]["href"])
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/sd.jpg$", data["assets"]["sd"]["href"])
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/thumb.jpg$", data["assets"]["thumb"]["href"])
            assert data["properties"]["tiles:tile_matrix_sets"]["geovisio"]["tileMatrix"][0]["tileWidth"] == 720
            assert data["properties"]["tiles:tile_matrix_sets"]["geovisio"]["tileMatrix"][0]["tileHeight"] == 720
            assert data["properties"]["tiles:tile_matrix_sets"]["geovisio"]["tileMatrix"][0]["matrixHeight"] == 4
            assert data["properties"]["tiles:tile_matrix_sets"]["geovisio"]["tileMatrix"][0]["matrixWidth"] == 8
            assert data["properties"]["pers:interior_orientation"]["camera_manufacturer"] == "GoPro"
            assert data["properties"]["pers:interior_orientation"]["camera_model"] == "Max"
            assert data["properties"]["pers:interior_orientation"]["field_of_view"] == 360
            assert data["properties"]["created"].startswith(date.today().isoformat())
            assert data["properties"]["geovisio:status"] == "ready"
            assert data["providers"] == [
                {"name": "Default account", "roles": ["producer"]},
            ]
            assert data["properties"]["geovisio:producer"] == "Default account"
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/hd.jpg$", data["properties"]["geovisio:image"])
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/thumb.jpg$", data["properties"]["geovisio:thumbnail"])

            item = Item.from_dict(data)
            assert len(item.links) == 5
            assert len([l for l in item.links if l.rel == "next"]) == 1

            # Make picture not available
            cursor.execute("UPDATE pictures SET status = 'hidden' WHERE id = %s", [picId])
            conn.commit()

            response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))
            assert response.status_code == 404


@conftest.SEQ_IMGS_FLAT
def test_item_flat(datafiles, initSequence, dburl):
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO cameras VALUES ('OLYMPUS IMAGING CORP. SP-720UZ', 6.16) ON CONFLICT DO NOTHING")
            conn.commit()

            client = initSequence(datafiles, preprocess=False)

            seqId, picId = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures WHERE rank = 1").fetchone()

            response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))
            data = response.json

            assert response.status_code == 200

            assert data["type"] == "Feature"
            assert data["geometry"]["type"] == "Point"
            assert len(str(data["id"])) > 0
            assert re.match(r"^2015-04-25T", data["properties"]["datetime"])
            assert data["properties"]["view:azimuth"] >= 0
            assert data["properties"]["view:azimuth"] <= 360
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/hd.jpg$", data["assets"]["hd"]["href"])
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/sd.jpg$", data["assets"]["sd"]["href"])
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/thumb.jpg$", data["assets"]["thumb"]["href"])
            assert "assert_templates" not in data
            assert "tiles:tile_matrix_sets" not in data["properties"]
            assert data["properties"]["pers:interior_orientation"]["camera_manufacturer"] == "OLYMPUS IMAGING CORP."
            assert data["properties"]["pers:interior_orientation"]["camera_model"] == "SP-720UZ"
            assert data["properties"]["pers:interior_orientation"]["field_of_view"] == 67
            assert data["properties"]["created"].startswith(date.today().isoformat())

            item = Item.from_dict(data)
            assert len(item.links) == 5
            assert len([l for l in item.links if l.rel == "next"]) == 1


@conftest.SEQ_IMG_FLAT
def test_item_flat_fov(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))
    data = response.json

    assert response.status_code == 200

    assert len(str(data["id"])) > 0
    assert data["properties"]["pers:interior_orientation"]["camera_manufacturer"] == "Canon"
    assert data["properties"]["pers:interior_orientation"]["camera_model"] == "EOS 6D0"
    assert "field_of_view" not in data["properties"]["pers:interior_orientation"]  # Not in cameras DB


@conftest.SEQ_IMG_FLAT
def test_item_missing_all_metadata(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqId, picId = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures WHERE rank = 1").fetchone()

            # Remove EXIF metadata from DB
            cursor.execute(
                "UPDATE pictures SET metadata = %s WHERE id = %s",
                [
                    '{"ts": 1430744932.0, "lat": 48.85779642035038, "lon": 2.3392783047650747, "type": "flat", "width": 4104, "height": 2736, "heading": 302}',
                    picId,
                ],
            )
            conn.commit()

            response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))
            data = response.json

            assert response.status_code == 200

            assert len(str(data["id"])) > 0
            assert len(data["properties"]["pers:interior_orientation"]) == 0


@conftest.SEQ_IMG_FLAT
@pytest.mark.parametrize(("status", "httpCode"), (("ready", 200), ("hidden", 404), ("preparing", 102), ("broken", 500)))
def test_item_status_httpcode(datafiles, initSequence, dburl, status, httpCode):
    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqId, picId = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures WHERE rank = 1").fetchone()

            # Remove EXIF metadata from DB
            cursor.execute("UPDATE pictures SET status = %s WHERE id = %s", [status, picId])
            conn.commit()

            response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))
            assert response.status_code == httpCode


@conftest.SEQ_IMG_FLAT
def test_item_missing_partial_metadata(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqId, picId = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures WHERE rank = 1").fetchone()

            # Remove EXIF metadata from DB
            cursor.execute(
                "UPDATE pictures SET metadata = %s WHERE id = %s",
                [
                    '{"ts": 1430744932.0, "lat": 48.85779642035038, "lon": 2.3392783047650747, "make": "Canon", "type": "flat", "width": 4104, "height": 2736, "heading": 302}',
                    picId,
                ],
            )
            conn.commit()

            response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))
            data = response.json

            assert response.status_code == 200

            assert len(str(data["id"])) > 0
            assert data["properties"]["pers:interior_orientation"] == {"camera_manufacturer": "Canon"}


intersectsGeojson1 = json.dumps(
    {
        "type": "Polygon",
        "coordinates": [
            [
                [1.9191969931125639, 49.00691313179996],
                [1.9191332906484602, 49.00689685694783],
                [1.9191691651940344, 49.00687024535389],
                [1.919211409986019, 49.006892018477274],
                [1.9191969931125639, 49.00691313179996],
            ]
        ],
    }
)
intersectsGeojson2 = json.dumps({"type": "Point", "coordinates": [1.919185442, 49.00688962]})


@pytest.mark.parametrize(
    ("limit", "bbox", "datetime", "intersects", "ids", "collections", "httpCode", "validRanks"),
    (
        (None, None, None, None, None, None, 200, [1, 2, 3, 4, 5]),
        (2, None, None, None, None, None, 200, None),
        (-1, None, None, None, None, None, 400, None),
        (99999, None, None, None, None, None, 400, None),
        ("bla", None, None, None, None, None, 400, None),
        (None, [0, 0, 1, 1], None, None, None, None, 200, []),
        (None, "[0,0,1,1", None, None, None, None, 200, []),
        (None, [1], None, None, None, None, 400, None),
        (None, [1.919185, 49.00688, 1.919187, 49.00690], None, None, None, None, 200, [1]),
        (None, None, "2021-07-29T11:16:54+02", None, None, None, 200, [1]),
        (None, None, "2021-07-29T00:00:00Z/..", None, None, None, 200, [1, 2, 3, 4, 5]),
        (None, None, "../2021-07-29T00:00:00Z", None, None, None, 200, []),
        (None, None, "2021-01-01T00:00:00Z/2021-07-29T11:16:58+02", None, None, None, 200, [1, 2, 3]),
        (None, None, "2021-01-01T00:00:00Z/", None, None, None, 400, None),
        (None, None, "/2021-01-01T00:00:00Z", None, None, None, 400, None),
        (None, None, "..", None, None, None, 400, None),
        (None, None, "2021-07-29TNOTATIME", None, None, None, 400, None),
        (None, None, None, intersectsGeojson1, None, None, 200, [1, 2]),
        (None, None, None, intersectsGeojson2, None, None, 200, [1]),
        (None, None, None, "{ 'broken': ''", None, None, 400, None),
        (None, None, None, "{ 'type': 'Feature' }", None, None, 400, None),
        (None, None, None, None, [1, 2], None, 200, [1, 2]),
        (None, None, None, None, None, "json1", 200, [1, 2, 3, 4, 5]),
        (None, None, None, None, None, "list1", 200, [1, 2, 3, 4, 5]),
        (None, None, None, None, None, "json2", 200, [1, 2, 3, 4, 5]),
        (None, None, None, None, None, "list2", 200, [1, 2, 3, 4, 5]),
    ),
)
@conftest.SEQ_IMGS
def test_search(datafiles, initSequence, dburl, limit, bbox, datetime, intersects, ids, collections, httpCode, validRanks):
    client = initSequence(datafiles, preprocess=False)

    # Transform input ranks into picture ID to pass to query
    if ids is not None and len(ids) > 0:
        with psycopg.connect(dburl) as conn:
            with conn.cursor() as cursor:
                ids = json.dumps(
                    cursor.execute(
                        "SELECT array_to_json(array_agg(pic_id::varchar)) FROM sequences_pictures WHERE rank = ANY(%s)", [ids]
                    ).fetchone()[0]
                )

    # Retrieve sequence ID to pass into collections in query
    if collections is not None:
        with psycopg.connect(dburl) as conn:
            with conn.cursor() as cursor:
                cid = cursor.execute("SELECT id::varchar FROM sequences").fetchone()[0]
                if collections.startswith("json"):
                    if collections == "json1":
                        collections = json.dumps([cid])
                    else:
                        collections = json.dumps([cid, cid])
                elif collections.startswith("list"):
                    if collections == "list1":
                        collections = cid
                    else:
                        collections = f"{cid},{cid}"

    query = {"limit": limit, "bbox": bbox, "datetime": datetime, "intersects": intersects, "ids": ids, "collections": collections}
    query = dict(filter(lambda val: val[1] is not None, query.items()))

    response = client.get("/api/search?" + urlencode(query))

    print(response.text)
    assert response.status_code == httpCode

    if httpCode == 200:
        clc = ItemCollection.from_dict(response.json)

        # all search response should have a link to the root of the stac catalog
        assert response.json["links"] == [
            {"rel": "root", "href": "http://localhost/api/", "title": "Instance catalog", "type": "application/json"}
        ]
        if validRanks is not None:
            assert len(clc) == len(validRanks)

            if len(validRanks) > 0:
                with psycopg.connect(dburl) as db:
                    validIds = db.execute(
                        "SELECT array_agg(pic_id ORDER BY rank) FROM sequences_pictures WHERE rank = ANY(%s)", [validRanks]
                    ).fetchone()[0]
                    allIds = db.execute("SELECT array_agg(pic_id ORDER BY rank) FROM sequences_pictures").fetchone()[0]
                    resIds = [UUID(item.id) for item in clc]
                    assert sorted(resIds) == sorted(validIds)

                    for i in range(len(validRanks)):
                        r = validRanks[i]
                        id = validIds[i]
                        links = [it.links for it in clc.items if it.id == str(id)][0]
                        if r == 1:
                            assert [l.target.split("/").pop() for l in links if l.rel == "next"] == [str(allIds[r])]
                            assert [l.target.split("/").pop() for l in links if l.rel == "prev"] == []
                        elif r == 5:
                            assert [l.target.split("/").pop() for l in links if l.rel == "next"] == []
                            assert [l.target.split("/").pop() for l in links if l.rel == "prev"] == [str(allIds[r - 2])]
                        else:
                            assert [l.target.split("/").pop() for l in links if l.rel == "next"] == [str(allIds[r])]
                            assert [l.target.split("/").pop() for l in links if l.rel == "prev"] == [str(allIds[r - 2])]

        elif limit is not None:
            assert len(clc) == limit


@conftest.SEQ_IMGS
def test_search_post(datafiles, initSequence):
    client = initSequence(datafiles, preprocess=False)

    response = client.post("/api/search", json={"limit": 1, "intersects": intersectsGeojson1})
    data = response.json

    assert response.status_code == 200
    clc = ItemCollection.from_dict(data)
    assert len(clc) == 1


@conftest.SEQ_IMGS
def test_search_post_list_params(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    ids = conftest.getFirstPictureIds(dburl)

    response = client.post("/api/search", json={"limit": 1, "collections": [ids[0]]})
    data = response.json

    assert response.status_code == 200
    clc = ItemCollection.from_dict(data)
    assert len(clc) == 1

    response = client.post("/api/search", json={"limit": 1, "ids": [ids[1]]})
    data = response.json

    assert response.status_code == 200
    clc = ItemCollection.from_dict(data)
    assert len(clc) == 1


def test_post_collection_nobody(client, dburl):
    response = client.post("/api/collections")

    assert response.status_code == 200
    assert response.headers.get("Location").startswith("http://localhost:5000/api/collections/")
    seqId = UUID(response.headers.get("Location").split("/").pop())
    assert seqId != ""

    # Check if JSON is a valid STAC collection
    assert response.json["type"] == "Collection"
    assert response.json["id"] == str(seqId)
    # the collection is associated to the default account since no auth was done
    assert response.json["providers"] == [{"name": "Default account", "roles": ["producer"]}]

    # Check if collection exists in DB
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqStatus = cursor.execute("SELECT status FROM sequences WHERE id = %s", [seqId]).fetchone()[0]
            assert seqStatus == "waiting-for-process"


@conftest.SEQ_IMGS
def test_search_hidden_pic(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    assert len(sequence.pictures) == 5

    # hide sequence
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "false"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200

    # searching the sequence should result in an empty set
    response = client.get(f'/api/search?collections=["{sequence.id}"]')
    assert response.status_code == 200, response
    assert len(response.json["features"]) == 0

    # searching the picture should result in an empty set
    for p in sequence.pictures:
        response = client.get(f'/api/search?ids=["{p.id}"]')
        assert response.status_code == 200
        assert len(response.json["features"]) == 0


@conftest.SEQ_IMGS
def test_search_hidden_pic_as_owner(datafiles, initSequenceApp, dburl, bobAccountToken):
    """
    Searching for hidden pic change if it's the owner that searches
    """
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    assert len(sequence.pictures) == 5

    # hide sequence
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "false"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200

    # searching the sequence as Bob should return all pictures
    response = client.get(f'/api/search?collections=["{sequence.id}"]', headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert response.status_code == 200
    assert len(response.json["features"]) == 5

    # searching the picture as Bob should also result in an empty set, event if it's the owner
    for p in sequence.pictures:
        response = client.get(f'/api/search?ids=["{p.id}"]', headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
        assert response.status_code == 200
        assert len(response.json["features"]) == 1


@conftest.SEQ_IMGS
def test_picture_next_hidden(datafiles, initSequenceApp, dburl, bobAccountToken):
    """
    if pic n°3 is hidden:
    * for anonymous call, the next link of pic n°2 should be pic n°4 and previous link of pic n°4 should be pic n°2
    * for the owner, the next link of pic n°2 should be pic n°3 and previous link of pic n°4 should be pic n°3
    """
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    assert len(sequence.pictures) == 5

    response = client.patch(
        f"/api/collections/{str(sequence.id)}/items/{sequence.pictures[2].id}",
        data={"visible": "false"},
        headers={"Authorization": f"Bearer {bobAccountToken(app)}"},
    )
    assert response.status_code == 200

    r = client.get(f"/api/collections/{sequence.id}/items/{sequence.pictures[2].id}")
    assert r.status_code == 404

    def _get_prev_link(r):
        return next(l for l in r.json["links"] if l["rel"] == "prev")

    def _get_next_link(r):
        return next(l for l in r.json["links"] if l["rel"] == "next")

    pic2 = client.get(f"/api/collections/{sequence.id}/items/{sequence.pictures[1].id}")
    assert pic2.status_code == 200
    next_link = _get_next_link(pic2)
    assert next_link["id"] == str(sequence.pictures[3].id)
    pic4 = client.get(f"/api/collections/{sequence.id}/items/{sequence.pictures[3].id}")
    assert pic4.status_code == 200
    prev_link = _get_prev_link(pic4)
    assert prev_link["id"] == str(sequence.pictures[1].id)

    # but calling this as the owner should return the right links
    pic2 = client.get(
        f"/api/collections/{sequence.id}/items/{sequence.pictures[1].id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert pic2.status_code == 200
    next_link = _get_next_link(pic2)
    assert next_link["id"] == str(sequence.pictures[2].id)
    pic4 = client.get(
        f"/api/collections/{sequence.id}/items/{sequence.pictures[3].id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert pic4.status_code == 200
    prev_link = _get_prev_link(pic4)
    assert prev_link["id"] == str(sequence.pictures[2].id)


@conftest.SEQ_IMGS
def test_patch_collection_contenttype(datafiles, initSequenceApp, dburl, bobAccountToken):
    """Setting an already visible sequence to visible is valid, and change nothing"""
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    # hide sequence
    p = client.patch(
        f"/api/collections/{sequence.id}",
        data={"visible": "false"},
        headers={"Content-Type": "multipart/form-data; whatever=blabla", "Authorization": f"Bearer {bobAccountToken(app)}"},
    )

    assert p.status_code == 200

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            newStatus = cursor.execute("SELECT status FROM sequences WHERE id = %s", [sequence.id]).fetchone()[0]
            assert newStatus == "hidden"


@conftest.SEQ_IMG_FLAT
def test_post_item_nobody(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    seqId, picId = conftest.getFirstPictureIds(dburl)
    response = client.post(f"/api/collections/{seqId}/items")
    assert response.status_code == 415


@pytest.mark.parametrize(
    ("filename", "position", "httpCode"),
    (
        ("1.jpg", 2, 202),
        ("1.jpg", 1, 409),
        (None, 2, 400),
        ("1.jpg", -1, 400),
        ("1.jpg", "bla", 400),
        ("1.txt", 2, 400),
    ),
)
@conftest.SEQ_IMG_FLAT
def test_post_item_body_formdata(datafiles, initSequence, dburl, filename, position, httpCode):
    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqId = cursor.execute("SELECT id FROM sequences LIMIT 1").fetchone()[0]

            # Make sequence marked as preparing
            cursor.execute("UPDATE sequences SET status='preparing' WHERE id = %s", [seqId])
            conn.commit()

            if filename is not None and filename != "1.jpg":
                os.mknod(datafiles / "seq1" / filename)

            origMetadata = None
            if filename == "1.jpg":
                origMetadata = reader.readPictureMetadata(Image.open(str(datafiles / "seq1" / filename)))
                assert len(origMetadata.exif) > 0

            response = client.post(
                f"/api/collections/{seqId}/items",
                headers={"Content-Type": "multipart/form-data"},
                data={"position": position, "picture": (datafiles / "seq1" / filename).open("rb") if filename is not None else None},
            )

            assert response.status_code == httpCode

            # Further testing if picture was accepted
            if httpCode == 202:
                assert response.headers.get("Location").startswith(f"http://localhost/api/collections/{seqId}/items/")
                picId = UUID(response.headers.get("Location").split("/").pop())
                assert str(picId) != ""

                # Check the returned JSON
                assert response.json["type"] == "Feature"
                assert response.json["id"] == str(picId)
                assert response.json["collection"] == str(seqId)
                # since the upload was not authenticated, the pictures are associated to the default account
                assert response.json["providers"] == [{"name": "Default account", "roles": ["producer"]}]

                # Check that picture has been correctly processed
                retries = 0
                while retries < 10 and retries != -1:
                    dbStatus = cursor.execute("SELECT status FROM pictures WHERE id = %s", [picId]).fetchone()[0]

                    if dbStatus == "ready":
                        retries = -1
                        laterResponse = client.get(f"/api/collections/{seqId}/items/{picId}")
                        assert laterResponse.status_code == 200

                        # Check file is available on filesystem
                        assert os.path.isfile(datafiles + "/permanent" + geovisio.utils.pictures.getHDPicturePath(picId))
                        assert not os.path.isdir(datafiles + "/permanent" + geovisio.utils.pictures.getPictureFolderPath(picId))

                        # Check sequence is marked as ready
                        seqStatus = cursor.execute("SELECT status FROM sequences WHERE id = %s", [seqId]).fetchone()
                        assert seqStatus and seqStatus[0] == "ready"

                        # Check picture has its metadata still stored
                        storedMetadata = reader.readPictureMetadata(
                            Image.open(str(datafiles + "/permanent" + geovisio.utils.pictures.getHDPicturePath(picId)))
                        )
                        assert str(storedMetadata) == str(origMetadata)

                    else:
                        retries += 1
                        time.sleep(2)

                if retries == 10:
                    raise Exception("Picture has never been processed")


@conftest.SEQ_IMGS_FLAT
def test_upload_pictures_with_external_ts(datafiles, client, dburl):
    # Create sequence
    resPostSeq = client.post("/api/collections")
    assert resPostSeq.status_code == 200
    seqId = resPostSeq.json["id"]

    external_ts = "2023-07-03T10:12:01.001Z"
    # Post an image, overloading it's datetime
    resPostImg1 = client.post(
        f"/api/collections/{seqId}/items",
        headers={"Content-Type": "multipart/form-data"},
        data={"position": 1, "picture": (datafiles / "b1.jpg").open("rb"), "override_capture_time": external_ts},
    )

    assert resPostImg1.status_code == 202

    # Check upload status
    conftest.waitForSequence(client, resPostSeq.headers["Location"])
    sequence = conftest.getPictureIds(dburl)[0]

    r = client.get(f"/api/collections/{seqId}/items")
    assert r.status_code == 200
    assert len(r.json["features"]) == 1
    # the picture should have the given datetime
    expected_date = "2023-07-03T10:12:01+00:00"
    assert r.json["features"][0]["properties"]["datetime"] == expected_date

    # we also check that the stored picture has the correct exif tags
    perm_pic = sequence.pictures[0].get_permanent_file(datafiles)
    tags = reader.readPictureMetadata(Image.open(perm_pic))
    assert datetime.fromtimestamp(tags.ts, tz=tz.UTC).isoformat() == expected_date


@pytest.mark.parametrize(
    ("date", "error"),
    (
        (
            "a bad date",
            {
                "message": "Parameter `override_capture_time` is not a valid datetime, it should be an iso formated datetime (like '2017-07-21T17:32:28Z').",
                "status_code": 400,
                "details": {"error": "Unknown string format: a bad date"},
            },
        ),
        (
            "",
            {
                "message": "Parameter `override_capture_time` is not a valid datetime, it should be an iso formated datetime (like '2017-07-21T17:32:28Z').",
                "status_code": 400,
                "details": {"error": "String does not contain a date: "},
            },
        ),
    ),
)
@conftest.SEQ_IMGS_FLAT
def test_upload_pictures_with_bad_external_ts(datafiles, client, date, error):
    """Test sending bad external datetime while uploading picutre, it should results in detailed errors"""
    resPostSeq = client.post("/api/collections")
    assert resPostSeq.status_code == 200
    r = client.post(
        f"/api/collections/{resPostSeq.json['id']}/items",
        headers={"Content-Type": "multipart/form-data"},
        data={"position": 1, "picture": (datafiles / "b1.jpg").open("rb"), "override_capture_time": date},
    )
    assert r.status_code == 400
    assert r.json == error


@conftest.SEQ_IMGS_FLAT
def test_upload_pictures_with_external_position(datafiles, client, dburl):
    # Create sequence
    resPostSeq = client.post("/api/collections")
    assert resPostSeq.status_code == 200
    seqId = resPostSeq.json["id"]

    lat = 42.42
    lon = 4.42
    # Post an image, overloading it's position
    resPostImg1 = client.post(
        f"/api/collections/{seqId}/items",
        headers={"Content-Type": "multipart/form-data"},
        data={"position": 1, "picture": (datafiles / "b1.jpg").open("rb"), "override_longitude": lon, "override_latitude": lat},
    )

    assert resPostImg1.status_code == 202

    # Check upload status
    conftest.waitForSequence(client, resPostSeq.headers["Location"])
    sequence = conftest.getPictureIds(dburl)[0]

    r = client.get(f"/api/collections/{seqId}/items")
    assert r.status_code == 200
    assert len(r.json["features"]) == 1
    # the picture should have the given position
    assert r.json["features"][0]["geometry"] == {"type": "Point", "coordinates": [lon, lat]}

    # we also check that the stored picture has the correct exif tags
    perm_pic = sequence.pictures[0].get_permanent_file(datafiles)
    tags = reader.readPictureMetadata(Image.open(perm_pic))
    assert math.isclose(tags.lat, lat)
    assert math.isclose(tags.lon, lon)


@pytest.mark.parametrize(
    ("lon", "lat", "error"),
    (
        (
            "43.12",
            None,
            {
                "message": "Longitude cannot be overridden alone, override_latitude also needs to be set",
                "status_code": 400,
            },
        ),
        (
            None,
            "43.12",
            {
                "message": "Latitude cannot be overridden alone, override_longitude also needs to be set",
                "status_code": 400,
            },
        ),
        (
            "pouet",
            "43.12",
            {
                "message": "For parameter `override_longitude`, `pouet` is not a valid longitude",
                "details": {"error": "could not convert string to float: 'pouet'"},
                "status_code": 400,
            },
        ),
        (
            "192.2",
            "43.12",
            {
                "message": "For parameter `override_longitude`, `192.2` is not a valid longitude",
                "details": {"error": "longitude needs to be between -180 and 180"},
                "status_code": 400,
            },
        ),
    ),
)
@conftest.SEQ_IMGS_FLAT
def test_upload_pictures_with_bad_external_position(datafiles, client, lon, lat, error):
    """Test sending bad external datetime while uploading picutre, it should results in detailed errors"""
    data = {"position": 1, "picture": (datafiles / "b1.jpg").open("rb")}
    if lon is not None:
        data["override_longitude"] = lon
    if lat is not None:
        data["override_latitude"] = lat
    resPostSeq = client.post("/api/collections")
    assert resPostSeq.status_code == 200
    r = client.post(
        f"/api/collections/{resPostSeq.json['id']}/items",
        headers={"Content-Type": "multipart/form-data"},
        data=data,
    )
    assert r.status_code == 400
    assert r.json == error


@pytest.mark.datafiles(os.path.join(conftest.FIXTURE_DIR, "e1_without_exif.jpg"))
def test_upload_pictures_without_exif_but_external_metadatas(datafiles, client, dburl):
    """Uploading pictures without metadatas shouldn't be a problem if the mandatory metadatas are provided by the API as external metadatas"""
    resPostSeq = client.post("/api/collections")
    assert resPostSeq.status_code == 200
    seqId = resPostSeq.json["id"]

    lat = 42.42
    lon = 4.42
    external_ts = "2023-07-03T10:12:01.001Z"
    resPostImg1 = client.post(
        f"/api/collections/{seqId}/items",
        headers={"Content-Type": "multipart/form-data"},
        data={
            "position": 1,
            "picture": (datafiles / "e1_without_exif.jpg").open("rb"),
            "override_longitude": lon,
            "override_latitude": lat,
            "override_capture_time": external_ts,
        },
    )

    assert resPostImg1.status_code == 202, resPostSeq.text

    # Check upload status
    conftest.waitForSequence(client, resPostSeq.headers["Location"])
    sequence = conftest.getPictureIds(dburl)[0]

    r = client.get(f"/api/collections/{seqId}/items")
    assert r.status_code == 200
    assert len(r.json["features"]) == 1
    # the picture should have the given position
    assert r.json["features"][0]["geometry"] == {"type": "Point", "coordinates": [lon, lat]}

    # we also check that the stored picture has the correct exif tags
    perm_pic = sequence.pictures[0].get_permanent_file(datafiles)
    tags = reader.readPictureMetadata(Image.open(perm_pic))
    assert math.isclose(tags.lat, lat)
    assert math.isclose(tags.lon, lon)
    expected_date = "2023-07-03T10:12:01+00:00"
    assert r.json["features"][0]["properties"]["datetime"] == expected_date


@pytest.mark.datafiles(os.path.join(conftest.FIXTURE_DIR, "e1_without_exif.jpg"))
def test_upload_pictures_without_complete_exif_but_external_metadatas(datafiles, client, dburl):
    """
    Uploading pictures should be an error if we don't find all mandatory metadata in the picture + it's external metadata

    There we upload a picture without exif metadata, and override only the timestamp, so we lack the coordinate
    """
    resPostSeq = client.post("/api/collections")
    assert resPostSeq.status_code == 200
    seqId = resPostSeq.json["id"]

    external_ts = "2023-07-03T10:12:01.001Z"
    resPostImg1 = client.post(
        f"/api/collections/{seqId}/items",
        headers={"Content-Type": "multipart/form-data"},
        data={
            "position": 1,
            "picture": (datafiles / "e1_without_exif.jpg").open("rb"),
            "override_capture_time": external_ts,  # only a timestamp
        },
    )

    assert resPostImg1.status_code == 400
    assert resPostImg1.json == {
        "details": {"error": "No GPS coordinates or broken coordinates in picture EXIF tags"},
        "message": "Impossible to parse picture metadata",
        "status_code": 400,
    }


@conftest.SEQ_IMGS_FLAT
def test_upload_on_unknown_sequence(datafiles, client, dburl):
    # add image on unexisting sequence
    resPostImg = client.post(
        "/api/collections/00000000-0000-0000-0000-000000000000/items",
        headers={"Content-Type": "multipart/form-data"},
        data={"position": 1, "picture": (datafiles / "b1.jpg").open("rb")},
    )

    assert resPostImg.status_code == 404
    assert resPostImg.json["message"] == "Sequence 00000000-0000-0000-0000-000000000000 wasn't found in database"


def mockBlurringAPIPostKO(requests_mock):
    """accessing the blurring api result in a connection timeout"""
    requests_mock.post(
        conftest.MOCK_BLUR_API + "/blur/",
        exc=requests.exceptions.ConnectTimeout,
    )


@conftest.SEQ_IMG
@conftest.SEQ_IMG_BLURRED
def test_upload_picture_skip_blurring(requests_mock, datafiles, tmp_path, dburl):
    """
    Inserting a picture which is already blurred should not call the KO Blur API, thus leading to no error
    """
    mockBlurringAPIPostKO(requests_mock)
    app = create_app(
        {
            "TESTING": True,
            "API_BLUR_URL": conftest.MOCK_BLUR_API,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND",
            "DB_URL": dburl,
            "FS_URL": str(tmp_path),
            "FS_TMP_URL": None,
            "FS_PERMANENT_URL": None,
            "FS_DERIVATES_URL": None,
        }
    )

    with app.app_context():
        with app.test_client() as client:
            seq_location = conftest.createSequence(client, "a_sequence")
            conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1, isBlurred=True)

            conftest.waitForSequence(client, seq_location)

            with psycopg.connect(dburl) as conn:
                with conn.cursor() as cursor:
                    blurred = cursor.execute(
                        "SELECT (metadata->>'blurredByAuthor')::boolean FROM pictures WHERE metadata->>'originalFileName' = '1.jpg'"
                    ).fetchone()
                    assert blurred and blurred[0] is True


def mockBlurringAPIPostOkay(requests_mock, datafiles):
    """Mock a working blur API call"""
    requests_mock.post(
        conftest.MOCK_BLUR_API + "/blur/",
        body=open(datafiles / "1_blurred.jpg", "rb"),
    )


@conftest.SEQ_IMG
@conftest.SEQ_IMG_BLURRED
def test_upload_picture_blurring_okay(requests_mock, datafiles, tmp_path, dburl):
    mockBlurringAPIPostOkay(requests_mock, datafiles)
    app = create_app(
        {
            "TESTING": True,
            "API_BLUR_URL": conftest.MOCK_BLUR_API,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND",
            "DB_URL": dburl,
            "FS_URL": str(tmp_path),
            "FS_TMP_URL": None,
            "FS_PERMANENT_URL": None,
            "FS_DERIVATES_URL": None,
        }
    )

    with app.app_context():
        with app.test_client() as client, psycopg.connect(dburl) as conn:
            with conn.cursor():
                seq_location = conftest.createSequence(client, "a_sequence")

                origMetadata = reader.readPictureMetadata(Image.open(str(datafiles / "1_blurred.jpg")))
                assert len(origMetadata.exif) > 0

                response = client.post(
                    f"{seq_location}/items",
                    headers={"Content-Type": "multipart/form-data"},
                    data={"position": 1, "picture": (datafiles / "1.jpg").open("rb")},
                )

                assert response.status_code == 202 and response.json

                assert response.headers["Location"].startswith(f"{seq_location}/items/")
                picId = UUID(response.headers["Location"].split("/").pop())
                assert str(picId) != ""

                # Check the returned JSON
                assert response.json["type"] == "Feature"
                assert response.json["id"] == str(picId)
                # since the upload was not authenticated, the pictures are associated to the default account
                assert response.json["providers"] == [{"name": "Default account", "roles": ["producer"]}]

                conftest.waitForSequence(client, seq_location)

                # Check that picture has been correctly processed
                laterResponse = client.get(f"{seq_location}/items/{picId}")
                assert laterResponse.status_code == 200

                # Check if picture sent to blur API is same as one from FS
                reqSize = int(requests_mock.request_history[0].headers["Content-Length"])
                picSize = os.path.getsize(datafiles / "1.jpg")
                assert reqSize <= picSize * 1.01

                # Check file is available on filesystem
                assert os.path.isfile(datafiles + "/permanent" + geovisio.utils.pictures.getHDPicturePath(picId))
                assert not os.path.isdir(datafiles + "/permanent" + geovisio.utils.pictures.getPictureFolderPath(picId))

                # Check picture has its metadata still stored
                storedMetadata = reader.readPictureMetadata(
                    Image.open(str(datafiles + "/permanent" + geovisio.utils.pictures.getHDPicturePath(picId)))
                )
                assert storedMetadata == origMetadata
                assert str(storedMetadata) == str(origMetadata)


@conftest.SEQ_IMG
@conftest.SEQ_IMG_BLURRED
def test_process_picture_with_pic_process_ko_1(requests_mock, datafiles, tmp_path, dburl):
    """
    Inserting a picture with the bluring api ko should result in the image having a broken status
    """
    mockBlurringAPIPostKO(requests_mock)
    app = create_app(
        {
            "TESTING": True,
            "API_BLUR_URL": conftest.MOCK_BLUR_API,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
            "DB_URL": dburl,
            "FS_URL": str(tmp_path),
            "FS_TMP_URL": None,
            "FS_PERMANENT_URL": None,
            "FS_DERIVATES_URL": None,
        }
    )

    with app.app_context():
        with app.test_client() as client:
            seq_location = conftest.createSequence(client, "a_sequence")
            conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1)

            def wanted_state(seq):
                pic_status = {p["rank"]: p["status"] for p in seq.json["items"]}
                return pic_status == {1: "broken"}

            conftest.waitForSequenceState(client, seq_location, wanted_state)

            s = client.get(f"{seq_location}/geovisio_status")

            assert s.json
            pic = s.json["items"][0]

            assert pic["status"] == "broken"
            assert pic["nb_errors"] == 1
            assert pic["processed_at"].startswith(date.today().isoformat())
            assert pic["process_error"] == "Blur API failure: ConnectTimeout"

            assert (
                s.json["status"] == "waiting-for-process"
            )  # since no pictures have been uploaded for the sequence, it's still in the 'waiting-for-processs' status


@conftest.SEQ_IMGS
@conftest.SEQ_IMG_BLURRED
def test_process_picture_with_pic_process_ko_2(datafiles, dburl, tmp_path, monkeypatch):
    """
    Inserting 2 pictures ('1.jpg' and '2.jpg'), and '1.jpg' cannot have its derivates generated should result in
    * '1.jpg' being in a 'broken' state
    * '2.jpg' being 'ready'
    * the sequence being 'ready'
    """
    from geovisio.workers import runner_pictures

    def new_processPictureFiles(db, dbPic, config):
        """Mock function that raises an exception for 1.jpg"""
        pic_name = db.execute("SELECT metadata->>'originalFileName' FROM pictures WHERE id = %s", [dbPic.id]).fetchone()[0]
        if pic_name == "1.jpg":
            raise Exception("oh no !")
        elif pic_name == "2.jpg":
            return  # all good
        raise Exception(f"picture {pic_name} not handled")

    with conftest.monkeypatched_function(runner_pictures, "processPictureFiles", new_processPictureFiles):
        app = create_app(
            {
                "TESTING": True,
                "API_BLUR_URL": conftest.MOCK_BLUR_API,
                "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
                "DB_URL": dburl,
                "FS_URL": str(tmp_path),
                "FS_TMP_URL": None,
                "FS_PERMANENT_URL": None,
                "FS_DERIVATES_URL": None,
            }
        )

        with app.app_context():
            with app.test_client() as client:
                seq_location = conftest.createSequence(client, "a_sequence")
                conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1)
                conftest.uploadPicture(client, seq_location, open(datafiles / "2.jpg", "rb"), "2.jpg", 2)

                import time

                time.sleep(1)

                s = client.get(f"{seq_location}/geovisio_status")
                assert s and s.status_code == 200 and s.json
                pic_status = {p["rank"]: p["status"] for p in s.json["items"]}

                assert pic_status == {1: "broken", 2: "ready"}
                assert s.json["status"] == "ready"


@conftest.SEQ_IMGS
@conftest.SEQ_IMG_BLURRED
def test_process_picture_with_last_picture_ko(datafiles, dburl, tmp_path, monkeypatch):
    """
    Inserting 3 pictures ('1.jpg', '2.jpg' and '3.jpg" ), and '3.jpg' cannot have its derivates generated should result in
    * '1.jpg' and '2.jpg' being in a 'ready' state
    * '3.jpg' being 'broken'
    * the sequence being 'ready', and with it's metadata generated (shapes for example)
    """
    from geovisio.workers import runner_pictures

    def new_processPictureFiles(db, dbPic, config):
        """Mock function that raises an exception for 1.jpg"""
        pic_name = db.execute("SELECT metadata->>'originalFileName' FROM pictures WHERE id = %s", [dbPic.id]).fetchone()[0]
        if pic_name in ("1.jpg", "2.jpg"):
            return  # all good
        elif pic_name == "3.jpg":
            raise Exception("oh no !")
        raise Exception(f"picture {pic_name} not handled")

    with conftest.monkeypatched_function(runner_pictures, "processPictureFiles", new_processPictureFiles):
        app = create_app(
            {
                "TESTING": True,
                "API_BLUR_URL": conftest.MOCK_BLUR_API,
                "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
                "DB_URL": dburl,
                "FS_URL": str(tmp_path),
                "FS_TMP_URL": None,
                "FS_PERMANENT_URL": None,
                "FS_DERIVATES_URL": None,
            }
        )

        with app.app_context():
            with app.test_client() as client:
                seq_location = conftest.createSequence(client, "a_sequence")
                conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1)
                conftest.uploadPicture(client, seq_location, open(datafiles / "2.jpg", "rb"), "2.jpg", 2)
                conftest.uploadPicture(client, seq_location, open(datafiles / "3.jpg", "rb"), "3.jpg", 3)

                def wanted_state(seq):
                    pic_status = {p["rank"]: p["status"] for p in seq.json["items"]}
                    return pic_status == {1: "ready", 2: "ready", 3: "broken"}

                conftest.waitForSequenceState(client, seq_location, wanted_state)
                seq = client.get(seq_location)
                assert seq.status_code == 200 and seq.json

                # the sequence should have been processed, and it's sequence computed
                assert seq.json["extent"]["spatial"]["bbox"] == [
                    [1.9191854417991367, 49.00688961988304, 1.9191963606027425, 49.00692625960235]
                ]


@conftest.SEQ_IMGS
@conftest.SEQ_IMG_BLURRED
def test_upload_picture_storage_ko(datafiles, dburl, tmp_path, monkeypatch):
    """
    Failing to save a picture in the storage should result in a 500 and no changes in the database
    """
    app = create_app(
        {
            "TESTING": True,
            "API_BLUR_URL": "",
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
            "DB_URL": dburl,
            "FS_URL": str(tmp_path),
            "FS_TMP_URL": None,
            "FS_PERMANENT_URL": None,
            "FS_DERIVATES_URL": None,
        }
    )

    class StorageException(Exception):
        pass

    with app.app_context():
        # files will be stored in permanent storage as there is no bluring
        permanent_storage = app.config["FILESYSTEMS"].permanent

        def new_writefile(*args, **kwargs):
            """Mock function that fails to store file"""
            raise StorageException("oh no !")

        with conftest.monkeypatched_function(permanent_storage, "writefile", new_writefile):
            with app.test_client() as client:
                seq_location = conftest.createSequence(client, "a_sequence")

                # with pytest.raises(StorageException):
                picture_response = client.post(
                    f"{seq_location}/items",
                    data={"position": 1, "picture": (open(datafiles / "1.jpg", "rb"), "1.jpg")},
                    content_type="multipart/form-data",
                )
                assert picture_response.status_code == 500

                # we post again the picture, now it should work, even with the same position
                picture_response = client.post(
                    f"{seq_location}/items",
                    data={"position": 1, "picture": (open(datafiles / "1.jpg", "rb"), "1.jpg")},
                    content_type="multipart/form-data",
                )
                assert picture_response.status_code == 500  # and not a 409, conflict

                # there should be nothing in the database
                with psycopg.connect(dburl) as conn:
                    with conn.cursor() as cursor:
                        nb_pic = cursor.execute("SELECT count(*) from pictures").fetchone()
                        assert nb_pic is not None and nb_pic[0] == 0
                        nb_pic_in_seq = cursor.execute("SELECT count(*) from sequences_pictures").fetchone()
                        assert nb_pic_in_seq is not None and nb_pic_in_seq[0] == 0


@pytest.mark.datafiles(os.path.join(conftest.FIXTURE_DIR, "invalid_exif.jpg"))
def test_upload_picture_invalid_metadata(datafiles, client):
    """
    Inserting a picture with invalid metada should result in a 400 error with details about why the picture has been rejected
    """

    seq_location = conftest.createSequence(client, "a_sequence")

    picture_response = client.post(
        f"{seq_location}/items",
        data={"position": 1, "picture": (open(datafiles / "invalid_exif.jpg", "rb"), "invalid_exif.jpg")},
        content_type="multipart/form-data",
    )

    assert picture_response.status_code == 400
    assert picture_response.json == {
        "details": {"error": "Broken GPS coordinates in picture EXIF tags"},
        "message": "Impossible to parse picture metadata",
        "status_code": 400,
    }


@conftest.SEQ_IMGS
def test_patch_item_noauth(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    itemRoute = "/api/collections/" + str(seqId) + "/items/" + str(picId)
    response = client.get(itemRoute)
    assert response.status_code == 200

    # Lacks authentication
    response = client.patch(itemRoute, data={"visible": "false"})
    assert response.status_code == 401


@conftest.SEQ_IMGS
def test_patch_item_authtoken(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    itemRoute = "/api/collections/" + str(seqId) + "/items/" + str(picId)
    response = client.get(itemRoute)
    assert response.status_code == 200

    # Prepare auth headers
    headers = {"Authorization": "Bearer " + bobAccountToken(app)}

    # Make picture not visible
    response = client.patch(itemRoute, data={"visible": "false"}, headers=headers)
    assert response.status_code == 200
    data = response.json
    assert data["id"] == str(picId)
    assert data["properties"]["geovisio:status"] == "hidden"

    # Try to retrieve hidden picture as public
    response = client.get(itemRoute)
    assert response.status_code == 404

    # we should also be able to see the picture from the /items route as bob
    all_pics_as_bob = client.get(f"/api/collections/{str(seqId)}/items", headers=headers)
    assert all_pics_as_bob.status_code == 200
    assert len(all_pics_as_bob.json["features"]) == 5
    assert all_pics_as_bob.json["features"][0]["id"] == str(picId)
    assert all_pics_as_bob.json["features"][0]["properties"]["geovisio:status"] == "hidden"
    for f in all_pics_as_bob.json["features"][1:]:
        assert f["properties"]["geovisio:status"] == "ready"

    # but an unauthentified call should see only 1 pic in the collection
    all_pics_unauthentified = client.get(f"/api/collections/{str(seqId)}/items")
    assert all_pics_unauthentified.status_code == 200
    assert len(all_pics_unauthentified.json["features"]) == 4
    assert picId not in [f["id"] for f in all_pics_unauthentified.json["features"]]
    for f in all_pics_unauthentified.json["features"]:
        assert f["properties"]["geovisio:status"] == "ready"

    # we should also be able to see the picture from the /items route as bob
    all_pics_as_bob = client.get(f"/api/collections/{str(seqId)}/items", headers=headers)
    assert all_pics_as_bob.status_code == 200
    assert len(all_pics_as_bob.json["features"]) == 5
    assert all_pics_as_bob.json["features"][0]["id"] == str(picId)
    assert all_pics_as_bob.json["features"][0]["properties"]["geovisio:status"] == "hidden"
    for f in all_pics_as_bob.json["features"][1:]:
        assert f["properties"]["geovisio:status"] == "ready"

    # but an unauthentified call should see only 1 pic in the collection
    all_pics_unauthentified = client.get(f"/api/collections/{str(seqId)}/items")
    assert all_pics_unauthentified.status_code == 200
    assert len(all_pics_unauthentified.json["features"]) == 4
    assert picId not in [f["id"] for f in all_pics_unauthentified.json["features"]]
    for f in all_pics_unauthentified.json["features"]:
        assert f["properties"]["geovisio:status"] == "ready"

    # Re-enable picture
    response = client.patch(itemRoute, data={"visible": "true"}, headers=headers)
    assert response.status_code == 200
    data = response.json
    assert data["id"] == str(picId)
    assert data["properties"]["geovisio:status"] == "ready"


@conftest.SEQ_IMGS
def test_patch_item_missing(datafiles, initSequenceApp, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    response = client.patch(
        "/api/collections/00000000-0000-0000-0000-000000000000/items/00000000-0000-0000-0000-000000000000",
        data={"visible": "false"},
        headers={"Authorization": "Bearer " + bobAccountToken(app)},
    )
    assert response.status_code == 404


@conftest.SEQ_IMGS
def test_patch_item_invalidVisible(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    itemRoute = "/api/collections/" + str(seqId) + "/items/" + str(picId)

    response = client.patch(itemRoute, data={"visible": "pouet"}, headers={"Authorization": "Bearer " + bobAccountToken(app)})

    assert response.status_code == 400
    assert response.json == {"message": "Picture visibility parameter (visible) should be either unset, true or false", "status_code": 400}


@conftest.SEQ_IMGS
def test_patch_item_nullvisibility(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    seqId, picId = conftest.getFirstPictureIds(dburl)
    itemRoute = "/api/collections/" + str(seqId) + "/items/" + str(picId)

    response = client.patch(itemRoute, data={}, headers={"Authorization": "Bearer " + bobAccountToken(app)})

    assert response.status_code == 200


@conftest.SEQ_IMGS
def test_patch_item_unchangedvisibility(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    seqId, picId = conftest.getFirstPictureIds(dburl)
    itemRoute = "/api/collections/" + str(seqId) + "/items/" + str(picId)

    response = client.patch(itemRoute, data={"visible": "true"}, headers={"Authorization": "Bearer " + bobAccountToken(app)})

    assert response.status_code == 200


@conftest.SEQ_IMGS
def test_patch_item_contenttype(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    seqId, picId = conftest.getFirstPictureIds(dburl)
    itemRoute = "/api/collections/" + str(seqId) + "/items/" + str(picId)

    response = client.patch(
        itemRoute,
        data={"visible": "false"},
        headers={"Content-Type": "multipart/form-data; whatever=blabla", "Authorization": "Bearer " + bobAccountToken(app)},
    )

    assert response.status_code == 200

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            newStatus = cursor.execute("SELECT status FROM pictures WHERE id = %s", [picId]).fetchone()
            assert newStatus and newStatus[0] == "hidden"


@conftest.SEQ_IMGS
def test_delete_picture_on_demand(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    first_pic_id = sequence.pictures[0].id

    # before the delte, we can query the first picture
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 200

    response = client.get(f"/api/collections/{sequence.id}/items")
    assert len(response.json["features"]) == 5
    assert first_pic_id in [f["id"] for f in response.json["features"]]

    assert os.path.exists(
        datafiles / "derivates" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8] / first_pic_id[9:]
    )
    assert os.path.exists(datafiles / "permanent" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8])

    response = client.delete(
        f"/api/collections/{sequence.id}/items/{first_pic_id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 204

    # The first picture should not be returned in any response
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 404

    response = client.get(f"/api/collections/{sequence.id}/items")
    assert len(response.json["features"]) == 4
    assert first_pic_id not in [f["id"] for f in response.json["features"]]

    # check that all files have correctly been deleted
    assert not os.path.exists(
        datafiles / "derivates" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8] / first_pic_id[9:]
    )
    assert not os.path.exists(datafiles / "permanent" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8])
    # there should be no empty directory
    for dirpath, dirname, files in itertools.chain(os.walk(datafiles / "permanent"), os.walk(datafiles / "derivates")):
        assert files or dirname, f"directory {dirpath} is empty"

    # requesting the picture now should result in a 404
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 404

    # and we should not see it anymore in the collection's item
    all_pics = client.get(f"/api/collections/{sequence.id}/items")
    assert all_pics.status_code == 200
    assert len(all_pics.json["features"]) == 4
    assert first_pic_id not in [f["id"] for f in all_pics.json["features"]]

    # same for deleting it again
    response = client.delete(
        f"/api/collections/{sequence.id}/items/{first_pic_id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 404


@conftest.SEQ_IMGS
def test_delete_picture_preprocess(datafiles, initSequenceApp, dburl, bobAccountToken):
    """Deleting a picture with the API configured as preprocess should work fine, and all derivates should be deleted"""
    client, app = initSequenceApp(datafiles, preprocess=True, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    first_pic_id = sequence.pictures[0].id

    # before the delte, we can query the first picture
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 200

    response = client.get(f"/api/collections/{sequence.id}/items")
    assert len(response.json["features"]) == 5
    assert first_pic_id in [f["id"] for f in response.json["features"]]

    assert os.path.exists(
        datafiles / "derivates" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8] / first_pic_id[9:]
    )
    assert os.path.exists(datafiles / "permanent" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8])

    response = client.delete(
        f"/api/collections/{sequence.id}/items/{first_pic_id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 204

    # The first picture should not be returned in any response
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 404

    response = client.get(f"/api/collections/{sequence.id}/items")
    assert len(response.json["features"]) == 4
    assert first_pic_id not in [f["id"] for f in response.json["features"]]

    # check that all files have correctly been deleted
    assert not os.path.exists(
        datafiles / "derivates" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8] / first_pic_id[9:]
    )
    assert not os.path.exists(datafiles / "permanent" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8])
    # there should be no empty directory
    for dirpath, dirname, files in itertools.chain(os.walk(datafiles / "permanent"), os.walk(datafiles / "derivates")):
        assert files or dirname, f"directory {dirpath} is empty"

    # requesting the picture now should result in a 404
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 404


@conftest.SEQ_IMGS
def test_delete_picture_no_auth(datafiles, initSequenceApp, dburl):
    """Deleting a picture wihout being identified is forbidden"""
    client, app = initSequenceApp(datafiles, preprocess=True, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    first_pic_id = sequence.pictures[0].id
    response = client.delete(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 401


@conftest.SEQ_IMGS
def test_delete_picture_as_another_user(datafiles, initSequenceApp, dburl, defaultAccountToken):
    """
    Deleting a not owned picture should be forbidden
    Here the pictures are owned by Bob and the default account tries to delete them
    """
    client, app = initSequenceApp(datafiles, preprocess=True, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    first_pic_id = sequence.pictures[0].id
    response = client.delete(
        f"/api/collections/{sequence.id}/items/{first_pic_id}", headers={"Authorization": f"Bearer {defaultAccountToken(app)}"}
    )
    assert response.status_code == 403


@conftest.SEQ_IMGS
def test_delete_picture_still_waiting_for_process(datafiles, tmp_path, initSequenceApp, dburl, bobAccountToken):
    """Deleting a picture that is still waiting to be processed should be fine (and the picture should be removed from the process queue)"""

    app = create_app(
        {
            "TESTING": True,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
            "DB_URL": dburl,
            "FS_URL": str(tmp_path),
            "SECRET_KEY": "a very secret key",
            "FS_TMP_URL": None,
            "FS_PERMANENT_URL": None,
            "FS_DERIVATES_URL": None,
            "PICTURE_PROCESS_THREADS_LIMIT": 0,  # we run the API without any picture worker, so no pictures will be processed
        }
    )

    with app.app_context():
        with app.test_client() as client, psycopg.connect(dburl) as conn:
            token = bobAccountToken(app)
            seq_location = conftest.createSequence(client, os.path.basename(datafiles), jwtToken=token)
            seq_id = seq_location.split("/")[-1]
            pic_id = conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1, jwtToken=token)

            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 1

            r = conn.execute("SELECT id, status FROM pictures").fetchall()
            assert r and list(r) == [(UUID(pic_id), "waiting-for-process")]

            assert os.path.exists(datafiles / "permanent" / pic_id[0:2] / pic_id[2:4] / pic_id[4:6] / pic_id[6:8])
            assert not os.path.exists(datafiles / "derivates" / pic_id[0:2] / pic_id[2:4] / pic_id[4:6] / pic_id[6:8] / pic_id[9:])

            response = client.delete(
                f"/api/collections/{seq_id}/items/{pic_id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
            )
            assert response.status_code == 204

            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 0

            r = conn.execute("SELECT count(*) FROM pictures").fetchone()
            assert r and r[0] == 0

            # pic should have been deleted too
            assert not os.path.exists(datafiles / "permanent" / pic_id[0:2] / pic_id[2:4] / pic_id[4:6] / pic_id[6:8])
