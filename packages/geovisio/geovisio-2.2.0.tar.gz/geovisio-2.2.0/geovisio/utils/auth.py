import flask
from flask import current_app, url_for, session, redirect, request
from functools import wraps
from authlib.integrations.flask_client import OAuth
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any
from typing import Optional


ACCOUNT_KEY = "account"  # Key in flask's session with the account's information

oauth = OAuth()
oauth_provider = None


@dataclass
class OAuthUserAccount(object):
    id: str
    name: str


class OAuthProvider(ABC):
    """Base class for oauth provider. Need so specify how to get user's info"""

    name: str
    client: Any

    def __init__(self, name, **kwargs) -> None:
        super(OAuthProvider, self).__init__()
        self.name = name
        self.client = oauth.register(name=name, **kwargs)

    @abstractmethod
    def get_user_oauth_info(self, tokenResponse) -> OAuthUserAccount:
        pass

    def logout_url(self):
        return None

    def user_profile_page_url(self):
        """
        URL to a user settings page.
        This URL should point to a web page where user can edit its password or email address,
        if that makes sense regardinz your GeoVisio instance.

        This is useful if your instance has its own specific identity provider. It may not be used if you rely on third-party auth provider.
        """
        return None


class OIDCProvider(OAuthProvider):
    def __init__(self, *args, **kwargs) -> None:
        super(OIDCProvider, self).__init__(*args, **kwargs)

    def get_user_oauth_info(self, tokenResponse) -> OAuthUserAccount:
        # user info is alway provided by oidc provider, nothing to do
        # we only need the 'sub' (subject) claim
        oidc_userinfo = tokenResponse["userinfo"]
        return OAuthUserAccount(id=oidc_userinfo["sub"], name=oidc_userinfo["preferred_username"])


class KeycloakProvider(OIDCProvider):
    def __init__(self, keycloack_realm_user, client_id, client_secret) -> None:
        super().__init__(
            name="keycloak",
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url=f"{keycloack_realm_user}/.well-known/openid-configuration",
            client_kwargs={
                "scope": "openid",
                "code_challenge_method": "S256",  # enable PKCE
            },
        )
        self._logout_url = f"{keycloack_realm_user}/protocol/openid-connect/logout?client_id={client_id}"
        self._user_profile_page_url = f"{keycloack_realm_user}/account/#/personal-info"

    def logout_url(self):
        return self._logout_url

    def user_profile_page_url(self):
        return self._user_profile_page_url


class OSMOAuthProvider(OAuthProvider):
    def __init__(self, oauth_key, oauth_secret) -> None:
        super().__init__(
            name="osm",
            client_id=oauth_key,
            client_secret=oauth_secret,
            api_base_url="https://api.openstreetmap.org/api/0.6/",
            authorize_url="https://www.openstreetmap.org/oauth2/authorize",
            access_token_url="https://www.openstreetmap.org/oauth2/token",
            client_kwargs={
                "scope": "read_prefs",
            },
        )

    def get_user_oauth_info(self, tokenResponse) -> OAuthUserAccount:
        """Get the id/name of the logged user from osm's API
        cf. https://wiki.openstreetmap.org/wiki/API_v0.6
        Args:
                        tokenResponse: access token to the OSM api, will be automatically used to query the OSM API

        Returns:
                        OAuthUserAccount: id and name of the account
        """
        details = self.client.get("user/details.json")
        details.raise_for_status()
        details = details.json()
        return OAuthUserAccount(id=str(details["user"]["id"]), name=details["user"]["display_name"])


def make_auth(app):
    def ensure(*app_config_key):
        missing = [k for k in app_config_key if k not in app.config]
        if missing:
            raise Exception(f"To setup an oauth provider, you need to provide {missing} in configuration")

    global oauth_provider, oauth
    oauth = OAuth()
    if app.config.get("OAUTH_PROVIDER") == "oidc":
        ensure("OAUTH_OIDC_URL", "OAUTH_CLIENT_ID", "OAUTH_CLIENT_SECRET")

        oauth_provider = KeycloakProvider(
            app.config["OAUTH_OIDC_URL"],
            app.config["OAUTH_CLIENT_ID"],
            app.config["OAUTH_CLIENT_SECRET"],
        )
    elif app.config.get("OAUTH_PROVIDER") == "osm":
        ensure("OAUTH_CLIENT_ID", "OAUTH_CLIENT_SECRET")

        oauth_provider = OSMOAuthProvider(
            app.config["OAUTH_CLIENT_ID"],
            app.config["OAUTH_CLIENT_SECRET"],
        )
    else:
        raise Exception(
            "Unsupported OAUTH_PROVIDER, should be either 'oidc' or 'osm'. If you want another provider to be supported, add a subclass to OAuthProvider"
        )
    oauth.init_app(app)

    return oauth


@dataclass
class Account(object):
    id: str
    name: str
    oauth_provider: str
    oauth_id: str


def login_required():
    """Check that the user is logged, and abort if it's not the case"""

    def actual_decorator(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            account = get_current_account()
            if not account:
                return flask.abort(flask.make_response(flask.jsonify(message="Authentication is mandatory"), 401))
            kwargs["account"] = account

            return f(*args, **kwargs)

        return decorator

    return actual_decorator


def login_required_by_setting(mandatory_login_param):
    """Check that the user is logged, and abort if it's not the case

    Args:
            mandatory_login_param (str): name of the configuration parameter used to decide if the login is mandatory or not
    """

    def actual_decorator(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            account = get_current_account()
            if not account and current_app.config[mandatory_login_param]:
                return flask.abort(flask.make_response(flask.jsonify(message="Authentication is mandatory"), 401))
            kwargs["account"] = account

            return f(*args, **kwargs)

        return decorator

    return actual_decorator


def login_required_with_redirect():
    """Check that the user is logged, and redirect if it's not the case"""

    def actual_decorator(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            account = get_current_account()
            if not account:
                if "OAUTH_PROVIDER" not in current_app.config:
                    return flask.abort(
                        flask.make_response(
                            flask.jsonify(message="Authentication has not been activated in this instance, impossible to log in."), 403
                        )
                    )
                return redirect(url_for("auth.login", next_url=request.url))
            kwargs["account"] = account

            return f(*args, **kwargs)

        return decorator

    return actual_decorator


def isUserIdMatchingCurrentAccount():
    """Check if given user ID matches the currently logged-in account"""

    def actual_decorator(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            account = get_current_account()
            userId = kwargs.get("userId")
            kwargs["userIdMatchesAccount"] = account is not None and userId is not None and account.id == str(userId)
            return f(*args, **kwargs)

        return decorator

    return actual_decorator


class UnknowAccountException(Exception):
    status_code = 401

    def __init__(self):
        msg = f"No account with this oauth id is know, you should login first"
        super().__init__(msg)


class LoginRequiredException(Exception):
    status_code = 401

    def __init__(self):
        msg = f"You should login to request this API"
        super().__init__(msg)


def get_current_account():
    """Get the authenticated account information.

    This account is either stored in the flask's session or retrieved with the Bearer token passed with an `Authorization` header.

    The flask session is usually used by browser, whereas the bearer token is handly for non interactive uses, like curls or CLI usage.

    Returns:
                    Account: the current logged account, None if nobody is logged
    """
    if ACCOUNT_KEY in session:
        session_account = Account(**session[ACCOUNT_KEY])

        return session_account

    bearer_token = _get_bearer_token()
    if bearer_token:
        from geovisio.utils import tokens

        return tokens.get_account_from_jwt_token(bearer_token)

    return None


def _get_bearer_token() -> Optional[str]:
    """
    Get the associated bearer token from the `Authorization` header

    Raises:
            tokens.InvalidTokenException: if the token is not a bearer token
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    if not auth_header.startswith("Bearer "):
        from geovisio.utils.tokens import InvalidTokenException

        raise InvalidTokenException("Only Bearer token are supported")
    return auth_header.split(" ")[1]
