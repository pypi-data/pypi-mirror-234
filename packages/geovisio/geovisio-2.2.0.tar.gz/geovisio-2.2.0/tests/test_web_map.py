import os
import pytest
import mapbox_vector_tile

from geovisio.web import map
from . import conftest


FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@pytest.mark.parametrize(
    ("z", "x", "y", "format", "result"),
    (
        (6, 0, 0, "mvt", True),
        (6, 0, 1, "mvt", True),
        (6, 1, 0, "mvt", True),
        (6, 1, 1, "mvt", True),
        (-1, 0, 0, "mvt", 404),
        (16, 0, 0, "mvt", 404),
        (6, -1, 0, "mvt", 404),
        (6, 64, 0, "mvt", 404),
        (6, 0, -1, "mvt", 404),
        (6, 0, 64, "mvt", 404),
        (6, 0, 0, "jpg", 400),
        (None, 0, 0, "jpg", 400),
        (6, None, 0, "jpg", 400),
        (6, 0, None, "jpg", 400),
        (6, 0, 0, None, 400),
    ),
)
def test_isTileValid(z, x, y, format, result):
    if result is True:
        assert map.isTileValid(z, x, y, format) is True
    else:
        with pytest.raises(Exception) as e_info:
            map.isTileValid(z, x, y, format)
            assert e_info.status_code == result


@conftest.SEQ_IMGS
@pytest.mark.parametrize(
    ("z", "x", "y", "layersCount"),
    (
        (14, 8279, 5626, {"pictures": 5, "sequences": 1}),
        (11, 1034, 703, {"sequences": 1}),
        (11, 0, 0, {}),
        (6, 32, 21, {}),  # No sequences due to simplification
        (0, 0, 0, {}),  # No sequences due to simplification
    ),
)
def test_getTile(datafiles, initSequence, z, x, y, layersCount):
    client = initSequence(datafiles, preprocess=False)

    response = client.get(f"/api/map/{z}/{x}/{y}.mvt")

    assert response.status_code == 200
    data = mapbox_vector_tile.decode(response.get_data())

    for layerName, layerCount in layersCount.items():
        assert layerName in data
        assert len(data[layerName]["features"]) == layerCount
        # all pictures and sequence should be set as visible
        for f in data[layerName]["features"]:
            assert "hidden" not in f["properties"]  # if hidden is not in properties, it means it's visible
            # all pictures and sequence should have an accountId
            assert "account_id" in f["properties"]
            assert f["properties"].get("model") == "GoPro Max"
            assert f["properties"].get("type") == "equirectangular"

            if layerName == "sequences":
                assert f["properties"].get("date") == "2021-07-29"
            else:
                assert f["properties"].get("ts").startswith("2021-07-29")


def _get_prop_by_id(geoj):
    res = {}
    for t in ["pictures", "sequences"]:
        res[t] = {t["properties"]["id"]: t["properties"] for t in geoj.get(t, {}).get("features", [])}
    return res


@conftest.SEQ_IMGS
def test_getTile_hidden(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    def _get_tiles_features(asBob: bool):
        headers = {"Authorization": f"Bearer {bobAccountToken(app)}"} if asBob else {}
        response = client.get("/api/map/14/8279/5626.mvt", headers=headers)
        assert response.status_code == 200
        data = mapbox_vector_tile.decode(response.get_data())
        return data, {
            "nb_pic": len(data.get("pictures", {}).get("features", [])),
            "nb_seq": len(data.get("sequences", {}).get("features", [])),
        }

    assert _get_tiles_features(asBob=False)[1] == {"nb_pic": 5, "nb_seq": 1}

    # we hide a picture
    response = client.patch(
        f"/api/collections/{str(sequence.id)}/items/{str(sequence.pictures[0].id)}",
        data={"visible": "false"},
        headers={"Authorization": f"Bearer {bobAccountToken(app)}"},
    )
    assert response.status_code == 200

    assert _get_tiles_features(asBob=False)[1] == {"nb_pic": 4, "nb_seq": 1}
    # but the owner should see all pics
    t, stats = _get_tiles_features(asBob=True)
    assert stats == {"nb_pic": 5, "nb_seq": 1}
    all_props = _get_prop_by_id(t)
    assert all_props["pictures"][str(sequence.pictures[0].id)]["hidden"] is True
    for p in sequence.pictures[1:]:
        assert "hidden" not in all_props["pictures"][str(p.id)]

    # we hide the whole sequence
    response = client.patch(
        f"/api/collections/{str(sequence.id)}", data={"visible": "false"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200

    assert _get_tiles_features(asBob=False)[1] == {"nb_pic": 0, "nb_seq": 0}
    t, stats = _get_tiles_features(asBob=True)
    assert stats == {"nb_pic": 5, "nb_seq": 1}
    all_props = _get_prop_by_id(t)
    print(f"{all_props}")
    assert all_props["sequences"][str(sequence.id)]["hidden"] is True
    for p in sequence.pictures:
        assert all_props["pictures"][str(p.id)]["hidden"] is True

    # we unhide the sequence
    response = client.patch(
        f"/api/collections/{str(sequence.id)}", data={"visible": "true"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )

    assert _get_tiles_features(asBob=False)[1] == {"nb_pic": 4, "nb_seq": 1}
    t, stats = _get_tiles_features(asBob=True)
    assert stats == {"nb_pic": 5, "nb_seq": 1}
    all_props = _get_prop_by_id(t)
    assert "hidden" not in all_props["sequences"][str(sequence.id)]
    assert all_props["pictures"][str(sequence.pictures[0].id)]["hidden"] is True
    for p in sequence.pictures[1:]:
        assert "hidden" not in all_props["pictures"][str(p.id)]

    # we unhide the picture
    response = client.patch(
        f"/api/collections/{str(sequence.id)}/items/{str(sequence.pictures[0].id)}",
        data={"visible": "true"},
        headers={"Authorization": f"Bearer {bobAccountToken(app)}"},
    )
    assert _get_tiles_features(asBob=False)[1] == {"nb_pic": 5, "nb_seq": 1}
    assert _get_tiles_features(asBob=True)[1] == {"nb_pic": 5, "nb_seq": 1}
