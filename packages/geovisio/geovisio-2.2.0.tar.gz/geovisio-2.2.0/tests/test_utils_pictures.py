import math
import psycopg
from geovisio import utils
from geovisio.utils import filesystems
from tests import conftest
from geovisio.utils import sequences
from psycopg.rows import dict_row
from .conftest import FIXTURE_DIR, MOCK_BLUR_API, mockBlurringAPIPost
import pytest
from PIL import Image
from fs import open_fs
import os


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "1.jpg"),
    os.path.join(FIXTURE_DIR, "1_blurred.jpg"),
)
def test_createBlurredHDPicture(requests_mock, datafiles, tmp_path):
    destPath = str(tmp_path)

    with open_fs(destPath) as fs:
        with fs.openbin("1.jpg") as f:
            picture = Image.open(f)
            mockBlurringAPIPost(datafiles, requests_mock)

            res = utils.pictures.createBlurredHDPicture(fs, MOCK_BLUR_API, f, "/output.jpg")

            assert res.size == picture.size
            assert sorted(fs.listdir("/")) == sorted(["1.jpg", "1_blurred.jpg", "output.jpg"])


def test_getHDPicturePath(app):
    with app.app_context():
        assert utils.pictures.getHDPicturePath("4366dddb-8a71-4f6e-a3d4-cb6b545476bb") == "/43/66/dd/db/8a71-4f6e-a3d4-cb6b545476bb.jpg"


def test_getPictureFolderPath(app):
    with app.app_context():
        assert utils.pictures.getPictureFolderPath("4366dddb-8a71-4f6e-a3d4-cb6b545476bb") == "/43/66/dd/db/8a71-4f6e-a3d4-cb6b545476bb"


@conftest.SEQ_IMGS
@pytest.mark.parametrize(("preprocess"), ((True), (False)))
def test_checkPictureStatus(preprocess, datafiles, initSequenceApp, fsesUrl, dburl):
    client, app = initSequenceApp(datafiles, preprocess=preprocess)

    # Retrieve loaded sequence metadata
    fses = filesystems.openFilesystems(fsesUrl)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = str(cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0])

            assert len(str(picId)) > 0

            with app.app_context(), app.test_request_context():
                picMetadata = utils.pictures.checkPictureStatus(fses, picId)
                assert picMetadata["status"] == "ready"
                assert picMetadata["type"] == "equirectangular"

                assert utils.pictures.areDerivatesAvailable(fses.derivates, picId, "equirectangular")


@conftest.SEQ_IMGS
@conftest.SEQ_IMGS_FLAT
@pytest.mark.parametrize(("derivates", "pictype"), ((True, "equirectangular"), (False, "equirectangular"), (True, "flat"), (False, "flat")))
def test_areDerivatesAvailable(derivates, pictype, datafiles, initSequenceApp, dburl):
    if pictype == "flat":
        os.remove(datafiles / "1.jpg")
        os.remove(datafiles / "2.jpg")
        os.remove(datafiles / "3.jpg")
        os.remove(datafiles / "4.jpg")
        os.remove(datafiles / "5.jpg")
    else:
        os.remove(datafiles / "b1.jpg")
        os.remove(datafiles / "b2.jpg")

    client, app = initSequenceApp(datafiles, preprocess=derivates)

    # Retrieve loaded sequence metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]

            assert len(str(picId)) > 0

            with app.app_context():
                with open_fs(str(datafiles / "derivates")) as fs:
                    res = utils.pictures.areDerivatesAvailable(fs, picId, pictype)
                    assert res == derivates


@conftest.SEQ_IMG
def test_generatePictureDerivates(datafiles, tmp_path, dburl):
    srcPath = str(datafiles)

    destPath = tmp_path / "out"
    destPath.mkdir()

    with open_fs(str(tmp_path)) as fs:
        res = utils.pictures.generatePictureDerivates(
            fs, Image.open(srcPath + "/1.jpg"), {"cols": 8, "rows": 4, "width": 5760, "height": 2880}, "/out"
        )
        assert res is True

        # Check folder content
        assert sorted(fs.listdir("/out")) == ["sd.jpg", "thumb.jpg", "tiles"]


@conftest.SEQ_IMG
def test_generatePictureDerivates_skipThumbnail(datafiles, tmp_path, dburl):
    srcPath = str(datafiles)

    destPath = tmp_path / "out"
    destPath.mkdir()

    with open_fs(str(tmp_path)) as fs:
        res = utils.pictures.generatePictureDerivates(
            fs, Image.open(srcPath + "/1.jpg"), {"cols": 8, "rows": 4, "width": 5760, "height": 2880}, "/out", skipThumbnail=True
        )
        assert res is True

        # Check folder content
        assert sorted(fs.listdir("/out")) == ["sd.jpg", "tiles"]


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "b1.jpg"))
def test_generatePictureDerivates_flat(datafiles, tmp_path, dburl):
    srcPath = str(datafiles)

    destPath = tmp_path / "out"
    destPath.mkdir()

    with open_fs(str(tmp_path)) as fs:
        res = utils.pictures.generatePictureDerivates(fs, Image.open(srcPath + "/b1.jpg"), {"width": 4288, "height": 3216}, "/out", "flat")
        assert res is True

        # Check folder content
        assert sorted(fs.listdir("/out")) == ["sd.jpg", "thumb.jpg"]


@conftest.SEQ_IMG
def test_createSDPicture(datafiles, tmp_path):
    picture = Image.open(str(datafiles / "1.jpg"))
    destPath = str(tmp_path)

    # Generate file
    with open_fs(destPath) as fs:
        res = utils.pictures.createSDPicture(fs, picture, "/sd.jpg")
        assert res is True

        # Check result file
        resImg = Image.open(destPath + "/sd.jpg")
        w, h = resImg.size
        assert w == 2048
        assert resImg.info["exif"] == picture.info["exif"]


@conftest.SEQ_IMG
def test_createThumbPicture(datafiles, tmp_path):
    picture = Image.open(str(datafiles / "1.jpg"))
    destPath = str(tmp_path)

    # Generate file
    with open_fs(destPath) as fs:
        res = utils.pictures.createThumbPicture(fs, picture, "/thumb.jpg")
        assert res is True

        # Check result file
        resImg = Image.open(destPath + "/thumb.jpg")
        w, h = resImg.size
        assert w == 500
        assert h == 300


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "b1.jpg"))
def test_createThumbPicture_flat(datafiles, tmp_path):
    picture = Image.open(str(datafiles / "b1.jpg"))
    destPath = str(tmp_path)

    # Generate file
    with open_fs(destPath) as fs:
        res = utils.pictures.createThumbPicture(fs, picture, "/thumb.jpg", "flat")
        assert res is True

        # Check result file
        resImg = Image.open(destPath + "/thumb.jpg")
        w, h = resImg.size
        assert w == 500
        assert h == 375


@pytest.mark.parametrize(
    ("imgWidth", "tileCols"), ((512, 4), (1024, 4), (2048, 4), (4096, 8), (5760, 8), (8192, 16), (32768, 64), (655536, 64))
)
def test_getTileSize(imgWidth, tileCols):
    res = utils.pictures.getTileSize((imgWidth, imgWidth / 2))
    assert isinstance(res[0], int)
    assert isinstance(res[1], int)
    assert res[0] == tileCols
    assert res[1] == tileCols / 2
    assert tileCols in [4, 8, 16, 32, 64]


@conftest.SEQ_IMG
def test_getPictureSizing(datafiles):
    res = utils.pictures.getPictureSizing(Image.open(str(datafiles / "1.jpg")))
    assert res["cols"] == 8
    assert res["rows"] == 4
    assert res["width"] == 5760
    assert res["height"] == 2880


@conftest.SEQ_IMG
def test_createTiledPicture(datafiles, tmp_path):
    picture = Image.open(str(datafiles / "1.jpg"))
    destPath = str(tmp_path)
    cols = 4
    rows = 2

    # Generate tiles
    with open_fs(destPath) as fs:
        res = utils.pictures.createTiledPicture(fs, picture, "/", cols, rows)
        assert res is True

        # Check every single file
        origImgSize = picture.size
        colWidth = math.floor(origImgSize[0] / cols)
        rowHeight = math.floor(origImgSize[1] / rows)

        for col in range(cols):
            for row in range(rows):
                tilePath = destPath + "/" + str(col) + "_" + str(row) + ".jpg"
                assert os.path.isfile(tilePath)
                tile = Image.open(tilePath)
                assert tile.size == (colWidth, rowHeight)

                origImgTile = picture.crop((colWidth * col, rowHeight * row, colWidth * (col + 1), rowHeight * (row + 1)))

                assert tile.height == origImgTile.height and tile.width == origImgTile.width

                if tile.mode == origImgTile.mode == "RGBA":
                    img1_alphas = [pixel[3] for pixel in tile.getdata()]
                    img2_alphas = [pixel[3] for pixel in origImgTile.getdata()]
                    assert img1_alphas == img2_alphas


@conftest.SEQ_IMG
def test_insertNewPictureInDatabase(datafiles, tmp_path, dburl, app, defaultAccountID):
    picture = Image.open(str(datafiles / "1.jpg"))
    with psycopg.connect(dburl) as db:
        seqId = sequences.createSequence({}, defaultAccountID)

        picId = utils.pictures.insertNewPictureInDatabase(db, seqId, 1, picture, defaultAccountID, {"another metadata": "a_value"})
        db.commit()

        with psycopg.connect(dburl, row_factory=dict_row) as db2:
            res = db2.execute(
                """
				SELECT id, ts, heading, ST_X(geom) AS lon, ST_Y(geom) AS lat, status, metadata, exif
				FROM pictures
				WHERE id = %s
			""",
                [picId],
            ).fetchone()
            assert res
            assert len(str(res["id"])) > 0
            assert res["ts"].timestamp() == 1627550214.0
            assert res["heading"] == 349
            assert res["lon"] == 1.9191854417991367
            assert res["lat"] == 49.00688961988304
            assert res["status"] == "waiting-for-process"
            assert res["metadata"]["width"] == 5760
            assert res["metadata"]["height"] == 2880
            assert res["metadata"]["cols"] == 8
            assert res["metadata"]["rows"] == 4
            assert res["metadata"].get("lat") is None
            assert res["metadata"].get("lon") is None
            assert res["metadata"].get("ts") is None
            assert res["metadata"].get("heading") is None
            assert res["metadata"]["another metadata"] == "a_value"
            assert len(res["exif"]) > 0


@conftest.SEQ_IMG
def test_readPictureMetadata(datafiles):
    result = utils.pictures.readPictureMetadata(Image.open(str(datafiles) + "/1.jpg"))
    assert result == {
        "lat": 49.00688961988304,
        "lon": 1.9191854417991367,
        "ts": 1627550214.0,
        "heading": 349,
        "type": "equirectangular",
        "make": "GoPro",
        "model": "Max",
        "focal_length": 3.0,
        "crop": None,
        "tagreader_warnings": [],
    }


@conftest.SEQ_IMG
def test_readPictureMetadata_fullExif(datafiles):
    result = utils.pictures.readPictureMetadata(Image.open(str(datafiles) + "/1.jpg"), fullExif=True)
    assert len(result["exif"]) > 0
