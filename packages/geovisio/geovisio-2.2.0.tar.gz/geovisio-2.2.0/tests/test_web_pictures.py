import pytest
import psycopg
import io
from PIL import Image
from . import conftest


@conftest.SEQ_IMGS
def test_getPictureHD(datafiles, initSequence, dburl):
    client = initSequence(datafiles)

    # Retrieve loaded sequence metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]

            assert len(str(picId)) > 0

            # Call on WebP
            response = client.get("/api/pictures/" + str(picId) + "/hd.webp")
            assert response.status_code == 200
            assert response.content_type == "image/webp"

            # Call on JPEG
            response = client.get("/api/pictures/" + str(picId) + "/hd.jpg")
            assert response.status_code == 200
            assert response.content_type == "image/jpeg"

            # Call on invalid format
            response = client.get("/api/pictures/" + str(picId) + "/hd.gif")
            assert response.status_code == 404

            # Call on unexisting picture
            response = client.get("/api/pictures/ffffffff-ffff-ffff-ffff-ffffffffffff/hd.webp")
            assert response.status_code == 404

            # Call on hidden picture
            cursor.execute("UPDATE pictures SET status = 'hidden' WHERE id = %s", [picId])
            conn.commit()
            response = client.get("/api/pictures/" + str(picId) + "/hd.webp")
            assert response.status_code == 403


@pytest.mark.skipci
@conftest.SEQ_IMG
@conftest.SEQ_IMG_BLURRED
def test_getPictureHD_blurred(requests_mock, datafiles, initSequenceApp, dburl):
    conftest.mockBlurringAPIPost(datafiles, requests_mock)
    client, app = initSequenceApp(datafiles, blur=True)

    # Retrieve loaded sequence metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]

            assert len(str(picId)) > 0

            # Call on WebP
            response = client.get("/api/pictures/" + str(picId) + "/hd.webp")
            assert response.status_code == 200
            assert response.content_type == "image/webp"

            # Call on JPEG
            response = client.get("/api/pictures/" + str(picId) + "/hd.jpg")
            assert response.status_code == 200
            assert response.content_type == "image/jpeg"


@conftest.SEQ_IMGS
def test_getPictureSD(datafiles, initSequence, dburl):
    client = initSequence(datafiles)

    # Retrieve loaded sequence metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]

            assert len(str(picId)) > 0

            # Call on WebP
            response = client.get("/api/pictures/" + str(picId) + "/sd.webp")
            assert response.status_code == 200
            assert response.content_type == "image/webp"

            # Call on JPEG
            response = client.get("/api/pictures/" + str(picId) + "/sd.jpg")
            assert response.status_code == 200
            assert response.content_type == "image/jpeg"

            img = Image.open(io.BytesIO(response.get_data()))
            w, h = img.size
            assert w == 2048

            # Call API on unexisting picture
            response = client.get("/api/pictures/ffffffff-ffff-ffff-ffff-ffffffffffff/sd.jpg")
            assert response.status_code == 404

            # Call API on hidden picture
            cursor.execute("UPDATE pictures SET status = 'hidden' WHERE id = %s", [picId])
            conn.commit()
            response = client.get("/api/pictures/" + str(picId) + "/sd.jpg")
            assert response.status_code == 403


@conftest.SEQ_IMGS
def test_getPictureThumb(datafiles, initSequence, dburl):
    client = initSequence(datafiles)

    # Retrieve loaded sequence metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]

            assert len(str(picId)) > 0

            # Call on WebP
            response = client.get("/api/pictures/" + str(picId) + "/thumb.webp")
            assert response.status_code == 200
            assert response.content_type == "image/webp"

            # Call on JPEG
            response = client.get("/api/pictures/" + str(picId) + "/thumb.jpg")
            assert response.status_code == 200
            assert response.content_type == "image/jpeg"

            img = Image.open(io.BytesIO(response.get_data()))
            w, h = img.size
            assert w == 500
            assert h == 300

            # Call API on unexisting picture
            response = client.get("/api/pictures/ffffffff-ffff-ffff-ffff-ffffffffffff/thumb.webp")
            assert response.status_code == 404

            # Call API on hidden picture
            cursor.execute("UPDATE pictures SET status = 'hidden' WHERE id = %s", [picId])
            conn.commit()
            response = client.get("/api/pictures/" + str(picId) + "/thumb.webp")
            assert response.status_code == 403


def test_getPictureTiledEmpty(tmp_path, client):
    # Call API on unexisting picture
    response = client.get("/api/pictures/00000000-0000-0000-0000-000000000000/tiled/0_0.jpg")
    assert response.status_code == 404


@pytest.mark.parametrize(
    ("col", "row", "httpCode", "picStatus", "format"),
    (
        (0, 0, 200, "ready", "webp"),
        (0, 0, 200, "ready", "jpeg"),
        (7, 3, 200, "ready", "jpeg"),
        (8, 4, 404, "ready", "jpeg"),
        (-1, -1, 404, "ready", "jpeg"),
        (0, 0, 403, "hidden", "jpeg"),
    ),
)
@conftest.SEQ_IMGS
def test_getPictureTiled(datafiles, initSequence, dburl, col, row, httpCode, picStatus, format):
    client = initSequence(datafiles)

    # Retrieve loaded sequence metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]

            assert len(str(picId)) > 0

            seqId = cursor.execute("SELECT id FROM sequences LIMIT 1").fetchone()[0]

            assert len(str(seqId)) > 0

            if picStatus != "ready":
                cursor.execute("UPDATE pictures SET status = %s WHERE id = %s", (picStatus, picId))
                conn.commit()

            # Call on WebP
            response = client.get(
                "/api/pictures/" + str(picId) + "/tiled/" + str(col) + "_" + str(row) + "." + ("jpg" if format == "jpeg" else format)
            )
            assert response.status_code == httpCode

            if httpCode == 200:
                assert response.content_type == "image/" + format

                diskImg = Image.open(
                    str(datafiles)
                    + "/derivates/"
                    + str(picId)[0:2]
                    + "/"
                    + str(picId)[2:4]
                    + "/"
                    + str(picId)[4:6]
                    + "/"
                    + str(picId)[6:8]
                    + "/"
                    + str(picId)[9:]
                    + "/tiles/"
                    + str(col)
                    + "_"
                    + str(row)
                    + ".jpg"
                )
                apiImg = Image.open(io.BytesIO(response.get_data()))

                assert conftest.arePicturesSimilar(diskImg, apiImg, limit=2)


@conftest.SEQ_IMGS_FLAT
def test_getPictureTiled_flat(datafiles, initSequence, tmp_path, dburl):
    client = initSequence(datafiles)

    # Prepare sequence
    with psycopg.connect(dburl) as db:
        # Get picture ID
        picId = db.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]
        assert len(str(picId)) > 0

        # Check tiles API call
        response = client.get("/api/pictures/" + str(picId) + "/tiled/0_0.webp")
        assert response.status_code == 404
