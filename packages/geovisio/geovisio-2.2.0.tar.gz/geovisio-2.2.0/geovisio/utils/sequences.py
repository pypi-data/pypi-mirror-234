import psycopg
from flask import current_app
from psycopg.types.json import Jsonb


def createSequence(metadata, accountId) -> str:
    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            # Add sequence in database
            seqId = cursor.execute(
                "INSERT INTO sequences(account_id, metadata) VALUES(%s, %s) RETURNING id", [accountId, Jsonb(metadata)]
            ).fetchone()

            # Make changes definitive in database
            conn.commit()

            if seqId is None:
                raise Exception(f"impossible to insert sequence in database")
            return seqId[0]
