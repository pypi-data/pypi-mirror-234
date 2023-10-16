from flask import Blueprint, current_app
from flask.cli import with_appcontext
import click
from geovisio import db_migrations

bp = Blueprint("db", __name__)


@bp.cli.command("upgrade")
@with_appcontext
def upgrade():
    """Update database schema"""
    db_migrations.update_db_schema(current_app.config["DB_URL"], force=True)


@bp.cli.command("rollback")
@click.option(
    "--all",
    is_flag=True,
    default=False,
    show_default=True,
    help="rollbacks all migrations instead, meaning everything created by Geovisio in database is deleted",
)
@with_appcontext
def rollback(all):
    """Rollbacks the latest database migration"""
    db_migrations.rollback_db_schema(current_app.config["DB_URL"], all)
