import psycopg
from geovisio import db_migrations, create_app
from . import conftest
import pytest
import psycopg


def test_upgrade_downgrade_upgrade(dburl, app):
    """Tests that schema upgrade -> downgrade -> upgrade"""
    # At startup the database should have an up to date schema
    assert _pictures_table_exists(dburl)

    # downgrade the schema
    db_migrations.rollback_db_schema(dburl, rollback_all=True)

    # after the downgrade there should not be a pictures table anymore
    assert not _pictures_table_exists(dburl)

    # if we apply the schema again we get back the table
    db_migrations.update_db_schema(dburl, force=True)
    assert _pictures_table_exists(dburl)


def test_one_rollback(dburl):
    """Creating an app with an invalid database lead to an error"""
    db_migrations.update_db_schema(dburl, force=True)
    assert _pictures_table_exists(dburl)
    backend = db_migrations.get_yoyo_backend(dburl)
    initial_migrations_applyed = backend.get_applied_migration_hashes()
    assert len(initial_migrations_applyed) > 0

    # downgrade the schema
    db_migrations.rollback_db_schema(dburl, rollback_all=False)

    # we should have one less migration
    migrations_applyed = backend.get_applied_migration_hashes()
    assert len(migrations_applyed) == len(initial_migrations_applyed) - 1


def test_init_bad_db(tmp_path):
    """Creating an app with an invalid database lead to an error"""
    invalidUrl = "postgres://postgres@invalid_host/geovisio"
    with pytest.raises(psycopg.OperationalError):
        create_app(
            {
                "TESTING": True,
                "DB_URL": invalidUrl,
                "FS_URL": str(tmp_path),
                "FS_TMP_URL": None,
                "FS_DERIVATES_URL": None,
                "FS_PERMANENT_URL": None,
            }
        )


@conftest.SEQ_IMGS
def test_db_update_pictures_sequences(datafiles, initSequence, dburl):
    # Checks behaviour of DB migration 20230425_01_gYP77-pictures-edits-triggers.sql
    initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl, autocommit=True) as db:
        seqId, origGeom = db.execute("SELECT id, ST_AsText(geom) AS geom FROM sequences").fetchone()
        assert seqId is not None
        assert (
            origGeom
            == "LINESTRING(1.919185441799137 49.00688961988304,1.919189623000528 49.0068986458004,1.919196360602742 49.00692625960235,1.919199780601944 49.00695484980094,1.919194019996227 49.00697341759938)"
        )

        # Change first picture location -> edits sequence geom
        db.execute(
            "UPDATE pictures SET geom = ST_SetSRID(ST_Point(1, 1), 4326) WHERE id = (SELECT pic_id FROM sequences_pictures WHERE rank = 1 AND seq_id = %s)",
            [seqId],
        )
        newGeom = db.execute("SELECT ST_AsText(geom) AS geom FROM sequences WHERE id = %s", [seqId]).fetchone()[0]

        assert (
            newGeom
            == "LINESTRING(1 1,1.919189623000528 49.0068986458004,1.919196360602742 49.00692625960235,1.919199780601944 49.00695484980094,1.919194019996227 49.00697341759938)"
        )


@conftest.SEQ_IMGS
def test_db_delete_pictures_sequences(datafiles, initSequence, dburl):
    # Checks behaviour of DB migration 20230425_01_gYP77-pictures-edits-triggers.sql
    initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl, autocommit=True) as db:
        seqId, origGeom = db.execute("SELECT id, ST_AsText(geom) AS geom FROM sequences").fetchone()
        assert seqId is not None
        assert (
            origGeom
            == "LINESTRING(1.919185441799137 49.00688961988304,1.919189623000528 49.0068986458004,1.919196360602742 49.00692625960235,1.919199780601944 49.00695484980094,1.919194019996227 49.00697341759938)"
        )

        # Delete first picture in sequence -> edits sequence geom
        db.execute("DELETE FROM sequences_pictures WHERE rank = 1 AND seq_id = %s", [seqId])
        newGeom = db.execute("SELECT ST_AsText(geom) AS geom FROM sequences WHERE id = %s", [seqId]).fetchone()[0]

        assert (
            newGeom
            == "LINESTRING(1.919189623000528 49.0068986458004,1.919196360602742 49.00692625960235,1.919199780601944 49.00695484980094,1.919194019996227 49.00697341759938)"
        )


def _pictures_table_exists(dburl):
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            return cursor.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname = 'pictures')").fetchone()[0]
