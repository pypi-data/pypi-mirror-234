import typing
from dateutil import tz

from geovisio import errors
import psycopg
from flask import current_app, url_for

STAC_VERSION = "1.0.0"


def removeNoneInDict(val):
    """Removes empty values from dictionnary"""
    return {k: v for k, v in val.items() if v is not None}


def cleanNoneInDict(val):
    """Removes empty values from dictionnary, and return None if dict is empty"""
    res = removeNoneInDict(val)
    return res if len(res) > 0 else None


def dbTsToStac(dbts):
    """Transforms timestamp returned by PostgreSQL into UTC ISO format expected by STAC"""
    return dbts.astimezone(tz.gettz("UTC")).isoformat() if dbts is not None else None


def cleanNoneInList(val: typing.List) -> typing.List:
    """Removes empty values from list"""
    return list(filter(lambda e: e is not None, val))


def accountIdOrDefault(account):
    # Get default account ID
    if account is not None:
        return account.id
    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        accountId = conn.execute("SELECT id FROM accounts WHERE is_default").fetchone()
        if accountId is None:
            raise errors.InternalError("No default account defined, please contact your instance administrator")
        return str(accountId[0])


def get_license_link():
    license_url = current_app.config.get("API_PICTURES_LICENSE_URL")
    if not license_url:
        return None
    return {
        "rel": "license",
        "title": f"License for this object ({current_app.config['API_PICTURES_LICENSE_SPDX_ID']})",
        "href": license_url,
    }


def get_root_link():
    return {
        "rel": "root",
        "type": "application/json",
        "title": "Instance catalog",
        "href": url_for("stac.getLanding", _external=True),
    }
