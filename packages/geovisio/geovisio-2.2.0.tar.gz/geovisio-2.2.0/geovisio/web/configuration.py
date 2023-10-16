import flask
from flask import jsonify

bp = flask.Blueprint("configuration", __name__, url_prefix="/api")


@bp.route("/configuration")
def configuration():
    """Return instance configuration informations
    ---
    tags:
        - Metadata
    responses:
        200:
            description: Information about the instance configuration
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioConfiguration'
    """

    return jsonify(
        {
            "auth": _auth_configuration(),
            "license": _license_configuration(),
        }
    )


def _auth_configuration():
    from geovisio.utils import auth

    if auth.oauth_provider is None:
        return {"enabled": False}
    else:
        return {"enabled": True, "user_profile": {"url": auth.oauth_provider.user_profile_page_url()}}


def _license_configuration():
    l = {"id": flask.current_app.config["API_PICTURES_LICENSE_SPDX_ID"]}
    u = flask.current_app.config.get("API_PICTURES_LICENSE_URL")
    if u:
        l["url"] = u
    return l
