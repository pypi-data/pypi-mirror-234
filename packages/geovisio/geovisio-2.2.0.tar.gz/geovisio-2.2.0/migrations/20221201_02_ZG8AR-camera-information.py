"""
Camera metadata
"""

from yoyo import step
import json
import requests

__depends__ = {"20221201_01_wpCGc-initial-schema"}


def apply_step(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
CREATE TABLE cameras(
	model VARCHAR PRIMARY KEY,
	sensor_width FLOAT NOT NULL
);

CREATE INDEX cameras_model_idx ON cameras USING GIST(model gist_trgm_ops);
"""
        )
        print("Initializing cameras metadata...")
        sensorsUrl = "https://github.com/mapillary/OpenSfM/raw/main/opensfm/data/sensor_data.json"
        sensorsData = requests.get(sensorsUrl)
        sensorsJson = json.loads(sensorsData.text)

        with cursor.copy("COPY cameras(model, sensor_width) FROM STDIN") as copy:
            for sensor in sensorsJson.items():
                copy.write_row(sensor)
            print("Cameras metadata initialized")


def rollback_step(conn):
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS cameras;")


steps = [step(apply_step, rollback_step)]
