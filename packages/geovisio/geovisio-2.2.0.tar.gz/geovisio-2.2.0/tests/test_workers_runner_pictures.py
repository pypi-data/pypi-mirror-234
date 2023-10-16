import os
import io
import psycopg
import re
from psycopg.rows import dict_row
from PIL import Image
from uuid import UUID
from geovisio.workers import runner_pictures
from . import conftest
from geovisio import utils, create_app

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@conftest.SEQ_IMGS
def test_processSequence(datafiles, initSequence, tmp_path, dburl, defaultAccountID):
    initSequence(datafiles)

    # Check results
    with psycopg.connect(dburl, row_factory=dict_row) as db2:
        # Sequence definition
        res0 = db2.execute(
            """
            SELECT
                id, status, metadata,
                account_id, ST_AsText(geom) AS geom,
                computed_type, computed_model, computed_capture_date
            FROM sequences
        """
        ).fetchall()[0]

        seqId = str(res0["id"])
        assert len(seqId) > 0

        # use regex because float precision may differ between systems
        expectedGeom = re.compile(
            r"^LINESTRING\(1\.919185441799\d+ 49\.00688961988\d+,1\.919189623000\d+ 49\.0068986458\d+,1\.919196360602\d+ 49\.00692625960\d+,1\.919199780601\d+ 49\.00695484980\d+,1\.919194019996\d+ 49\.00697341759\d+\)$"
        )
        assert expectedGeom.match(res0["geom"]) is not None
        assert res0["status"] == "ready"
        assert res0["account_id"] == defaultAccountID
        assert res0["metadata"]["title"] == "seq1"
        assert res0["computed_type"] == "equirectangular"
        assert res0["computed_model"] == "GoPro Max"
        assert res0["computed_capture_date"].isoformat() == "2021-07-29"

        # Pictures
        res1 = db2.execute("SELECT id, ts, status, metadata, account_id FROM pictures ORDER BY ts").fetchall()

        assert len(res1) == 5
        assert len(str(res1[0]["id"])) > 0
        assert res1[0]["ts"].timestamp() == 1627550214.0
        assert res1[0]["status"] == "ready"
        assert res1[0]["metadata"]["field_of_view"] == 360
        assert res1[0]["account_id"] == defaultAccountID

        picIds = []
        for rec in res1:
            picIds.append(str(rec["id"]))

        # Sequences + pictures
        with db2.cursor() as cursor:
            res2 = cursor.execute("SELECT pic_id FROM sequences_pictures WHERE seq_id = %s ORDER BY rank", [seqId]).fetchall()
            resPicIds = [str(f["pic_id"]) for f in res2]

            assert resPicIds == picIds

        # Check destination folder structure
        for picId in picIds:
            permaPath = str(tmp_path / "permanent" / picId[0:2] / picId[2:4] / picId[4:6] / picId[6:8] / picId[9:]) + ".jpg"
            derivPath = tmp_path / "derivates" / picId[0:2] / picId[2:4] / picId[4:6] / picId[6:8] / picId[9:]
            assert os.path.isfile(permaPath)
            assert os.path.isdir(derivPath)
            assert os.path.isdir(derivPath / "tiles")
            assert os.path.isfile(derivPath / "sd.jpg")
            assert os.path.isfile(derivPath / "thumb.jpg")

        # Check upload folder has been removed
        assert len(os.listdir(tmp_path / "tmp")) == 0

        newSequencePicturesEntries = db2.execute(
            "select rank from sequences_pictures inner join pictures on (pic_id = id) order by ts asc"
        ).fetchall()
        assert newSequencePicturesEntries == [{"rank": rank} for rank in range(1, len(newSequencePicturesEntries) + 1)]


@conftest.SEQ_IMGS_FLAT
def test_processSequence_flat(datafiles, initSequence, tmp_path, dburl, defaultAccountID):
    with psycopg.connect(dburl, row_factory=dict_row) as db2:
        # Add camera metadata
        db2.execute("INSERT INTO cameras(model, sensor_width) VALUES ('OLYMPUS IMAGING CORP. SP-720UZ', 6.16) ON CONFLICT DO NOTHING")
        db2.commit()

        # Run processing
        initSequence(datafiles)

        # Sequence definition
        res0 = db2.execute(
            """
            SELECT
                id, status, metadata,
                account_id, ST_AsText(geom) AS geom,
                computed_type, computed_model, computed_capture_date
            FROM sequences
        """
        ).fetchall()[0]

        seqId = str(res0["id"])
        assert len(seqId) > 0
        # use regex because float precision may differ between systems
        expectedGeom = re.compile(r"^LINESTRING\(-1\.949973106007\d+ 48\.139852239480\d+,-1\.949124581909\d+ 48\.13939279199\d+\)$")
        assert expectedGeom.match(res0["geom"]) is not None
        assert res0["status"] == "ready"
        assert res0["account_id"] == defaultAccountID
        assert res0["metadata"]["title"] == "seq1"
        assert res0["computed_type"] == "flat"
        assert res0["computed_model"] == "OLYMPUS IMAGING CORP. SP-720UZ"
        assert res0["computed_capture_date"].isoformat() == "2015-04-25"

        # Pictures
        res1 = db2.execute("SELECT id, ts, status, metadata, account_id FROM pictures ORDER BY ts").fetchall()

        assert len(res1) == 2
        assert len(str(res1[0]["id"])) > 0
        assert res1[0]["ts"].timestamp() == 1429976177.0
        assert res1[0]["status"] == "ready"
        assert res1[0]["metadata"]["field_of_view"] == 67
        assert res1[0]["account_id"] == defaultAccountID

        picIds = []
        for rec in res1:
            picIds.append(str(rec["id"]))

        # Check destination folder structure
        for picId in picIds:
            permaPath = str(tmp_path / "permanent" / picId[0:2] / picId[2:4] / picId[4:6] / picId[6:8] / picId[9:]) + ".jpg"
            derivPath = tmp_path / "derivates" / picId[0:2] / picId[2:4] / picId[4:6] / picId[6:8] / picId[9:]
            assert os.path.isfile(permaPath)
            assert os.path.isdir(derivPath)
            assert not os.path.isdir(derivPath / "tiles")
            assert os.path.isfile(derivPath / "sd.jpg")
            assert os.path.isfile(derivPath / "thumb.jpg")

        # Check upload folder has been removed
        assert len(os.listdir(tmp_path / "tmp")) == 0


@conftest.SEQ_IMGS_NOHEADING
def test_processSequence_noheading(datafiles, initSequence, tmp_path, dburl):
    with psycopg.connect(dburl, row_factory=dict_row) as db2:
        initSequence(datafiles, preprocess=False)

        # Sequence definition
        seqId = db2.execute("SELECT id FROM sequences").fetchall()
        assert len(seqId) == 1

        # Pictures
        pics = db2.execute("SELECT * FROM pictures ORDER BY ts").fetchall()

        for r in pics:
            assert r["status"] == "ready"
            assert r["metadata"].get("heading") is None

        headings = {r["metadata"].get("originalFileName"): r["heading"] for r in pics}
        assert headings == {"1.jpg": 277, "2.jpg": 272, "3.jpg": 272, "4.jpg": 270, "5.jpg": 270}


@conftest.SEQ_IMGS
def test_updateSequenceHeadings_unchanged(datafiles, initSequence, dburl):
    initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl, autocommit=True) as db:
        seqId = db.execute("SELECT id FROM sequences").fetchone()
        assert seqId
        seqId = seqId[0]
        picHeadings = {}
        for key, value in db.execute("SELECT id, heading FROM pictures").fetchall():
            picHeadings[key] = value

        runner_pictures.updateSequenceHeadings(db, seqId, 10, True)

        for id, heading, headingMetadata in db.execute("SELECT id, heading, metadata->>'heading' AS mh FROM pictures").fetchall():
            assert picHeadings[id] == heading
            assert headingMetadata is None


@conftest.SEQ_IMGS
def test_updateSequenceHeadings_updateAllExisting(datafiles, initSequence, dburl):
    initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl, autocommit=True) as db:
        seqId = db.execute("SELECT id FROM sequences").fetchone()
        assert seqId is not None
        seqId = seqId[0]
        runner_pictures.updateSequenceHeadings(db, seqId, 10, False)
        res = db.execute("select metadata->>'originalFileName', heading, metadata->>'heading' AS mh from pictures").fetchall()
        for r in res:
            assert r[2] is None
        headings = {r[0].split("/")[-1]: r[1] for r in res}
        assert headings == {"1.jpg": 34, "2.jpg": 23, "3.jpg": 16, "4.jpg": 352, "5.jpg": 352}


@conftest.SEQ_IMG
def test_processPictureFiles_noblur_preprocess(datafiles, tmp_path, fsesUrl, dburl, defaultAccountID):
    with open(datafiles / "1.jpg", "rb") as f:
        picAsBytes = io.BytesIO(f.read())
    picture = Image.open(str(datafiles / "1.jpg"))
    pictureOrig = picture.copy()

    app = create_app(
        {
            "TESTING": True,
            "DB_URL": dburl,
            "FS_URL": None,
            "FS_TMP_URL": fsesUrl.tmp,
            "FS_PERMANENT_URL": fsesUrl.permanent,
            "FS_DERIVATES_URL": fsesUrl.derivates,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
        }
    )
    with app.app_context():
        with psycopg.connect(dburl) as db:
            seqId = utils.sequences.createSequence({}, defaultAccountID)
            picId = utils.pictures.insertNewPictureInDatabase(db, seqId, 0, picture, defaultAccountID, {})

            # persist file
            utils.pictures.saveRawPicture(picId, picAsBytes, isBlurred=False)

            runner_pictures.process_next_picture(app.config)

            pics = conftest.getPictureIds(dburl)[0].pictures
            derivate_dir = pics[0].get_derivate_dir(datafiles)

            # No Blur + preprocess derivates = generates thumbnail and all derivates+ original file
            assert sorted(os.listdir(derivate_dir)) == [
                "sd.jpg",
                "thumb.jpg",
                "tiles",
            ]
            assert conftest.arePicturesSimilar(pictureOrig, Image.open(str(pics[0].get_permanent_file(datafiles))))

            # Check content is same as generatePictureDerivates
            os.makedirs(datafiles / "derivates" / "gvs_picder")
            resPicDer = utils.pictures.generatePictureDerivates(
                app.config["FILESYSTEMS"].derivates, picture, {"cols": 8, "rows": 4, "width": 5760, "height": 2880}, "/gvs_picder"
            )
            assert resPicDer is True
            assert sorted(os.listdir(derivate_dir)) == sorted(app.config["FILESYSTEMS"].derivates.listdir("/gvs_picder/"))
            assert sorted(os.listdir(f"{derivate_dir}/tiles/")) == sorted(app.config["FILESYSTEMS"].derivates.listdir("/gvs_picder/tiles/"))


@conftest.SEQ_IMG
def test_processPictureFiles_noblur_ondemand(datafiles, tmp_path, fsesUrl, dburl, defaultAccountID):
    with open(datafiles / "1.jpg", "rb") as f:
        picAsBytes = io.BytesIO(f.read())
    picture = Image.open(str(datafiles / "1.jpg"))
    pictureOrig = picture.copy()

    app = create_app(
        {
            "TESTING": True,
            "DB_URL": dburl,
            "FS_URL": None,
            "FS_TMP_URL": fsesUrl.tmp,
            "FS_PERMANENT_URL": fsesUrl.permanent,
            "FS_DERIVATES_URL": fsesUrl.derivates,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND",
        }
    )
    with app.app_context():
        with psycopg.connect(dburl) as db:
            seqId = utils.sequences.createSequence({}, defaultAccountID)
            picId = utils.pictures.insertNewPictureInDatabase(db, seqId, 0, picture, defaultAccountID, {})

            # persist file
            utils.pictures.saveRawPicture(picId, picAsBytes, isBlurred=False)

            runner_pictures.process_next_picture(app.config)

            pics = conftest.getPictureIds(dburl)[0].pictures
            derivate_dir = pics[0].get_derivate_dir(datafiles)

            # No blur + on-demand derivates = generates thumbnail + original file
            assert sorted(os.listdir(derivate_dir)) == ["thumb.jpg"]
            assert conftest.arePicturesSimilar(pictureOrig, Image.open(str(pics[0].get_permanent_file(datafiles))))


@conftest.SEQ_IMG
@conftest.SEQ_IMG_BLURRED
def test_processPictureFiles_blur_preprocess(monkeypatch, datafiles, tmp_path, fsesUrl, dburl, defaultAccountID):
    monkeypatch.setattr(utils.pictures, "createBlurredHDPicture", conftest.mockCreateBlurredHDPictureFactory(datafiles))
    with open(datafiles / "1.jpg", "rb") as f:
        picAsBytes = io.BytesIO(f.read())
    picture = Image.open(str(datafiles / "1.jpg"))
    pictureOrig = picture.copy()

    app = create_app(
        {
            "TESTING": True,
            "DB_URL": dburl,
            "FS_URL": None,
            "FS_TMP_URL": fsesUrl.tmp,
            "FS_PERMANENT_URL": fsesUrl.permanent,
            "FS_DERIVATES_URL": fsesUrl.derivates,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
            "API_BLUR_URL": "https://geovisio-blurring.net",
        }
    )
    with app.app_context():
        with psycopg.connect(dburl) as db:
            seqId = utils.sequences.createSequence({}, defaultAccountID)
            picId = utils.pictures.insertNewPictureInDatabase(db, seqId, 0, picture, defaultAccountID, {})

            # persist file
            utils.pictures.saveRawPicture(picId, picAsBytes, isBlurred=False)

            runner_pictures.process_next_picture(app.config)

            pics = conftest.getPictureIds(dburl)[0].pictures
            derivate_dir = pics[0].get_derivate_dir(datafiles)

            # Blur + preprocess derivates = generates thumbnail, all derivates + blurred original file
            assert sorted(os.listdir(derivate_dir)) == [
                "sd.jpg",
                "thumb.jpg",
                "tiles",
            ]
            # picture should be blurred, so different from original
            assert not conftest.arePicturesSimilar(pictureOrig, Image.open(str(pics[0].get_permanent_file(datafiles))))

            # Check tmp folder has been removed
            assert len(app.config["FILESYSTEMS"].tmp.listdir("/")) == 0


@conftest.SEQ_IMG
@conftest.SEQ_IMG_BLURRED
def test_processPictureFiles_blur_ondemand(monkeypatch, datafiles, tmp_path, fsesUrl, dburl, defaultAccountID):
    monkeypatch.setattr(utils.pictures, "createBlurredHDPicture", conftest.mockCreateBlurredHDPictureFactory(datafiles))
    with open(datafiles / "1.jpg", "rb") as f:
        picAsBytes = io.BytesIO(f.read())
    picture = Image.open(str(datafiles / "1.jpg"))
    pictureOrig = picture.copy()

    app = create_app(
        {
            "TESTING": True,
            "DB_URL": dburl,
            "FS_URL": None,
            "FS_TMP_URL": fsesUrl.tmp,
            "FS_PERMANENT_URL": fsesUrl.permanent,
            "FS_DERIVATES_URL": fsesUrl.derivates,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND",
            "API_BLUR_URL": "https://geovisio-blurring.net",
        }
    )
    with app.app_context():
        with psycopg.connect(dburl) as db:
            seqId = utils.sequences.createSequence({}, defaultAccountID)
            picId = utils.pictures.insertNewPictureInDatabase(db, seqId, 0, picture, defaultAccountID, {})

            # persist file
            utils.pictures.saveRawPicture(picId, picAsBytes, isBlurred=False)

            runner_pictures.process_next_picture(app.config)

            pics = conftest.getPictureIds(dburl)[0].pictures
            derivate_dir = pics[0].get_derivate_dir(datafiles)

            # Blur + on-demand derivates = generates thumbnail + blurred original file
            assert sorted(os.listdir(derivate_dir)) == ["thumb.jpg"]
            # picture should be blurred, so different from original
            assert not conftest.arePicturesSimilar(pictureOrig, Image.open(str(pics[0].get_permanent_file(datafiles))))

            # Check tmp folder has been removed
            assert len(app.config["FILESYSTEMS"].tmp.listdir("/")) == 0


@conftest.SEQ_IMGS
def test_get_next_picture_to_process(datafiles, app, tmp_path, dburl, defaultAccountID):
    """
    Test runner_pictures._get_next_picture_to_process
    Insert 3 images, they should be taken in order 1 -> 3 -> 2 -> None (since 2 is marked as 'preparing-derivates' and should be taken last as we consider it has already been tried)
    """
    picture = Image.open(str(datafiles / "1.jpg"))

    seqId = utils.sequences.createSequence({}, defaultAccountID)
    with psycopg.connect(dburl) as db:
        db.commit()
        pic1_id = utils.pictures.insertNewPictureInDatabase(db, seqId, 1, picture, defaultAccountID, {})
        db.commit()  # we commit each insert to get different insert_at timestamp
        pic2_id = utils.pictures.insertNewPictureInDatabase(db, seqId, 2, picture, defaultAccountID, {})
        db.commit()
        pic3_id = utils.pictures.insertNewPictureInDatabase(db, seqId, 3, picture, defaultAccountID, {})
        db.commit()
        # being 'preparing-derivates' should only makes pic 2 to be taken last
        db.execute("UPDATE pictures SET status = 'preparing-derivates' WHERE id = %s", [pic2_id])
        db.commit()

    config = {"DB_URL": dburl}
    with runner_pictures._get_next_picture_to_process(config) as db_pic:
        assert db_pic is not None
        assert db_pic.id == str(pic1_id)

        with runner_pictures._get_next_picture_to_process(config) as db_pic2:
            assert db_pic2 is not None
            assert db_pic2.id == str(pic3_id)

            try:
                with runner_pictures._get_next_picture_to_process(config) as db_pic3:
                    assert db_pic3 is not None
                    assert db_pic3.id == str(pic2_id)

                    # There should no more be pictures to process
                    with runner_pictures._get_next_picture_to_process(config) as db_pic4:
                        assert db_pic4 is None

                    # An exception is raised, a rollback should occure, pic2 should be marked on error and lock should be released
                    raise Exception("some exception")
            except:
                pass

            with runner_pictures._get_next_picture_to_process(config) as db_pic5:
                assert db_pic5 is None


def start_background_worker(dburl, tmp_path, config):
    import threading

    def pic_background_process():
        worker = create_app(config)
        import logging

        logging.info("Running picture worker in test")
        worker = runner_pictures.PictureProcessor(config=worker.config, stop=True)
        worker.process_next_pictures()
        return

    t = threading.Thread(target=pic_background_process)

    t.start()

    t.join()


@conftest.SEQ_IMGS
def test_split_workers(datafiles, dburl, tmp_path):
    """
    Test posting new picture with some split workers to do the job
    """

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
            seq_location = conftest.createSequence(client, os.path.basename(datafiles))
            pic_id = conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1)

            # no worker start yet, pictures should be waiting for process
            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 1
            r = conn.execute("SELECT id, status FROM pictures").fetchall()
            assert r and list(r) == [(UUID(pic_id), "waiting-for-process")]

            # start a background job that stop when all pictures have been processed
            start_background_worker(
                dburl,
                tmp_path,
                config={
                    "TESTING": True,
                    "DB_URL": dburl,
                    "FS_URL": str(tmp_path),
                    "FS_TMP_URL": None,
                    "FS_PERMANENT_URL": None,
                    "FS_DERIVATES_URL": None,
                },
            )

            # all should be ready
            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 0
            r = conn.execute("SELECT id, status FROM pictures").fetchall()
            assert r and list(r) == [(UUID(pic_id), "ready")]


@conftest.SEQ_IMGS
def test_split_workers_reprocess_pic(datafiles, dburl, tmp_path):
    """
    Test posting new picture with some split workers to do the job
    After the picture has been processed, we try to reprocess the picture, and this should work
    """

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

    def start_worker():
        start_background_worker(
            dburl,
            tmp_path,
            config={
                "TESTING": True,
                "DB_URL": dburl,
                "FS_URL": str(tmp_path),
                "FS_TMP_URL": None,
                "FS_PERMANENT_URL": None,
                "FS_DERIVATES_URL": None,
            },
        )

    with app.app_context():
        with app.test_client() as client, psycopg.connect(dburl) as conn:
            seq_location = conftest.createSequence(client, os.path.basename(datafiles))
            pic_id = conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1)

            # no worker start yet, pictures should be waiting for process
            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 1
            r = conn.execute("SELECT id, status, process_error, nb_errors FROM pictures").fetchall()
            assert r and list(r) == [(UUID(pic_id), "waiting-for-process", None, 0)]

            # start a background job that stop when all pictures have been processed
            start_worker()

            # all should be ready
            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 0
            r = conn.execute("SELECT id, status, process_error, nb_errors FROM pictures").fetchall()
            assert r and list(r) == [(UUID(pic_id), "ready", None, 0)]

            # we add again the picture into the picture_to_process table
            r = conn.execute("INSERT INTO pictures_to_process (picture_id) VALUES (%s)", [pic_id])
            conn.commit()

            # no worker start yet, pictures should be waiting for process
            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 1
            r = conn.execute("SELECT id, status, process_error, nb_errors FROM pictures").fetchall()
            assert r and list(r) == [
                (UUID(pic_id), "ready", None, 0)
            ]  # picture is ready even if it need processing, because it has already been processed once

            # start a background job that stop when all pictures have been processed
            start_worker()

            # all should be ready
            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 0
            r = conn.execute("SELECT id, status, process_error, nb_errors FROM pictures").fetchall()
            assert r and list(r) == [(UUID(pic_id), "ready", None, 0)]


@conftest.SEQ_IMGS
@conftest.SEQ_IMG_BLURRED
def test_split_workers_reprocess_pic_blur(monkeypatch, datafiles, dburl, tmp_path):
    monkeypatch.setattr(utils.pictures, "createBlurredHDPicture", conftest.mockCreateBlurredHDPictureFactory(datafiles))
    """
    Test posting new picture with some split workers to do the job
    After the picture has been processed, we try to reprocess the picture, and this should work even if blurring is needed
    """

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
            "API_BLUR_URL": conftest.MOCK_BLUR_API,
        }
    )

    def start_worker():
        start_background_worker(
            dburl,
            tmp_path,
            config={
                "TESTING": True,
                "DB_URL": dburl,
                "FS_URL": str(tmp_path),
                "FS_TMP_URL": None,
                "FS_PERMANENT_URL": None,
                "FS_DERIVATES_URL": None,
                "API_BLUR_URL": conftest.MOCK_BLUR_API,
            },
        )

    with app.app_context():
        with app.test_client() as client, psycopg.connect(dburl) as conn:
            seq_location = conftest.createSequence(client, os.path.basename(datafiles))
            pic_id = conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1, isBlurred=False)

            # no worker start yet, pictures should be waiting for process
            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 1
            r = conn.execute("SELECT id, status, process_error, nb_errors FROM pictures").fetchall()
            assert r and list(r) == [(UUID(pic_id), "waiting-for-process", None, 0)]

            # start a background job that stop when all pictures have been processed
            start_worker()

            # all should be ready
            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 0
            r = conn.execute("SELECT id, status, process_error, nb_errors FROM pictures").fetchall()
            assert r and list(r) == [(UUID(pic_id), "ready", None, 0)]

            # we add again the picture into the picture_to_process table
            r = conn.execute("INSERT INTO pictures_to_process (picture_id) VALUES (%s)", [pic_id])
            conn.commit()

            # no worker start yet, pictures should be waiting for process
            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 1
            r = conn.execute("SELECT id, status, process_error, nb_errors FROM pictures").fetchall()
            assert r and list(r) == [
                (UUID(pic_id), "ready", None, 0)
            ]  # picture is ready even if it need processing, because it has already been processed once

            # start a background job that stop when all pictures have been processed
            start_worker()

            # all should be ready
            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 0
            r = conn.execute("SELECT id, status, process_error, nb_errors FROM pictures").fetchall()
            assert r and list(r) == [(UUID(pic_id), "ready", None, 0)]
