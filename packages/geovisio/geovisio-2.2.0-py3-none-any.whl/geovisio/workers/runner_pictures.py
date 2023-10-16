from fs import open_fs
from fs.path import dirname
from PIL import Image, ImageOps
from flask import current_app
import psycopg
import traceback
from geovisio import utils
from geovisio import errors
from dataclasses import dataclass
import logging
from contextlib import contextmanager
from enum import Enum
from typing import Any
import threading

import geovisio.utils.filesystems

log = logging.getLogger("geovisio.runner_pictures")


class PictureBackgroundProcessor(object):
    def init_app(self, app):
        nb_threads = app.config["EXECUTOR_MAX_WORKERS"]
        self.enabled = nb_threads != 0

        if self.enabled:
            from flask_executor import Executor

            self.executor = Executor(app, name="PicProcessor")
        else:
            import sys

            if "run" in sys.argv or "waitress" in sys.argv:  # hack not to display a frightening warning uselessly
                log.warning("No picture background processor run, no picture will be processed unless another separate worker is run")
                log.warning("A separate process can be run with:")
                log.warning("flask picture-worker")

    def process_pictures(self):
        """
        Ask for a background picture process that will run until not pictures need to be processed
        """
        if self.enabled:
            worker = PictureProcessor(config=current_app.config)
            return self.executor.submit(worker.process_next_pictures)


background_processor = PictureBackgroundProcessor()


class ProcessTask(str, Enum):
    prepare = "prepare"
    delete = "delete"


@dataclass
class DbPicture:
    id: str
    task: ProcessTask
    metadata: dict

    def blurred_by_author(self):
        return self.metadata.get("blurredByAuthor", False)


def updateSequenceHeadings(db, sequenceId, relativeHeading=0, updateOnlyMissing=True):
    """Defines pictures heading according to sequence path.
    Database is not committed in this function, to make entry definitively stored
    you have to call db.commit() after or use an autocommit connection.

    Parameters
    ----------
    db : psycopg.Connection
            Database connection
    sequenceId : uuid
            The sequence's uuid, as stored in the database
    relativeHeading : int
            Camera relative orientation compared to path, in degrees clockwise.
            Example: 0° = looking forward, 90° = looking to right, 180° = looking backward, -90° = looking left.
    updateOnlyMissing : bool
            If true, doesn't change existing heading values in database
    """

    db.execute(
        """
		WITH h AS (
			SELECT
				p.id,
				CASE
					WHEN LEAD(sp.rank) OVER othpics IS NULL AND LAG(sp.rank) OVER othpics IS NULL
						THEN NULL
					WHEN LEAD(sp.rank) OVER othpics IS NULL
						THEN (360 + FLOOR(DEGREES(ST_Azimuth(LAG(p.geom) OVER othpics, p.geom)))::int + (%(diff)s %% 360)) %% 360
					ELSE
						(360 + FLOOR(DEGREES(ST_Azimuth(p.geom, LEAD(p.geom) OVER othpics)))::int + (%(diff)s %% 360)) %% 360
				END AS heading
			FROM pictures p
			JOIN sequences_pictures sp ON sp.pic_id = p.id AND sp.seq_id = %(seq)s
			WINDOW othpics AS (ORDER BY sp.rank)
		)
		UPDATE pictures p
		SET heading = h.heading, heading_computed = true
		FROM h
		WHERE h.id = p.id
		"""
        + (
            " AND (p.heading IS NULL OR p.heading = 0 OR p.heading_computed)" if updateOnlyMissing else ""
        ),  # lots of camera have heading set to 0 for unset heading, so we recompute the heading when it's 0 too, even if this could be a valid value
        {"seq": sequenceId, "diff": relativeHeading},
    )


def processPictureFiles(db, dbPic: DbPicture, config):
    """Generates the files associated with a sequence picture.

    If needed the image is blurred before the tiles and thumbnail are generated.

    Parameters
    ----------
    db : psycopg.Connection
            Database connection
    dbPic : DbPicture
            The picture metadata extracted from database
    config : dict
            Flask app.config (passed as param to allow using ThreadPoolExecutor)
    """

    skipBlur = dbPic.blurred_by_author() or config.get("API_BLUR_URL") == None
    fses = config["FILESYSTEMS"]
    fs = fses.permanent if skipBlur else fses.tmp
    picHdPath = utils.pictures.getHDPicturePath(dbPic.id)

    if not fs.exists(picHdPath):
        # if we were looking for the picture in the temporary fs ans it's not here, we check if it's in the permanent one
        # it can be the case when we try to reprocess an already processed picture
        if fs != fses.permanent and fses.permanent.exists(picHdPath):
            fs = fses.permanent
        else:
            raise Exception(f"Impossible to find picture file: {picHdPath}")

    with fs.openbin(picHdPath) as pictureBytes:
        picture = Image.open(pictureBytes)

        # Create picture folders for this specific picture
        picDerivatesFolder = utils.pictures.getPictureFolderPath(dbPic.id)
        fses.derivates.makedirs(picDerivatesFolder, recreate=True)
        fses.permanent.makedirs(dirname(picHdPath), recreate=True)

        # Create blurred version if required
        if not skipBlur:
            _set_status(db, dbPic.id, "preparing-blur")
            try:
                picture = utils.pictures.createBlurredHDPicture(fses.permanent, config.get("API_BLUR_URL"), pictureBytes, picHdPath)
            except Exception as e:
                logging.exception(e)
                raise Exception("Blur API failure: " + errors.getMessageFromException(e)) from e

            # Delete original unblurred file
            geovisio.utils.filesystems.removeFsEvenNotFound(fses.tmp, picHdPath)

            # Cleanup parent folders
            parentFolders = picHdPath.split("/")
            parentFolders.pop()
            checkFolder = parentFolders.pop()
            while checkFolder:
                currentFolder = "/".join(parentFolders) + "/" + checkFolder
                if fses.tmp.exists(currentFolder) and fses.tmp.isempty(currentFolder):
                    geovisio.utils.filesystems.removeFsTreeEvenNotFound(fses.tmp, currentFolder)
                    checkFolder = parentFolders.pop()
                else:
                    checkFolder = False

        else:
            # Make sure image rotation is always applied
            #  -> Not necessary on pictures from blur API, as SGBlur ensures rotation is always applied
            picture = ImageOps.exif_transpose(picture)

        _set_status(db, dbPic.id, "preparing-derivates")

        # Always pre-generate thumbnail
        utils.pictures.createThumbPicture(fses.derivates, picture, picDerivatesFolder + "/thumb.jpg", dbPic.metadata["type"])

        # Create SD and tiles
        if config.get("PICTURE_PROCESS_DERIVATES_STRATEGY") == "PREPROCESS":
            utils.pictures.generatePictureDerivates(
                fses.derivates, picture, dbPic.metadata, picDerivatesFolder, dbPic.metadata["type"], skipThumbnail=True
            )


class RecoverableProcessException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class PictureProcessor:
    stop: bool
    config: dict[Any, Any]

    def __init__(self, config, stop=True) -> None:
        self.config = config
        self.stop = stop
        if threading.current_thread() is threading.main_thread():
            # if worker is in daemon mode, register signals to gracefully stop it
            self._register_signals()

    def process_next_pictures(self):
        try:
            while True:
                r = process_next_picture(self.config)
                if self.stop:
                    return
                if not r:
                    # no more picture to process
                    # wait a bit until there are some
                    import time

                    time.sleep(1)

        except:
            log.exception("Exiting thread")

    def _register_signals(self):
        import signal

        signal.signal(signal.SIGINT, self._graceful_shutdown)
        signal.signal(signal.SIGTERM, self._graceful_shutdown)

    def _graceful_shutdown(self, *args):
        log.info("Stoping worker, waiting for last picture processing to finish...")
        self.stop = True


def process_next_picture(config):
    with _get_next_picture_to_process(config) as db_pic:
        if db_pic is None:
            return False
        if db_pic.task == ProcessTask.prepare:
            with utils.time.log_elapsed(f"Processing picture {db_pic.id}"), psycopg.connect(config["DB_URL"], autocommit=True) as db:
                # open another connection for reporting and queries
                _process_picture(db, config, db_pic)
        elif db_pic.task == ProcessTask.delete:
            with utils.time.log_elapsed(f"Deleting picture {db_pic.id}"), psycopg.connect(config["DB_URL"], autocommit=True) as db:
                _delete_picture(db_pic)
        else:
            raise RecoverableProcessException(f"Unhandled process task: {db_pic.task}")

        return True


@contextmanager
def _get_next_picture_to_process(config):
    """
    Open a new connection and return the next picture to process
    Note: the picture should be used as a context manager to close the connection when we stop using the returned picture.

    The new connection is needed because we lock the `pictures_to_process` for the whole transaction for another worker not to process the same picture
    """
    with psycopg.connect(config["DB_URL"]) as locking_transaction:
        r = locking_transaction.execute(
            """
		SELECT p.id, pictures_to_process.task, p.metadata
			FROM pictures_to_process
			JOIN pictures p ON p.id = pictures_to_process.picture_id
			ORDER by
				p.nb_errors,
				CASE
					WHEN p.status = 'waiting-for-process' THEN 0
					WHEN p.status = 'waiting-for-delete' THEN 0
					WHEN p.status::text LIKE 'preparing%' THEN 1
				END,
				pictures_to_process.ts
			FOR UPDATE of pictures_to_process SKIP LOCKED
			LIMIT 1
		"""
        ).fetchone()
        if r is None:
            # Nothing to process
            yield None
        else:
            log.debug(f"Processing {r[0]}")

            db_pic = DbPicture(id=str(r[0]), task=r[1], metadata=r[2])
            try:
                yield db_pic

                # Finalize the picture process, set the picture status and remove the picture from the queue process
                _finalize_picture_process(locking_transaction, db_pic)
                log.debug(f"Picture {db_pic.id} processed")
            except RecoverableProcessException as e:
                log.exception(f"Impossible to process picture {db_pic.id} for the moment")
                _mark_process_as_error(locking_transaction, db_pic, e, recoverable=True)
                locking_transaction.commit()
            except InterruptedError as interruption:
                log.error(f"Interruption received, stoping process of picture {db_pic.id}")
                # starts a new connection, since the current one can be corrupted by the exception
                with psycopg.connect(config["DB_URL"], autocommit=True) as t:
                    _mark_process_as_error(t, db_pic, interruption, recoverable=True)
                raise interruption
            except Exception as e:
                log.exception(f"Impossible to process picture {db_pic.id}")
                _mark_process_as_error(locking_transaction, db_pic, e, recoverable=False)
                locking_transaction.commit()
                raise e


def _process_picture(db, config, db_pic: DbPicture):
    _start_process(db, db_pic)

    try:
        processPictureFiles(db, db_pic, config)
        _set_status(db, db_pic.id, "ready")
    finally:
        _finalize_sequence_if_last_picture(db, db_pic)


def _finalize_picture_process(db, pic: DbPicture):
    db.execute(
        """
		DELETE FROM pictures_to_process WHERE picture_id = %(id)s
   		""",
        {"id": pic.id},
    )
    if pic.task == ProcessTask.delete:
        # for picture deletion, we also cleanup the picture from the database
        db.execute("DELETE FROM pictures WHERE id = %s", [pic.id])


def _set_status(db, pic_id: str, status: str):
    db.execute("UPDATE pictures SET status = %s WHERE id = %s", [status, pic_id])


def _start_process(db, pic: DbPicture):
    db.execute(
        """
	UPDATE pictures SET
		status = 'preparing',
		processed_at = NOW()
	WHERE id = %(id)s
	""",
        {"id": pic.id},
    )


def _mark_process_as_error(db, db_pic: DbPicture, e: Exception, recoverable: bool = False):
    if recoverable:
        db.execute(
            """
			UPDATE pictures SET
				status = 'waiting-for-process',
				nb_errors = nb_errors + 1,
				process_error = %(err)s
			WHERE id = %(id)s
			""",
            {"err": str(e), "id": db_pic.id},
        )
    else:
        # on unrecoverable error, we remove the picture from the queue to process
        db.execute(
            """
			WITH pic_to_process_update AS (
				DELETE FROM pictures_to_process
				WHERE picture_id = %(id)s
			)
			UPDATE pictures SET
				status = 'broken',
				nb_errors = nb_errors + 1,
				process_error = %(err)s
			WHERE id = %(id)s
			""",
            {"err": str(e), "id": db_pic.id},
        )


def _finalize_sequence_if_last_picture(db, db_pic: DbPicture):
    r = db.execute(
        """
		SELECT sp.seq_id AS id FROM sequences_pictures AS sp
		WHERE sp.pic_id = %(id)s
	""",
        {"id": db_pic.id},
    ).fetchone()
    if not r:
        raise Exception(f"impossible to find sequence associated to picture {db_pic.id}")

    seqId = r[0]

    is_sequence_finalized = _is_sequence_finalized(db, seqId)
    if not is_sequence_finalized:
        log.debug("sequence not finalized")
        return
    log.debug(f"Finalizing sequence {seqId}")

    with utils.time.log_elapsed(f"Finalizing sequence {seqId}"):
        # Complete missing headings in pictures
        updateSequenceHeadings(db, seqId)

        # Change sequence database status in DB
        # Also generates data in computed columns
        db.execute(
            """
            WITH c AS (
                SELECT
                    ST_MakeLine(ARRAY_AGG(p.geom ORDER BY sp.rank)) AS geom,
                    MIN(p.ts::DATE) AS day,
		            ARRAY_AGG(DISTINCT TRIM(
                        CONCAT(p.metadata->>'make', ' ', p.metadata->>'model')
                    )) AS models,
		            ARRAY_AGG(DISTINCT p.metadata->>'type') AS types
				FROM sequences_pictures sp
				JOIN pictures p ON sp.pic_id = p.id
				WHERE sp.seq_id = %(seq)s
            )
			UPDATE sequences
			SET
                status = 'ready',
                geom = c.geom,
                computed_type = CASE WHEN array_length(c.types, 1) = 1 THEN c.types[1] ELSE NULL END,
	            computed_model = CASE WHEN array_length(c.models, 1) = 1 THEN c.models[1] ELSE NULL END,
	            computed_capture_date = c.day
            FROM c
			WHERE id = %(seq)s
		""",
            {"seq": seqId},
        )

        log.info(f"Sequence {seqId} is ready")


def _is_sequence_finalized(db, seq_id: str):
    statuses = db.execute(
        """
		SELECT p.status FROM pictures p
		JOIN sequences_pictures sp ON sp.pic_id = p.id
		WHERE sp.seq_id = %(id)s
  		;
	""",
        {"id": seq_id},
    ).fetchall()

    for s in statuses:
        if s[0] == "waiting-for-process" or s[0].startswith("preparing"):
            return False
    return True


def _delete_picture(db_pic: DbPicture):
    """Delete a picture from the filesystem"""
    log.debug(f"Deleting picture files {db_pic.id}")
    utils.pictures.removeAllFiles(db_pic.id)
