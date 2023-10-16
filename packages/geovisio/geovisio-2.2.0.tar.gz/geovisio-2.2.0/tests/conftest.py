from PIL import Image, ImageChops, ImageStat
import pytest
import psycopg
import os
import re
import time
import contextlib
import typing
from dataclasses import dataclass, field

from geovisio import create_app, db_migrations, tokens
from geovisio.utils import filesystems


@pytest.fixture
def dburl():
    # load test.env file if available
    import dotenv

    dotenv.load_dotenv("test.env")

    db = os.environ["DB_URL"]

    db_migrations.update_db_schema(db, force=True)
    return db


@pytest.fixture
def fsesUrl(tmp_path):
    fstmp = tmp_path / "tmp"
    fstmp.mkdir()
    fspermanent = tmp_path / "permanent"
    fspermanent.mkdir()
    fsderivates = tmp_path / "derivates"
    fsderivates.mkdir()
    return filesystems.FilesystemsURL(
        tmp="osfs://" + str(fstmp), permanent="osfs://" + str(fspermanent), derivates="osfs://" + str(fsderivates)
    )


@pytest.fixture
def app(dburl, tmp_path, fsesUrl):
    app = create_app(
        {
            "TESTING": True,
            "DB_URL": dburl,
            "FS_URL": None,
            "FS_TMP_URL": fsesUrl.tmp,
            "FS_PERMANENT_URL": fsesUrl.permanent,
            "FS_DERIVATES_URL": fsesUrl.derivates,
            "SERVER_NAME": "localhost:5000",
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND",
            "SECRET_KEY": "a very secret key",
            "API_PICTURES_LICENSE_SPDX_ID": "etalab-2.0",
            "API_PICTURES_LICENSE_URL": "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE",
        }
    )
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    with app.app_context():
        with app.test_client() as client:
            yield client


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# Code for having at least one sequence in tests
FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

SEQ_IMG = pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "1.jpg"))
SEQ_IMG_FLAT = pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "c1.jpg"))

SEQ_IMGS = pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "1.jpg"),
    os.path.join(FIXTURE_DIR, "2.jpg"),
    os.path.join(FIXTURE_DIR, "3.jpg"),
    os.path.join(FIXTURE_DIR, "4.jpg"),
    os.path.join(FIXTURE_DIR, "5.jpg"),
)

SEQ_IMGS_FLAT = pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "b1.jpg"), os.path.join(FIXTURE_DIR, "b2.jpg"))

SEQ_IMGS_NOHEADING = pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
    os.path.join(FIXTURE_DIR, "e4.jpg"),
    os.path.join(FIXTURE_DIR, "e5.jpg"),
)

SEQ_IMG_BLURRED = pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "1_blurred.jpg"))
MOCK_BLUR_API = "https://geovisio-blurring.net"


@pytest.fixture
def initSequence(initSequenceApp):
    def fct2(datafiles, preprocess=True):
        return initSequenceApp(datafiles, preprocess)[0]

    return fct2


@pytest.fixture
def initSequenceApp(tmp_path, dburl, fsesUrl, bobAccountToken):
    seqPath = tmp_path / "seq1"
    seqPath.mkdir()

    def fct(datafiles, preprocess=True, blur=False, withBob=False):
        twoSeqs = os.path.isfile(datafiles / "1.jpg") and os.path.isfile(datafiles / "b1.jpg")

        if twoSeqs:
            seq2Path = tmp_path / "seq2"
            seq2Path.mkdir()
            for f in os.listdir(datafiles):
                if f not in ["seq1", "seq2", "1_blurred.jpg", "tmp", "derivates", "permanent"]:
                    os.rename(datafiles / f, (seq2Path if f[0:1] == "b" else seqPath) / re.sub("^[a-z]+", "", f))
        else:
            for f in os.listdir(datafiles):
                if f not in ["seq1", "1_blurred.jpg", "tmp", "derivates", "permanent"]:
                    os.rename(datafiles / f, seqPath / re.sub("^[a-z]+", "", f))
        app = create_app(
            {
                "TESTING": True,
                "API_BLUR_URL": MOCK_BLUR_API if blur else "",
                "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS" if preprocess else "ON_DEMAND",
                "DB_URL": dburl,
                "FS_URL": None,
                "FS_TMP_URL": fsesUrl.tmp,
                "FS_PERMANENT_URL": fsesUrl.permanent,
                "FS_DERIVATES_URL": fsesUrl.derivates,
                "SECRET_KEY": "cest beau la vie",
                "API_FORCE_AUTH_ON_UPLOAD": "true" if withBob else None,
            }
        )
        with app.app_context():
            with app.test_client() as client:
                jwtToken = None
                if withBob:
                    jwtToken = bobAccountToken(app)

                uploadSequence(client, tmp_path / "seq1", jwtToken=jwtToken)
                if twoSeqs:
                    uploadSequence(client, tmp_path / "seq2", jwtToken=jwtToken)

                return (client, app)

    return fct


def createSequence(test_client, title, jwtToken=None) -> str:
    headers = {}
    if jwtToken:
        headers["Authorization"] = "Bearer " + jwtToken

    seq = test_client.post(
        "/api/collections",
        headers=headers,
        data={
            "title": title,
        },
    )
    assert seq.status_code < 400
    return seq.headers["Location"]


def uploadPicture(test_client, sesquence_location, pic, filename, position, isBlurred=False, jwtToken=None):
    postData = {"position": position, "picture": (pic, filename)}

    if isBlurred:
        postData["isBlurred"] = "true"

    headers = {}
    if jwtToken:
        headers["Authorization"] = "Bearer " + jwtToken

    picture_response = test_client.post(f"{sesquence_location}/items", headers=headers, data=postData, content_type="multipart/form-data")
    assert picture_response.status_code < 400
    return picture_response.json["id"]


def uploadSequence(test_client, directory, wait=True, jwtToken=None):
    seq_location = createSequence(test_client, os.path.basename(directory), jwtToken=jwtToken)

    pictures_filenames = sorted([f for f in os.listdir(directory) if re.search(r"\.jpe?g$", f, re.IGNORECASE)])

    for i, p in enumerate(pictures_filenames):
        uploadPicture(test_client, seq_location, open(directory / p, "rb"), p, i + 1, jwtToken=jwtToken)

    if wait:
        waitForSequence(test_client, seq_location)


def waitForSequence(test_client, seq_location):
    return waitForSequenceState(
        test_client,
        seq_location,
        wanted_state=lambda s: all(p["status"] == "ready" for p in s.json["items"]) and s.json["status"] == "ready",
    )


def waitForSequenceState(test_client, seq_location, wanted_state):
    """
    Wait for a sequence to have a given state
    `wanted_state` should be a function returning true when the sequence state is the one wanted
    """
    timeout = 10
    waiting_time = 0.1
    total_time = 0
    while total_time < timeout:
        s = test_client.get(f"{seq_location}/geovisio_status")

        # we wait for the collection and all its pictures to be ready
        if wanted_state(s):
            return s
        time.sleep(waiting_time)
        total_time += waiting_time
    assert False, "sequence not ready"


@pytest.fixture(autouse=True)
def dbCleanup(dburl):
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
TRUNCATE TABLE sequences, sequences_pictures, pictures, pictures_to_process CASCADE;
"""
            )


@pytest.fixture()
def defaultAccountID(dburl):
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            accountID = cursor.execute("SELECT id from accounts where is_default = true").fetchone()
            assert accountID
            accountID = accountID[0]
    return accountID


@pytest.fixture()
def bobAccountID(dburl):
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            accountID = cursor.execute("SELECT id from accounts WHERE name = 'bob'").fetchone()
            if accountID:
                return accountID[0]
            accountID = cursor.execute("INSERT INTO accounts (name) VALUES ('bob') RETURNING id").fetchone()
            assert accountID
            accountID = accountID[0]
    return accountID


@pytest.fixture()
def bobAccountToken(bobAccountID, dburl):
    def fct(app):
        with app.app_context(), psycopg.connect(dburl) as conn, conn.cursor() as cursor:
            accountToken = cursor.execute("SELECT id FROM tokens WHERE account_id = %s", [bobAccountID]).fetchone()
            assert accountToken
            accountToken = accountToken[0]
            return tokens._generate_jwt_token(accountToken)

    return fct


@pytest.fixture()
def defaultAccountToken(defaultAccountID, dburl):
    def fct(app):
        with app.app_context(), psycopg.connect(dburl) as conn, conn.cursor() as cursor:
            accountToken = cursor.execute("SELECT id FROM tokens WHERE account_id = %s", [defaultAccountID]).fetchone()
            assert accountToken
            accountToken = accountToken[0]
            return tokens._generate_jwt_token(accountToken)

    return fct


@contextlib.contextmanager
def monkeypatched_function(object, name, patch):
    """Temporarily monkeypatches an object."""
    pre_patched_value = getattr(object, name)
    setattr(object, name, patch)
    yield object
    setattr(object, name, pre_patched_value)


def getFirstPictureIds(dburl) -> typing.Tuple[str, str]:
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            p = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures WHERE rank = 1").fetchone()
            assert p is not None
            return p


@dataclass
class Picture(object):
    id: str

    def get_derivate_dir(self, datafiles):
        return os.path.join(datafiles, "derivates", self.id[0:2], self.id[2:4], self.id[4:6], self.id[6:8], self.id[9:])

    def get_permanent_file(self, datafiles):
        return os.path.join(datafiles, "permanent", self.id[0:2], self.id[2:4], self.id[4:6], self.id[6:8], f"{self.id[9:]}.jpg")


@dataclass
class Sequence(object):
    id: str
    pictures: typing.List[Picture] = field(default_factory=lambda: [])


def getPictureIds(dburl) -> typing.List[Sequence]:
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            pics = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures ORDER BY rank").fetchall()
            assert pics is not None

            sequences = []
            for seq_id, pic_id in pics:
                s = next((s for s in sequences if s.id == str(seq_id)), None)
                if s is None:
                    s = Sequence(id=str(seq_id))
                    sequences.append(s)
                s.pictures.append(Picture(id=str(pic_id)))

            return sequences


def createManySequences(dburl):
    seq = getPictureIds(dburl)[0]

    # Duplicate sequence metadata to have many sequences
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            # Populate sequences
            for i in range(10):
                cursor.execute(
                    """
                    INSERT INTO sequences(status, metadata, geom, account_id, inserted_at)
                    SELECT status, metadata, geom, account_id, inserted_at + random() * (timestamp '2030-01-01 00:00:00' - inserted_at)
                    FROM sequences
                """
                )

            # Populate sequences_pictures
            cursor.execute(
                """
                INSERT INTO sequences_pictures(seq_id, pic_id, rank)
                SELECT s.id, sp.pic_id, sp.rank
                FROM sequences s, sequences_pictures sp
                WHERE s.id != %s
            """,
                [seq.id],
            )

            conn.commit()


def mockCreateBlurredHDPictureFactory(datafiles):
    """Mock function for pictures.createBlurredHDPicture"""

    def mockCreateBlurredHDPicture(fs, blurApi, pictureBytes, outputFilename):
        with open(datafiles + "/1_blurred.jpg", "rb") as f:
            fs.writebytes(outputFilename, f.read())
            return Image.open(str(datafiles + "/1_blurred.jpg"))

    return mockCreateBlurredHDPicture


def mockBlurringAPIPost(datafiles, requests_mock):
    with open(datafiles + "/1_blurred.jpg", "rb") as mask:
        requests_mock.post(MOCK_BLUR_API + "/blur/", headers={"Content-Type": "image/jpeg"}, content=mask.read())


def arePicturesSimilar(pic1, pic2, limit=1):
    """Checks if two images have less than limit % of differences"""
    diff = ImageChops.difference(pic1.convert("RGB"), pic2.convert("RGB"))
    stat = ImageStat.Stat(diff)
    diff_ratio = sum(stat.mean) / (len(stat.mean) * 255) * 100
    return diff_ratio <= limit


STAC_VERSION = "1.0.0"


@pytest.fixture
def no_license_app_client(dburl, fsesUrl):
    app = create_app(
        {
            "TESTING": True,
            "DB_URL": dburl,
            "FS_URL": None,
            "FS_TMP_URL": fsesUrl.tmp,
            "FS_PERMANENT_URL": fsesUrl.permanent,
            "FS_DERIVATES_URL": fsesUrl.derivates,
            "SERVER_NAME": "localhost:5000",
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND",
            "SECRET_KEY": "a very secret key",
        }
    )
    with app.app_context(), app.test_client() as client:
        yield client
