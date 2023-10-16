from pystac import Collection
from dateutil.parser import parse as dateparser
import geovisio.web.collections
from geovisio.workers import runner_pictures
from tests import conftest
from tests.conftest import STAC_VERSION
import os
from pystac import Collection
from datetime import date, datetime
from uuid import UUID
from geovisio import create_app
from PIL import Image
import pytest
import time
import io
import psycopg


def test_dbSequenceToStacCollection(client):
    dbSeq = {
        "id": UUID("{12345678-1234-5678-1234-567812345678}"),
        "name": "Test sequence",
        "minx": -1.0,
        "maxx": 1.0,
        "miny": -2.0,
        "maxy": 2.0,
        "mints": datetime.fromisoformat("2020-01-01T12:50:37+00:00"),
        "maxts": datetime.fromisoformat("2020-01-01T13:30:42+00:00"),
        "inserted_at": datetime.fromisoformat("2023-01-01T12:42:00+02:00"),
        "updated_at": datetime.fromisoformat("2023-01-01T13:42:00+02:00"),
        "account_name": "Default account",
        "nbpic": 10,
    }

    res = geovisio.web.collections.dbSequenceToStacCollection(dbSeq)

    assert res
    assert res["type"] == "Collection"
    assert res["stac_version"] == STAC_VERSION
    assert res["id"] == "12345678-1234-5678-1234-567812345678"
    assert res["title"] == "Test sequence"
    assert res["description"] == "A sequence of geolocated pictures"
    assert res["providers"] == [
        {"name": "Default account", "roles": ["producer"]},
    ]
    assert res["keywords"] == ["pictures", "Test sequence"]
    assert res["license"] == "etalab-2.0"
    assert res["created"] == "2023-01-01T10:42:00+00:00"
    assert res["updated"] == "2023-01-01T11:42:00+00:00"
    assert res["extent"]["spatial"]["bbox"] == [[-1.0, -2.0, 1.0, 2.0]]
    assert res["extent"]["temporal"]["interval"] == [["2020-01-01T12:50:37+00:00", "2020-01-01T13:30:42+00:00"]]
    assert res["stats:items"]["count"] == 10
    assert len(res["links"]) == 5
    l = next(l for l in res["links"] if l["rel"] == "license")
    assert l["title"] == "License for this object (etalab-2.0)"
    assert l["href"] == "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE"


def test_dbSequenceToStacCollectionEmptyTemporalInterval(client):
    dbSeq = {
        "id": UUID("{12345678-1234-5678-1234-567812345678}"),
        "name": "Test sequence",
        "minx": -1.0,
        "maxx": 1.0,
        "miny": -2.0,
        "maxy": 2.0,
        "mints": None,
        "inserted_at": datetime.fromisoformat("2023-01-01T12:42:00+02:00"),
        "account_name": "Default account",
    }

    res = geovisio.web.collections.dbSequenceToStacCollection(dbSeq)

    assert res
    assert res["type"] == "Collection"
    assert res["stac_version"] == STAC_VERSION
    assert res["id"] == "12345678-1234-5678-1234-567812345678"
    assert res["title"] == "Test sequence"
    assert res["description"] == "A sequence of geolocated pictures"
    assert res["providers"] == [
        {"name": "Default account", "roles": ["producer"]},
    ]
    assert res["keywords"] == ["pictures", "Test sequence"]
    assert res["license"] == "etalab-2.0"
    assert res["created"] == "2023-01-01T10:42:00+00:00"
    assert res["extent"]["spatial"]["bbox"] == [[-1.0, -2.0, 1.0, 2.0]]
    assert res["extent"]["temporal"]["interval"] == [[None, None]]
    assert len(res["links"]) == 5


def test_dbSequenceToStacCollectionEmptyBbox(client):
    dbSeq = {
        "id": UUID("{12345678-1234-5678-1234-567812345678}"),
        "name": "Test sequence",
        "minx": None,
        "maxx": None,
        "miny": None,
        "maxy": None,
        "mints": datetime.fromisoformat("2020-01-01T12:50:37+00:00"),
        "maxts": datetime.fromisoformat("2020-01-01T13:30:42+00:00"),
        "inserted_at": datetime.fromisoformat("2023-01-01T12:42:00+02:00"),
        "account_name": "Default account",
    }

    res = geovisio.web.collections.dbSequenceToStacCollection(dbSeq)

    assert res
    assert res["type"] == "Collection"
    assert res["stac_version"] == STAC_VERSION
    assert res["id"] == "12345678-1234-5678-1234-567812345678"
    assert res["title"] == "Test sequence"
    assert res["description"] == "A sequence of geolocated pictures"
    assert res["providers"] == [
        {"name": "Default account", "roles": ["producer"]},
    ]
    assert res["keywords"] == ["pictures", "Test sequence"]
    assert res["license"] == "etalab-2.0"
    assert res["created"] == "2023-01-01T10:42:00+00:00"
    assert res["extent"]["spatial"]["bbox"] == [[-180.0, -90.0, 180.0, 90.0]]

    l = next(l for l in res["links"] if l["rel"] == "license")
    assert l["title"] == "License for this object (etalab-2.0)"
    assert l["href"] == "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE"


def test_dbSequenceToStacCollectionNoLicense(no_license_app_client):
    dbSeq = {
        "id": UUID("{12345678-1234-5678-1234-567812345678}"),
        "name": "Test sequence",
        "minx": -1.0,
        "maxx": 1.0,
        "miny": -2.0,
        "maxy": 2.0,
        "mints": datetime.fromisoformat("2020-01-01T12:50:37+00:00"),
        "maxts": datetime.fromisoformat("2020-01-01T13:30:42+00:00"),
        "inserted_at": datetime.fromisoformat("2023-01-01T12:42:00+02:00"),
        "updated_at": datetime.fromisoformat("2023-01-01T13:42:00+02:00"),
        "account_name": "Default account",
    }

    res = geovisio.web.collections.dbSequenceToStacCollection(dbSeq)

    assert res
    assert res["type"] == "Collection"
    assert res["stac_version"] == STAC_VERSION
    assert res["id"] == "12345678-1234-5678-1234-567812345678"
    assert res["title"] == "Test sequence"
    assert res["description"] == "A sequence of geolocated pictures"
    assert res["providers"] == [
        {"name": "Default account", "roles": ["producer"]},
    ]
    assert res["keywords"] == ["pictures", "Test sequence"]
    assert res["license"] == "proprietary"
    assert res["created"] == "2023-01-01T10:42:00+00:00"
    assert res["updated"] == "2023-01-01T11:42:00+00:00"
    assert res["extent"]["spatial"]["bbox"] == [[-1.0, -2.0, 1.0, 2.0]]
    assert res["extent"]["temporal"]["interval"] == [["2020-01-01T12:50:37+00:00", "2020-01-01T13:30:42+00:00"]]
    assert len(res["links"]) == 4
    rels = [l for l in res["links"] if l["rel"] == "license"]
    assert not rels


def test_collectionsEmpty(client):
    response = client.get("/api/collections")

    assert response.status_code == 200
    assert len(response.json["collections"]) == 0
    assert set((l["rel"] for l in response.json["links"])) == {"root", "parent", "self", "first"}


@conftest.SEQ_IMGS
def test_collections(datafiles, initSequence):
    client = initSequence(datafiles, preprocess=False)

    response = client.get("/api/collections")
    data = response.json

    assert response.status_code == 200

    assert len(data["collections"]) == 1
    assert len(data["links"]) == 5

    assert data["links"][0]["rel"] == "root"
    assert data["links"][0]["href"].endswith("/api/")
    assert data["links"][1]["rel"] == "parent"
    assert data["links"][1]["href"].endswith("/api/")
    assert data["links"][2]["rel"] == "self"
    assert data["links"][2]["href"].endswith("/api/collections")
    assert data["links"][3]["rel"] == "first"
    assert data["links"][3]["href"] == "http://localhost/api/collections?limit=100"
    assert data["links"][4]["rel"] == "last"
    assert "http://localhost/api/collections?limit=100&created_before=" in data["links"][4]["href"]

    Collection.from_dict(data["collections"][0])

    assert data["collections"][0]["type"] == "Collection"
    assert data["collections"][0]["stac_version"] == STAC_VERSION
    assert len(data["collections"][0]["id"]) > 0
    assert len(data["collections"][0]["title"]) > 0
    assert data["collections"][0]["description"] == "A sequence of geolocated pictures"
    assert len(data["collections"][0]["keywords"]) > 0
    assert len(data["collections"][0]["license"]) > 0
    assert len(data["collections"][0]["extent"]["spatial"]["bbox"][0]) == 4
    assert len(data["collections"][0]["extent"]["temporal"]["interval"][0]) == 2
    assert len(data["collections"][0]["links"]) == 4
    assert data["collections"][0]["created"].startswith(date.today().isoformat())
    assert data["collections"][0]["stats:items"]["count"] == 5


@conftest.SEQ_IMGS
def test_collections_rss(datafiles, initSequence):
    client = initSequence(datafiles, preprocess=False)

    # With query string
    response = client.get("/api/collections", query_string={"format": "rss"})
    assert response.status_code == 200
    assert response.data.startswith(b"""<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" """)

    # With Accept header
    response = client.get("/api/collections", headers={"Accept": "application/rss+xml"})
    assert response.status_code == 200
    assert response.data.startswith(b"""<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" """)


@conftest.SEQ_IMGS
def test_collections_pagination_classic(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    conftest.createManySequences(dburl)

    # Launch all calls against API
    nextLink = "/api/collections?limit=50"
    receivedLinks = []
    receivedSeqIds = []

    while nextLink:
        response = client.get(nextLink)
        assert response.status_code == 200

        myLinks = {l["rel"]: l["href"] for l in response.json["links"]}

        receivedLinks.append(myLinks)
        nextLink = myLinks.get("next")

        for c in response.json["collections"]:
            receivedSeqIds.append(c["id"])

    # Check received links
    for i, links in enumerate(receivedLinks):
        assert "root" in links
        assert "parent" in links
        assert "self" in links
        assert "/api/collections?limit=50" in links["self"]
        assert links["first"] == "http://localhost/api/collections?limit=50"
        assert "last" in links

        if i == 0:
            assert "next" in links
            assert "prev" not in links
        elif i == len(receivedLinks) - 1:
            assert "next" not in links
            assert "prev" in links
        else:
            assert "next" in links
            assert "prev" in links
            prevLinks = receivedLinks[i - 1]
            prevLinks["next"] = links["self"]
            prevLinks["self"] = links["prev"]
            nextLinks = receivedLinks[i + 1]
            links["next"] = nextLinks["self"]
            links["self"] = nextLinks["prev"]

    # Check received sequence IDS
    assert len(receivedSeqIds) == 1024
    assert len(set(receivedSeqIds)) == 1024


@conftest.SEQ_IMGS
def test_collections_pagination_descending(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    conftest.createManySequences(dburl)

    # Call collections endpoint to get last page
    response = client.get("/api/collections?limit=50")
    assert response.status_code == 200

    lastLink = next((l for l in response.json["links"] if l["rel"] == "last"))

    # Launch all calls against API
    prevLink = lastLink["href"]
    receivedLinks = []
    receivedSeqIds = []

    while prevLink:
        response = client.get(prevLink)
        assert response.status_code == 200

        myLinks = {l["rel"]: l["href"] for l in response.json["links"]}

        receivedLinks.append(myLinks)
        prevLink = myLinks.get("prev")

        for c in response.json["collections"]:
            receivedSeqIds.append(c["id"])

    # Check received links
    for i, links in enumerate(receivedLinks):
        assert "root" in links
        assert "parent" in links
        assert "self" in links
        assert "/api/collections?limit=50" in links["self"]
        assert "first" in links
        assert links["first"].endswith("/api/collections?limit=50")
        assert "last" in links

        if i == 0:
            assert "next" not in links
            assert "prev" in links
        elif i == len(receivedLinks) - 1:
            assert "next" in links
            assert "prev" not in links
        else:
            assert "next" in links
            assert "prev" in links
            prevLinks = receivedLinks[i + 1]
            prevLinks["next"] = links["self"]
            prevLinks["self"] = links["prev"]
            nextLinks = receivedLinks[i - 1]
            links["next"] = nextLinks["self"]
            links["self"] = nextLinks["prev"]

    # Check received sequence IDS
    assert len(receivedSeqIds) == 1024
    assert len(set(receivedSeqIds)) == 1024


@conftest.SEQ_IMGS
def test_collections_pagination_outalimit(datafiles, initSequence):
    client = initSequence(datafiles, preprocess=False)

    response = client.get("/api/collections?limit=50&created_after=2100-01-01T10:00:00Z")
    assert response.status_code == 400
    assert response.json == {"message": "There is no collection created after 2100-01-01 10:00:00+00:00", "status_code": 400}

    response = client.get("/api/collections?limit=50&created_before=2000-01-01T10:00:00Z")
    assert response.status_code == 400
    assert response.json == {"message": "There is no collection created before 2000-01-01 10:00:00+00:00", "status_code": 400}

    response = client.get("/api/collections?limit=-1")
    assert response.status_code == 400
    assert response.json == {"message": "limit parameter should be an integer between 1 and 1000", "status_code": 400}

    response = client.get("/api/collections?limit=1001")
    assert response.status_code == 400
    assert response.json == {"message": "limit parameter should be an integer between 1 and 1000", "status_code": 400}


@conftest.SEQ_IMGS
def test_collections_created_date_filtering(datafiles, initSequence, dburl):
    from dateutil.tz import UTC

    client = initSequence(datafiles, preprocess=False)
    conftest.createManySequences(dburl)

    def get_creation_date(response):
        return sorted(dateparser(r["created"]) for r in response.json["collections"])

    response = client.get("/api/collections?limit=10")
    assert response.status_code == 200
    initial_creation_date = get_creation_date(response)
    last_date = initial_creation_date[-1]

    def compare_query(query, date, after):
        response = client.get(query)
        assert response.status_code == 200
        creation_dates = get_creation_date(response)
        assert creation_dates
        if after:
            assert all([d > date for d in creation_dates])
        else:
            assert all([d < date for d in creation_dates])

    compare_query(
        f"/api/collections?limit=10&created_after={last_date.strftime('%Y-%m-%dT%H:%M:%S')}", last_date.replace(microsecond=0), after=True
    )
    # date without hour should be ok
    compare_query(
        f"/api/collections?limit=10&created_after={last_date.strftime('%Y-%m-%d')}",
        datetime.combine(last_date.date(), last_date.min.time(), tzinfo=UTC),
        after=True,
    )
    compare_query(
        f"/api/collections?limit=10&created_after={last_date.strftime('%Y-%m-%dT%H:%M:%SZ')}", last_date.replace(microsecond=0), after=True
    )
    # isoformated date should work
    compare_query(
        f"/api/collections?limit=10&created_after={last_date.strftime('%Y-%m-%dT%H:%M:%S')}%2B00:00",
        last_date.replace(microsecond=0),
        after=True,
    )

    # same filters should work with the `created_before` parameter
    compare_query(
        f"/api/collections?limit=10&created_before={last_date.strftime('%Y-%m-%dT%H:%M:%S')}", last_date.replace(microsecond=0), after=False
    )
    compare_query(
        f"/api/collections?limit=10&created_before={last_date.strftime('%Y-%m-%d')}",
        datetime.combine(last_date.date(), last_date.min.time(), tzinfo=UTC),
        after=False,
    )
    compare_query(
        f"/api/collections?limit=10&created_before={last_date.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        last_date.replace(microsecond=0),
        after=False,
    )
    compare_query(
        f"/api/collections?limit=10&created_before={last_date.strftime('%Y-%m-%dT%H:%M:%S')}%2B00:00",
        last_date.replace(microsecond=0),
        after=False,
    )

    # We can also filter by both created_before and created_after
    mid_date = initial_creation_date[int(len(initial_creation_date) / 2)]
    response = client.get(
        f"/api/collections?limit=10&created_before={last_date.strftime('%Y-%m-%dT%H:%M:%SZ')}&created_after={mid_date.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    )
    assert response.status_code == 200
    creation_dates = get_creation_date(response)
    assert creation_dates
    assert all([d > mid_date.replace(microsecond=0) and d < last_date for d in creation_dates])


@conftest.SEQ_IMGS
def test_collections_invalid_created_after(datafiles, initSequence):
    client = initSequence(datafiles, preprocess=False)

    response = client.get("/api/collections?limit=50&created_after=pouet")
    assert response.status_code == 400
    assert response.json == {
        "details": {"error": "Unknown string format: pouet"},
        "message": "Invalid `created_after` argument",
        "status_code": 400,
    }


@conftest.SEQ_IMGS
def test_collections_hidden(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)

    seqId, picId = conftest.getFirstPictureIds(dburl)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE sequences SET status = 'hidden'")
            conn.commit()

    response = client.get("/api/collections")
    assert response.status_code == 200
    assert len(response.json["collections"]) == 0


@conftest.SEQ_IMGS
def test_collections_bbox(datafiles, initSequence):
    client = initSequence(datafiles, preprocess=False)

    response = client.get("/api/collections?bbox=0,0,1,1")
    print(response.text)
    assert response.status_code == 200
    assert len(response.json["collections"]) == 0

    response = client.get("/api/collections?bbox=1.312864,48.004817,3.370054,49.357521")
    assert response.status_code == 200
    assert len(response.json["collections"]) == 1


@conftest.SEQ_IMGS
def test_collections_datetime(datafiles, initSequence):
    client = initSequence(datafiles, preprocess=False)

    response = client.get("/api/collections?datetime=../2021-01-01")
    print(response.text)
    assert response.status_code == 200
    assert len(response.json["collections"]) == 0

    response = client.get("/api/collections?datetime=2021-01-01/..")
    assert response.status_code == 200
    assert len(response.json["collections"]) == 1

    # Note that sequences are filtered by day, not time
    #   due to computed_capture_date field in sequences table
    response = client.get("/api/collections?datetime=2021-07-29T09:00:00Z/2021-07-29T10:00:00Z")
    assert response.status_code == 200
    assert len(response.json["collections"]) == 1


def test_collectionMissing(client):
    response = client.get("/api/collections/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@conftest.SEQ_IMGS
def test_collectionById(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)

    seqId, picId = conftest.getFirstPictureIds(dburl)

    response = client.get("/api/collections/" + str(seqId))
    data = response.json

    assert response.status_code == 200
    clc = Collection.from_dict(data)
    assert clc.extra_fields["stats:items"]["count"] == 5


@conftest.SEQ_IMGS
def test_get_hidden_sequence(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    assert len(sequence.pictures) == 5

    # hide sequence
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "false"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200
    assert response.json["geovisio:status"] == "hidden"

    # status should be set to hidden in db
    with psycopg.connect(dburl) as conn, conn.cursor() as cursor:
        seqStatus = cursor.execute("SELECT status FROM sequences WHERE id = %s", [sequence.id]).fetchone()
        assert seqStatus
        assert seqStatus[0] == "hidden"

    # The sequence is hidden, public call cannot see it, only Bob
    r = client.get(f"/api/collections/{sequence.id}")
    assert r.status_code == 404
    r = client.get(f"/api/collections/{sequence.id}/items")
    assert r.status_code == 404

    # same for the list of items in the collection
    r = client.get(f"/api/collections/{sequence.id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert r.status_code == 200
    r = client.get(f"/api/collections/{sequence.id}/items", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert r.status_code == 200
    assert len(r.json["features"]) == 5

    for p in sequence.pictures:
        r = client.get(f"/api/collections/{sequence.id}/items/{p.id}")
        assert r.status_code == 404

        r = client.get(f"/api/collections/{sequence.id}/items/{p.id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
        assert r.status_code == 200

    # other sequence's routes are also unavailable for public access
    r = client.get(f"/api/collections/{sequence.id}/geovisio_status")
    assert r.status_code == 404
    r = client.get(f"/api/collections/{sequence.id}/geovisio_status", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert r.status_code == 200

    # if we set the sequence back to public, it should be fine for everybody
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "true"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200

    assert client.get(f"/api/collections/{sequence.id}").status_code == 200
    for p in sequence.pictures:
        assert client.get(f"/api/collections/{sequence.id}/items/{p.id}").status_code == 200


@conftest.SEQ_IMGS
def test_get_hidden_sequence_and_pictures(datafiles, initSequenceApp, dburl, bobAccountToken):
    """
    If we:
            * hide the pictures n°1
            * hide the sequence
            * un-hide the sequence

    The pictures n°1 should stay hidden
    """
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    assert len(sequence.pictures) == 5

    # hide pic
    response = client.patch(
        f"/api/collections/{sequence.id}/items/{sequence.pictures[0].id}",
        data={"visible": "false"},
        headers={"Authorization": f"Bearer {bobAccountToken(app)}"},
    )

    r = client.get(f"/api/collections/{sequence.id}/items/{sequence.pictures[0].id}")
    assert r.status_code == 404

    # hide sequence
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "false"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200

    r = client.get(f"/api/collections/{sequence.id}")
    assert r.status_code == 404

    # set the sequence to visible
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "true"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200
    r = client.get(f"/api/collections/{sequence.id}")
    assert r.status_code == 200

    # but the pic is still hidden
    r = client.get(f"/api/collections/{sequence.id}/items/{sequence.pictures[0].id}")
    assert r.status_code == 404


@conftest.SEQ_IMGS
def test_invalid_sequence_hide(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    # hide pic
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "invalid_value"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 400


@conftest.SEQ_IMGS
def test_hide_unexisting_seq(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, withBob=True)

    response = client.patch(
        "/api/collections/00000000-0000-0000-0000-000000000000",
        data={"visible": "false"},
        headers={"Authorization": f"Bearer {bobAccountToken(app)}"},
    )
    assert response.status_code == 404
    assert response.json == {"message": "Sequence 00000000-0000-0000-0000-000000000000 wasn't found in database", "status_code": 404}


@conftest.SEQ_IMGS
def test_empty_sequence_patch(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    response = client.patch(
        f"/api/collections/{sequence.id}/items/{sequence.pictures[0].id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    # changing no value is valid, and should result if the same thing as a get
    assert response.status_code == 200


@conftest.SEQ_IMGS
def test_anomynous_sequence_patch(datafiles, initSequenceApp, dburl):
    """Patching a sequence as an unauthentified user should result in an error"""
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    response = client.patch(
        f"/api/collections/{sequence.id}",
    )
    assert response.status_code == 401
    assert response.json == {"message": "Authentication is mandatory"}


@conftest.SEQ_IMGS
def test_set_already_visible_sequence(datafiles, initSequenceApp, dburl, bobAccountToken):
    """Setting an already visible sequence to visible is valid, and change nothing"""
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    # hide sequence
    p = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "true"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert p.status_code == 200
    r = client.get(f"/api/collections/{sequence.id}")
    assert r.status_code == 200


@conftest.SEQ_IMGS
def test_not_owned_sequence_patch(datafiles, initSequenceApp, dburl, defaultAccountToken):
    """Patching a sequence that does not belong to us should result in an error"""
    client, app = initSequenceApp(datafiles, withBob=True)  # the sequence belongs to Bob
    sequence = conftest.getPictureIds(dburl)[0]

    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "true"}, headers={"Authorization": f"Bearer {defaultAccountToken(app)}"}
    )
    assert response.status_code == 403


def test_post_collection_body_form(client):
    response = client.post("/api/collections", data={"title": "Séquence"})

    assert response.status_code == 200
    assert response.headers.get("Location").startswith("http://localhost:5000/api/collections/")
    seqId = UUID(response.headers.get("Location").split("/").pop())
    assert seqId != ""

    # Check if JSON is a valid STAC collection
    assert response.json["type"] == "Collection"
    assert response.json["id"] == str(seqId)
    assert response.json["title"] == "Séquence"


def test_post_collection_body_json(client):
    response = client.post("/api/collections", json={"title": "Séquence"})

    assert response.status_code == 200
    assert response.headers.get("Location").startswith("http://localhost:5000/api/collections/")
    seqId = UUID(response.headers.get("Location").split("/").pop())
    assert seqId != ""

    # Check if JSON is a valid STAC collection
    assert response.json["type"] == "Collection"
    assert response.json["id"] == str(seqId)
    assert response.json["title"] == "Séquence"


def test_getCollectionImportStatus_noseq(client):
    response = client.get("/api/collections/00000000-0000-0000-0000-000000000000/geovisio_status")
    assert response.status_code == 404


@conftest.SEQ_IMGS_FLAT
def test_getCollectionImportStatus_ready(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    response = client.get(f"/api/collections/{seqId}/geovisio_status")

    assert response.status_code == 200
    assert len(response.json["items"]) == 2

    for i in response.json["items"]:
        assert len(i) == 6
        assert UUID(i["id"]) is not None
        assert i["rank"] > 0
        assert i["status"] == "ready"
        assert i["processed_at"].startswith(date.today().isoformat())
        assert i["nb_errors"] == 0
        assert i["process_error"] is None


@conftest.SEQ_IMGS_FLAT
def test_getCollectionImportStatus_hidden(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE pictures SET status = 'hidden' WHERE id = %s", [picId])
            conn.commit()

            response = client.get(f"/api/collections/{seqId}/geovisio_status")

            assert response.status_code == 200
            assert len(response.json["items"]) == 1
            assert response.json["items"][0]["id"] != picId
            assert response.json["items"][0]["status"] == "ready"


@conftest.SEQ_IMGS_FLAT
def test_upload_sequence(datafiles, client, dburl):
    # Create sequence
    resPostSeq = client.post("/api/collections")
    assert resPostSeq.status_code == 200
    seqId = resPostSeq.json["id"]
    seqLocation = resPostSeq.headers["Location"]

    # add the cameras into the db to be able to have field_of_view
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO cameras VALUES ('OLYMPUS IMAGING CORP. SP-720UZ', 6.16) ON CONFLICT DO NOTHING")
            conn.commit()
    # Create first image
    resPostImg1 = client.post(
        f"/api/collections/{seqId}/items",
        headers={"Content-Type": "multipart/form-data"},
        data={"position": 1, "picture": (datafiles / "b1.jpg").open("rb")},
    )

    assert resPostImg1.status_code == 202

    # Create second image
    resPostImg2 = client.post(
        f"/api/collections/{seqId}/items",
        headers={"Content-Type": "multipart/form-data"},
        data={"position": 2, "picture": (datafiles / "b2.jpg").open("rb")},
    )

    assert resPostImg2.status_code == 202

    # Check upload status
    conftest.waitForSequence(client, seqLocation)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            dbSeq = cursor.execute("SELECT status, geom FROM sequences where id = %s", [seqId]).fetchone()
            assert dbSeq
            # Check sequence is ready
            assert dbSeq[0] == "ready"
            # the sequence geometry should have been computed too
            assert dbSeq[1] is not None

    resGetSeq = client.get(f"/api/collections/{seqId}")
    assert resGetSeq.status_code == 200

    # the sequence should have some metadata computed
    seq = resGetSeq.json

    assert seq["extent"]["spatial"] == {"bbox": [[-1.9499731060073981, 48.13939279199841, -1.9491245819090675, 48.139852239480945]]}
    assert seq["extent"]["temporal"]["interval"] == [["2015-04-25T15:36:17+00:00", "2015-04-25T15:37:48+00:00"]]

    # 2 pictures should be in the collections
    r = client.get(f"/api/collections/{seqId}/items")
    assert r.status_code == 200

    assert len(r.json["features"]) == 2
    # both pictures should be ready
    assert r.json["features"][0]["properties"]["geovisio:status"] == "ready"
    assert r.json["features"][1]["properties"]["geovisio:status"] == "ready"

    # the pictures should have the original filename and size as metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            blurred = cursor.execute("SELECT id, metadata FROM pictures").fetchall()
            assert blurred and len(blurred) == 2
            blurred = {str(p[0]): p[1] for p in blurred}
            assert os.path.getsize(datafiles / "b1.jpg") == blurred[resPostImg1.json["id"]]["originalFileSize"]
            assert blurred[resPostImg1.json["id"]] == {
                "make": "OLYMPUS IMAGING CORP.",
                "type": "flat",
                "model": "SP-720UZ",
                "width": 4288,
                "height": 3216,
                "focal_length": 4.66,
                "field_of_view": 67,
                "blurredByAuthor": False,
                "originalFileName": "b1.jpg",
                "originalFileSize": 2731046,
                "crop": None,
            }
            assert os.path.getsize(datafiles / "b2.jpg") == blurred[resPostImg2.json["id"]]["originalFileSize"]
            assert blurred[resPostImg2.json["id"]] == {
                "make": "OLYMPUS IMAGING CORP.",
                "type": "flat",
                "model": "SP-720UZ",
                "width": 4288,
                "height": 3216,
                "focal_length": 4.66,
                "field_of_view": 67,
                "blurredByAuthor": False,
                "originalFileName": "b2.jpg",
                "originalFileSize": 2896575,
                "crop": None,
            }


@pytest.fixture()
def removeDefaultAccount(dburl):
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            accountID = cursor.execute("UPDATE accounts SET is_default = false WHERE is_default = true RETURNING id").fetchone()
            assert accountID

            conn.commit()
            yield
            # put back the account at the end of the test
            cursor.execute("UPDATE accounts SET is_default = true WHERE id = %s", [accountID[0]])


def test_upload_sequence_noDefaultAccount(client, dburl, removeDefaultAccount):
    resPostSeq = client.post("/api/collections")
    assert resPostSeq.status_code == 500
    assert resPostSeq.json == {"message": "No default account defined, please contact your instance administrator", "status_code": 500}


@conftest.SEQ_IMGS
def test_get_collection_thumbnail(datafiles, initSequenceApp, dburl):
    client, _ = initSequenceApp(datafiles)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    response = client.get(f"/api/collections/{str(seqId)}/thumb.jpg")
    assert response.status_code == 200
    assert response.content_type == "image/jpeg"
    img = Image.open(io.BytesIO(response.get_data()))
    assert img.size == (500, 300)

    first_pic_thumb = client.get(f"/api/pictures/{str(picId)}/thumb.jpg")
    assert first_pic_thumb.data == response.data


@conftest.SEQ_IMGS
def test_get_collection_thumbnail_first_pic_hidden(datafiles, initSequenceApp, dburl, bobAccountToken, defaultAccountToken):
    """ "
    If the first pic is hidden, the owner of the sequence should still be able to see it as the thumbnail,
    but all other users should see another pic as the thumbnail
    """
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    # change the first pic visibility
    response = client.patch(
        f"/api/collections/{sequence.id}/items/{sequence.pictures[0].id}",
        data={"visible": "false"},
        headers={"Authorization": f"Bearer {bobAccountToken(app)}"},
    )
    assert response.status_code == 200

    response = client.get(f"/api/collections/{sequence.id}/thumb.jpg")
    assert response.status_code == 200
    assert response.content_type == "image/jpeg"
    img = Image.open(io.BytesIO(response.get_data()))
    assert img.size == (500, 300)

    # non logged users should not see the same picture
    first_pic_thumb = client.get(f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg")
    assert first_pic_thumb.status_code == 403  # this picture should not be visible to the other users

    second_pic_thumb = client.get(f"/api/pictures/{str(sequence.pictures[1].id)}/thumb.jpg")
    assert second_pic_thumb.status_code == 200  # the second picture is not hidden and should be visible and be the thumbnail
    assert response.data == second_pic_thumb.data

    # same thing for a logged user that is not the owner
    first_pic_thumb = client.get(
        f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg", headers={"Authorization": f"Bearer {defaultAccountToken(app)}"}
    )
    assert first_pic_thumb.status_code == 403

    second_pic_thumb = client.get(
        f"/api/pictures/{str(sequence.pictures[1].id)}/thumb.jpg", headers={"Authorization": f"Bearer {defaultAccountToken(app)}"}
    )
    assert second_pic_thumb.status_code == 200
    assert response.data == second_pic_thumb.data

    owner_thumbnail = client.get(f"/api/collections/{sequence.id}/thumb.jpg", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert owner_thumbnail.status_code == 200
    assert owner_thumbnail.content_type == "image/jpeg"
    owner_first_pic_thumbnail = client.get(
        f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert owner_first_pic_thumbnail.status_code == 200
    assert owner_thumbnail.data == owner_first_pic_thumbnail.data  # the owner should see the first pic


@conftest.SEQ_IMGS
def test_get_collection_thumbnail_all_pics_hidden(datafiles, initSequenceApp, dburl, bobAccountToken, defaultAccountToken):
    """ "
    If the all pics are hidden, the owner of the sequence should still be able to see a the thumbnail,
    but all other users should not have any thumbnails
    """
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    # change the first pic visibility
    for p in sequence.pictures:
        response = client.patch(
            f"/api/collections/{sequence.id}/items/{str(p.id)}",
            data={"visible": "false"},
            headers={"Authorization": f"Bearer {bobAccountToken(app)}"},
        )
        assert response.status_code == 200

    # non logged users should not see a thumbnail
    response = client.get(f"/api/collections/{sequence.id}/thumb.jpg")
    assert response.status_code == 404

    for p in sequence.pictures:
        # the pictures should not be visible to the any other users, logged or not
        # specific hidden pictures will result on 403, not 404
        first_pic_thumb = client.get(f"/api/pictures/{str(p.id)}/thumb.jpg")
        assert first_pic_thumb.status_code == 403
        first_pic_thumb = client.get(
            f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg", headers={"Authorization": f"Bearer {defaultAccountToken(app)}"}
        )
        assert first_pic_thumb.status_code == 403

    # but the owner should see it
    owner_thumbnail = client.get(f"/api/collections/{sequence.id}/thumb.jpg", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert owner_thumbnail.status_code == 200
    assert owner_thumbnail.content_type == "image/jpeg"
    owner_first_pic_thumbnail = client.get(
        f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert owner_first_pic_thumbnail.status_code == 200
    assert owner_thumbnail.data == owner_first_pic_thumbnail.data  # the owner should see the first pic


@conftest.SEQ_IMGS
def test_get_collection_thumbnail_sequence_hidden(datafiles, initSequenceApp, dburl, bobAccountToken, defaultAccountToken):
    """ "
    If the sequence is hidden, the owner of the sequence should still be able to see a the thumbnail,
    but all other users should not have any thumbnails
    """
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    # change the sequence visibility
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "false"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200

    # non logged users should not see a thumbnail
    response = client.get(f"/api/collections/{sequence.id}/thumb.jpg")
    assert response.status_code == 404

    for p in sequence.pictures:
        # the pictures should not be visible to the any other users, logged or not
        # specific hidden pictures will result on 403, not 404
        first_pic_thumb = client.get(f"/api/pictures/{str(p.id)}/thumb.jpg")
        assert first_pic_thumb.status_code == 403
        first_pic_thumb = client.get(
            f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg", headers={"Authorization": f"Bearer {defaultAccountToken(app)}"}
        )
        assert first_pic_thumb.status_code == 403

    # but the owner should see it
    owner_thumbnail = client.get(f"/api/collections/{sequence.id}/thumb.jpg", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert owner_thumbnail.status_code == 200
    assert owner_thumbnail.content_type == "image/jpeg"
    owner_first_pic_thumbnail = client.get(
        f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert owner_first_pic_thumbnail.status_code == 200
    assert owner_thumbnail.data == owner_first_pic_thumbnail.data  # the owner should see the first pic


def _wait_for_pics_deletion(pics_id, dburl):
    with psycopg.connect(dburl) as conn:
        waiting_time = 0.1
        total_time = 0
        nb_pics = 0
        while total_time < 10:
            nb_pics = conn.execute("SELECT count(*) FROM pictures WHERE id = ANY(%(pics)s)", {"pics": pics_id}).fetchone()

            # we wait for the collection and all its pictures to be ready
            if nb_pics and not nb_pics[0]:
                return
            time.sleep(waiting_time)
            total_time += waiting_time
        assert False, f"All pictures not deleted ({nb_pics} remaining)"


@conftest.SEQ_IMGS
def test_delete_sequence(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    first_pic_id = sequence.pictures[0].id

    # before the delete, we can query the seq
    response = client.get(f"/api/collections/{sequence.id}")
    assert response.status_code == 200

    response = client.get(f"/api/collections/{sequence.id}/items")
    assert len(response.json["features"]) == 5
    assert first_pic_id in [f["id"] for f in response.json["features"]]

    assert os.path.exists(
        datafiles / "derivates" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8] / first_pic_id[9:]
    )
    assert os.path.exists(datafiles / "permanent" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8])

    response = client.delete(f"/api/collections/{sequence.id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert response.status_code == 204

    # The sequence or its pictures should not be returned in any response
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 404

    response = client.get(f"/api/collections/{sequence.id}")
    assert response.status_code == 404

    with psycopg.connect(dburl) as conn:
        seq = conn.execute("SELECT * FROM sequences WHERE id = %s", [sequence.id]).fetchone()
        assert not seq

        pic_status = conn.execute(
            "SELECT distinct(status) FROM pictures WHERE id = ANY(%(pics)s)", {"pics": [p.id for p in sequence.pictures]}
        ).fetchall()

        # pics are either already deleted or waiting deleting
        assert pic_status == [] or pic_status == [("waiting-for-delete",)]

    # async job should delete at one point all the pictures
    _wait_for_pics_deletion(pics_id=[p.id for p in sequence.pictures], dburl=dburl)

    # check that all files have correctly been deleted since it was the only sequence
    assert os.listdir(datafiles / "derivates") == []
    assert os.listdir(datafiles / "permanent") == []


@conftest.SEQ_IMGS
@conftest.SEQ_IMGS_FLAT
def test_delete_1_sequence_over_2(datafiles, initSequenceApp, dburl, bobAccountToken):
    """2 sequences available, and delete of them, we should not mess with the other sequence"""
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)
    assert len(sequence) == 2

    # before the delete, we can query both seq
    for seq in sequence:
        response = client.get(f"/api/collections/{seq.id}")
        assert response.status_code == 200

        response = client.get(f"/api/collections/{seq.id}/items")
        assert response.status_code == 200

    for s in sequence:
        for p in s.pictures:
            assert os.path.exists(p.get_derivate_dir(datafiles))
            assert os.path.exists(p.get_permanent_file(datafiles))

    # we delete the first sequence
    response = client.delete(f"/api/collections/{sequence[0].id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert response.status_code == 204

    # The sequence or its pictures should not be returned in any response
    response = client.get(f"/api/collections/{sequence[0].id}/items/{sequence[0].pictures[0].id}")
    assert response.status_code == 404

    response = client.get(f"/api/collections/{sequence[0].id}")
    assert response.status_code == 404

    # everything is still fine for the other sequence
    assert client.get(f"/api/collections/{sequence[1].id}/items/{sequence[1].pictures[0].id}").status_code == 200
    assert client.get(f"/api/collections/{sequence[1].id}").status_code == 200

    with psycopg.connect(dburl) as conn:
        seq = conn.execute("SELECT * FROM sequences WHERE id = %s", [sequence[0].id]).fetchone()
        assert not seq

        pic_status = conn.execute(
            "SELECT distinct(status) FROM pictures WHERE id = ANY(%(pics)s)", {"pics": [p.id for p in sequence[0].pictures]}
        ).fetchall()

        # pics are either already deleted or waiting deleting
        assert pic_status == [] or pic_status == [("waiting-for-delete",)]

    # async job should delete at one point all the pictures
    _wait_for_pics_deletion(pics_id=[p.id for p in sequence[0].pictures], dburl=dburl)

    for p in sequence[0].pictures:
        assert not os.path.exists(p.get_derivate_dir(datafiles))
        assert not os.path.exists(p.get_permanent_file(datafiles))
    for p in sequence[1].pictures:
        assert os.path.exists(p.get_derivate_dir(datafiles))
        assert os.path.exists(p.get_permanent_file(datafiles))


@conftest.SEQ_IMGS
def test_delete_sequence_no_auth(datafiles, initSequenceApp, dburl):
    """A sequence cannot be deleted with authentication"""
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)
    response = client.delete(f"/api/collections/{sequence[0].id}")
    assert response.status_code == 401
    assert response.json == {"message": "Authentication is mandatory"}


@conftest.SEQ_IMGS
def test_delete_sequence_not_owned(datafiles, initSequenceApp, dburl, defaultAccountToken):
    """A sequence cannot be deleted with authentication"""
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)
    response = client.delete(f"/api/collections/{sequence[0].id}", headers={"Authorization": f"Bearer {defaultAccountToken(app)}"})
    assert response.status_code == 403
    assert response.json == {"message": "You're not authorized to edit this sequence", "status_code": 403}


@conftest.SEQ_IMGS
def test_delete_sequence_with_pic_still_waiting_for_process(datafiles, tmp_path, initSequenceApp, dburl, bobAccountToken):
    """Deleting a sequence with pictures that are still waiting to be processed should be fine (and the picture should be removed from the process queue)"""
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

    with app.app_context(), app.test_client() as client, psycopg.connect(dburl) as conn:
        token = bobAccountToken(app)
        seq_location = conftest.createSequence(client, os.path.basename(datafiles), jwtToken=token)
        pic_id = conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1, jwtToken=token)
        sequence = conftest.getPictureIds(dburl)[0]

        r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
        assert r and r[0] == 1

        r = conn.execute("SELECT id, status FROM pictures").fetchall()
        assert r and list(r) == [(UUID(pic_id), "waiting-for-process")]

        assert not os.path.exists(sequence.pictures[0].get_derivate_dir(datafiles))
        assert os.path.exists(sequence.pictures[0].get_permanent_file(datafiles))

        response = client.delete(f"/api/collections/{sequence.id}", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 204

        # since there are no background worker, the deletion is not happening, but the picture should be marked for deletion
        r = conn.execute("SELECT picture_id, task FROM pictures_to_process").fetchall()
        assert r and r == [(UUID(pic_id), "delete")]

        r = conn.execute("SELECT count(*) FROM pictures").fetchone()
        assert r and r[0] == 1

        # pic should not have been deleted, since we background worker is there
        assert os.path.exists(sequence.pictures[0].get_permanent_file(datafiles))

        # we start the runner picture as a separate process
        import multiprocessing

        def process():
            with app.app_context():
                w = runner_pictures.PictureProcessor(config=app.config, stop=False)
                w.process_next_pictures()

        p = multiprocessing.Process(target=process)
        p.start()
        p.join(timeout=3)  # wait 3 seconds before killing the process
        if p.is_alive():
            p.terminate()
        r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
        assert r and r[0] == 0
        r = conn.execute("SELECT count(*) FROM pictures").fetchone()
        assert r and r[0] == 0

        assert not os.path.exists(sequence.pictures[0].get_permanent_file(datafiles))
        assert not os.path.exists(sequence.pictures[0].get_derivate_dir(datafiles))


@conftest.SEQ_IMGS
def test_user_collection(datafiles, initSequence, defaultAccountID):
    client = initSequence(datafiles, preprocess=False)

    # Get user ID
    response = client.get(f"/api/users/{defaultAccountID}/collection")
    data = response.json
    userName = "Default account"
    assert response.status_code == 200
    assert data["type"] == "Collection"
    ctl = Collection.from_dict(data)
    assert len(ctl.links) > 0
    assert ctl.title == userName + "'s sequences"
    assert ctl.id == f"user:{defaultAccountID}"
    assert ctl.description == "List of all sequences of user " + userName
    assert ctl.extent.spatial.to_dict() == {"bbox": [[1.9191854417991367, 49.00688961988304, 1.919199780601944, 49.00697341759938]]}
    assert ctl.extent.temporal.to_dict() == {"interval": [["2021-07-29T09:16:54Z", "2021-07-29T09:17:02Z"]]}
    assert ctl.get_links("self")[0].get_absolute_href() == f"http://localhost/api/users/{defaultAccountID}/collection"

    assert ctl.extra_fields["stats:items"]["count"] == 5
    assert data["providers"] == [{"name": "Default account", "roles": ["producer"]}]
    assert ctl.stac_extensions == [
        "https://stac-extensions.github.io/stats/v0.2.0/schema.json",
        "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json",
    ]

    # both `updated` and `created` should be valid date
    dateparser(data["updated"])
    dateparser(data["created"])
    assert data["created"].startswith(date.today().isoformat())
    assert data["updated"].startswith(date.today().isoformat())

    # Check links
    childs = ctl.get_links("child")
    assert len(childs) == 1
    child = childs[0]
    assert child.title is not None
    assert child.extra_fields["id"] is not None
    assert child.get_absolute_href() == "http://localhost/api/collections/" + child.extra_fields["id"]
    assert child.extra_fields["extent"]["temporal"] == {"interval": [["2021-07-29T09:16:54+00:00", "2021-07-29T09:17:02+00:00"]]}
    assert child.extra_fields["extent"]["spatial"] == {
        "bbox": [[1.9191854417991367, 49.00688961988304, 1.919199780601944, 49.00697341759938]]
    }
    assert child.extra_fields["stats:items"]["count"] == 5
    # each collection also have an updated/created date
    assert child.extra_fields["updated"].startswith(date.today().isoformat())
    assert child.extra_fields["created"].startswith(date.today().isoformat())
