import flask
from flask import current_app, url_for, request
from dateutil import tz
import psycopg
from psycopg.rows import dict_row
from authlib.jose import jwt
from authlib.jose.errors import DecodeError
import logging
import uuid
from geovisio.utils import auth
from geovisio import errors, utils


bp = flask.Blueprint("tokens", __name__, url_prefix="/api")


@bp.route("/users/me/tokens", methods=["GET"])
@auth.login_required_with_redirect()
def list_tokens(account):
    """
    List the tokens of a authenticated user
    ---
    tags:
        - Auth
        - Users
    responses:
        200:
            description: the token list
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioTokens'
    """

    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            records = cursor.execute(
                """
                SELECT id, description, generated_at FROM tokens WHERE account_id = %(account)s
            """,
                {"account": account.id},
            ).fetchall()

            tokens = [
                {
                    "id": r["id"],
                    "description": r["description"],
                    "generated_at": r["generated_at"].astimezone(tz.gettz("UTC")).isoformat(),
                    "links": [
                        {
                            "rel": "self",
                            "type": "application/json",
                            "href": url_for("tokens.get_jwt_token", token_id=r["id"], _external=True),
                        }
                    ],
                }
                for r in records
            ]
            return flask.jsonify(tokens)


@bp.route("/users/me/tokens/<uuid:token_id>", methods=["GET"])
@auth.login_required_with_redirect()
def get_jwt_token(token_id: uuid.UUID, account: auth.Account):
    """
    Get the JWT token corresponding to a token id.

    This token will be needed to authenticate others api calls
    ---
    tags:
        - Auth
        - Users
    parameters:
        - name: token_id
          in: path
          description: ID of the token
          required: true
          schema:
            type: string
    responses:
        200:
            description: The token, with it's JWT counterpart.
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/JWToken'
    """

    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            # check token existence
            token = cursor.execute(
                """
                SELECT id, description, generated_at FROM tokens WHERE account_id = %(account)s AND id = %(token)s
                """,
                {"account": account.id, "token": token_id},
            ).fetchone()

            if not token:
                raise errors.InvalidAPIUsage("Impossible to find token", status_code=404)

            jwt_token = _generate_jwt_token(token["id"])
            return flask.jsonify(
                {
                    "jwt_token": jwt_token,
                    "id": token["id"],
                    "description": token["description"],
                    "generated_at": token["generated_at"].astimezone(tz.gettz("UTC")).isoformat(),
                }
            )


@bp.route("/users/me/tokens/<uuid:token_id>", methods=["DELETE"])
@auth.login_required_with_redirect()
def revoke_token(token_id: uuid.UUID, account: auth.Account):
    """
    Delete a token corresponding to a token id.

    This token will not be usable anymore
    ---
    tags:
        - Auth
    parameters:
        - name: token_id
          in: path
          description: ID of the token
          required: true
          schema:
            type: string
    responses:
        200:
            description: The token has been correctly deleted
    """

    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            # check token existence
            res = cursor.execute(
                """
                DELETE FROM tokens WHERE account_id = %(account)s AND id = %(token)s
                """,
                {"account": account.id, "token": token_id},
            )

            token_deleted = res.rowcount

            if not token_deleted:
                raise errors.InvalidAPIUsage("Impossible to find token", status_code=404)
            conn.commit()
            return flask.jsonify({"message": "token revoked"}), 200


@bp.route("/auth/tokens/generate", methods=["POST"])
def generate_non_associated_token():
    """
    Generate a new token, not associated to any user

    The response contains the JWT token, and this token can be saved, but won't be usable until someone claims it with /auth/tokens/claims/:id

    The response contains the claim route as a link with `rel`=`claim`.
    ---
    tags:
        - Auth
    parameters:
        - name: description
          in: query
          description: optional description of the token
          schema:
            type: string
    responses:
        200:
            description: The newly generated token
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/JWTokenClaimable'
    """
    description = request.args.get("description", "")
    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            token = cursor.execute(
                "INSERT INTO tokens (description) VALUES (%(description)s) RETURNING *",
                {"description": description},
            ).fetchone()
            if not token:
                raise errors.InternalError("Impossible to generate a new token")

            jwt_token = _generate_jwt_token(token["id"])
            token = {
                "id": token["id"],
                "jwt_token": jwt_token,
                "description": token["description"],
                "generated_at": token["generated_at"].astimezone(tz.gettz("UTC")).isoformat(),
                "links": [
                    {
                        "rel": "claim",
                        "type": "application/json",
                        "href": url_for("tokens.claim_non_associated_token", token_id=token["id"], _external=True),
                    }
                ],
            }
            return flask.jsonify(token)


@bp.route("/auth/tokens/<uuid:token_id>/claim", methods=["GET"])
@auth.login_required_with_redirect()
def claim_non_associated_token(token_id, account):
    """
    Claim a non associated token

    The token will now be associated to the logged user.

    Only one user can claim a token
    ---
    tags:
        - Auth
    parameters:
        - name: token_id
          in: path
          description: Token ID
          required: true
          schema:
            type: string
    responses:
        200:
            description: The token has been correctly associated to the account
    """
    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            token = cursor.execute(
                """
                SELECT account_id FROM tokens WHERE id = %(token)s
                """,
                {"token": token_id},
            ).fetchone()
            if not token:
                raise errors.InvalidAPIUsage("Impossible to find token", status_code=404)

            associated_account = token["account_id"]
            if associated_account:
                if associated_account != account.id:
                    raise errors.InvalidAPIUsage("Token already claimed by another account", status_code=403)
                else:
                    return flask.jsonify({"message": "token already associated to account"}), 200

            cursor.execute(
                "UPDATE tokens SET account_id = %(account)s WHERE id = %(token)s",
                {"account": account.id, "token": token_id},
            )
            conn.commit()
            return "You are now logged in the CLI, you can upload your pictures", 200


def _generate_jwt_token(token_id: uuid.UUID) -> str:
    """
    Generate a JWT token from a token's id.

    The JWT token will be signed but not encrypted.

    This will makes the jwt token openly readable, but only a geovisio instance can issue validly signed tokens
    """
    header = {"alg": "HS256"}
    payload = {
        "iss": "geovisio",  # Issuer is optional and not used, but it just tell who issued this token
        "sub": str(token_id),
    }
    secret = current_app.config["SECRET_KEY"]

    if not secret:
        raise NoSecretKeyException()

    s = jwt.encode(header, payload, secret)

    return str(s, "utf-8")


def _decode_jwt_token(jwt_token: str) -> dict:
    """
    Decode a JWT token
    """
    secret = current_app.config["SECRET_KEY"]
    if not secret:
        raise NoSecretKeyException()
    try:
        return jwt.decode(jwt_token, secret)
    except DecodeError as e:
        logging.error(f"Impossible to decode token: {e}")
        raise utils.tokens.InvalidTokenException("Impossible to decode token")


class NoSecretKeyException(errors.InternalError):
    def __init__(self):
        msg = "No SECRET_KEY has been defined for the instance (defined by FLASK_SECRET_KEY environment variable), authentication is not possible. Please contact your instance administrator if this is needed."
        super().__init__(msg)
