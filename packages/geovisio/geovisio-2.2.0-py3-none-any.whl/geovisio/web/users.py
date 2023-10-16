import flask
from geovisio.utils import auth

bp = flask.Blueprint("user", __name__, url_prefix="/api/users")


@bp.route("/me")
@auth.login_required_with_redirect()
def getUserInfo(account):
    """Get current logged user informations
    ---
    tags:
        - Users
    responses:
        200:
            description: Information about the logged account
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioUser'
    """
    response = {
        "id": account.id,
        "name": account.name,
        "links": [
            {"rel": "catalog", "type": "application/json", "href": flask.url_for("user.getCatalog", _external=True)},
            {"rel": "collection", "type": "application/json", "href": flask.url_for("user.getCollection", _external=True)},
        ],
    }
    return flask.jsonify(response)


@bp.route("/me/catalog")
@auth.login_required_with_redirect()
def getCatalog(account):
    """Get current logged user catalog
    ---
    tags:
        - Users
        - Sequences
    responses:
        200:
            description: the Catalog listing all sequences associated to given user. Note that it's similar to the user's colletion, but with less metadata since a STAC collection is an enhanced STAC catalog.
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCatalog'
    """
    return flask.redirect(flask.url_for("stac.getUserCatalog", userId=account.id, _external=True))


@bp.route("/me/collection")
@auth.login_required_with_redirect()
def getCollection(account):
    """Get current logged user collectoin
    ---
    tags:
        - Users
        - Sequences
    responses:
        200:
            description: the Collection listing all sequences associated to given user. Note that it's similar to the user's catalog, but with more metadata since a STAC collection is an enhanced STAC catalog.
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollection'
    """
    return flask.redirect(flask.url_for("stac_collections.getUserCollection", userId=account.id, _external=True))
