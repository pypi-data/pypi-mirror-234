import logging
import psycopg
from flask import current_app
from geovisio.workers.runner_pictures import updateSequenceHeadings

log = logging.getLogger("geovisio.cli.sequence_heading")


def setSequencesHeadings(sequences, value, overwrite):
    with psycopg.connect(current_app.config["DB_URL"], autocommit=True) as db:
        if len(sequences) == 0:
            log.info("Updating all sequences")
            sequences = [r[0] for r in db.execute("SELECT id FROM sequences").fetchall()]

        for seq in sequences:
            updateSequenceHeadings(db, seq, value, not overwrite)

        log.info("Done processing %s sequences" % len(sequences))
