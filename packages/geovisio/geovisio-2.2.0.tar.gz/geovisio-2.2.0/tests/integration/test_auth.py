from urllib.parse import urlparse, quote
import requests
from ..conftest import SEQ_IMGS
from .conftest import redirect_history, get_keycloak_authenticate_form_url, get_keycloak_logout_form_url


def test_auth_deactivated(client):
    # by default the auth is not activated, so the login routes should not exists
    r = client.get("/api/auth/login")
    assert r.status_code == 501
    assert r.json == {"message": "authentication is not activated on this instance"}
    r = client.get("/api/auth/redirect")
    assert r.status_code == 501
    assert r.json == {"message": "authentication is not activated on this instance"}
    r = client.get("/api/auth/logout")
    assert r.status_code == 501
    assert r.json == {"message": "authentication is not activated on this instance"}


def test_login(auth_client, auth_app):
    response = auth_client.get("/api/auth/login")
    assert response.status_code == 302

    location = response.headers["Location"]
    parsed_url = urlparse(location)

    assert parsed_url.path == "/realms/geovisio/protocol/openid-connect/auth"

    queries = {s.split("=")[0]: s.split("=")[1] for s in parsed_url.query.split("&")}

    assert queries["response_type"] == "code"
    assert queries["code_challenge_method"] == "S256"
    assert queries["client_id"] == "geovisio"
    assert "code_challenge" in queries
    assert "state" in queries
    assert "nonce" in queries
    assert queries["scope"] == "openid"
    assert queries["redirect_uri"] == quote("http://localhost/api/auth/redirect", safe="")


def test_login_with_redirect(server, keycloak, auth_app):
    with requests.session() as s:
        # we do a first query to login (following redirect ) (inside a requests session to keep the cookies)
        login = s.get(f"{server}/api/auth/login", allow_redirects=True)
        login.raise_for_status()
        assert login.status_code == 200

        assert redirect_history(login) == [
            "/api/auth/login",
            "/realms/geovisio/protocol/openid-connect/auth",
        ]

        # Then we authenticate on the keycloak to an already created user (defined in 'keycloak-realm.json')
        url = get_keycloak_authenticate_form_url(login)
        r = s.post(
            url,
            data={"username": "elysee", "password": "my password"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            allow_redirects=True,
        )
        r.raise_for_status()

        # we should be redirected to '/'
        assert r.url == "http://localhost:5005/"

        # user_id/user_name should be accessible via cookies
        # but the cookie should be set by the /redirect route
        assert redirect_history(r) == ["/realms/geovisio/login-actions/authenticate", "/api/auth/redirect", "/"]
        set_cookie = r.history[-1].headers["Set-Cookie"]
        assert "user_id=" in set_cookie
        assert f'user_name={quote("elysee")}' in set_cookie

        # Once logged in, we can query the protected api /api/users/me (using the session cookie)
        user_info = s.get(f"{server}/api/users/me", allow_redirects=True)
        user_info.raise_for_status()
        user_info_json = user_info.json()
        assert "id" in user_info_json
        assert user_info_json["name"] == "elysee"
        assert user_info_json["links"] == [
            {"href": "http://localhost:5005/api/users/me/catalog", "rel": "catalog", "type": "application/json"},
            {"href": "http://localhost:5005/api/users/me/collection", "rel": "collection", "type": "application/json"},
        ]

        # we log out of the server, asking to be redirect to the home page after logout
        logout = s.get(f"{server}/api/auth/logout?next_url=/", allow_redirects=True)
        logout.raise_for_status()
        # this should redirect us to a keycloak logout page
        assert redirect_history(logout) == [
            "/api/auth/logout",
            "/realms/geovisio/protocol/openid-connect/logout",
        ]

        # Note: while the logout has not been confirmed on keycloak side, the user is still logged on geovisio
        r = s.get(f"{server}/api/users/me")
        r.raise_for_status()
        assert r.json()["name"] == "elysee"

        # we confirm the logout on keycloak
        keycloak_logout_url, session_code = get_keycloak_logout_form_url(logout)
        keycloak_logout = s.post(
            f"{keycloak}{keycloak_logout_url}",
            data={"session_code": session_code, "confirmLogout": "Logout"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            allow_redirects=True,
        )
        keycloak_logout.raise_for_status()

        assert redirect_history(keycloak_logout) == [
            "/realms/geovisio/protocol/openid-connect/logout/logout-confirm",
            "/api/auth/post_logout_redirect",
            "/",  # <- the logout redirect to the home page
        ]

        # then the next calls to /protected_api will relauch the oauth dance
        r = s.get(f"{server}/api/users/me", allow_redirects=True)

        assert redirect_history(r) == [
            "/api/users/me",
            "/api/auth/login",
            "/realms/geovisio/protocol/openid-connect/auth",  # <- keycloak ask for log in, we're back in square one
        ]


def test_logout_without_login(server, keycloak, auth_app):
    # a logout without a login should be successful
    login = requests.get(f"{server}/api/auth/logout", allow_redirects=True)
    assert login.status_code == 202


def test_not_logged_sequence_creation(server, keycloak, auth_app):
    r = requests.post(f"{server}/api/collections", json={"title": "Séquence"}, allow_redirects=True)
    assert r.status_code == 401


@SEQ_IMGS
def test_not_logged_picture_upload(server, keycloak, auth_app, datafiles):
    # Note: we can test this on an non existing collection since the authentication is checked before everything else
    r = requests.post(
        f"{server}/api/collections/00000000-0000-0000-0000-000000000000/items",
        data={"position": 1},
        files={"picture": (datafiles / "1.jpg").open("rb")},
    )
    assert r.status_code == 401


@SEQ_IMGS
def test_logged_upload(server, keycloak, auth_app, datafiles):
    with requests.session() as s:
        # we do a first query to login (following redirect ) (inside a requests session to keep the cookies)
        login = s.get(f"{server}/api/auth/login", allow_redirects=True)
        login.raise_for_status()
        assert login.status_code == 200

        assert redirect_history(login) == [
            "/api/auth/login",
            "/realms/geovisio/protocol/openid-connect/auth",
        ]
        # This should ask us for login, and the login has been set as mandatory for upload in the app config
        # Then we authenticate on the keycloak to an already created user (defined in 'keycloak-realm.json')
        url = get_keycloak_authenticate_form_url(login)
        authentication_response = s.post(
            url,
            data={"username": "elysee", "password": "my password"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            allow_redirects=True,
        )
        authentication_response.raise_for_status()
        assert redirect_history(authentication_response) == [
            "/realms/geovisio/login-actions/authenticate",
            "/api/auth/redirect",
            "/",
        ]

        sequence_creation_response = s.post(f"{server}/api/collections", json={"title": "Séquence"}, allow_redirects=True)
        sequence_creation_response.raise_for_status()

        # since we have already been authentified, the cookie should be here, and we should not be asked to authenticate again
        assert sequence_creation_response.history == []

        # the sequence should be associated to the user
        assert sequence_creation_response.json()["providers"] == [{"name": "elysee", "roles": ["producer"]}]

        sequence = sequence_creation_response.headers["Location"]

        # we then upload a pic to the sequence
        upload_response = s.post(f"{sequence}/items", data={"position": 1}, files={"picture": (datafiles / "1.jpg").open("rb")})

        # same, here, no oauth dance needed
        assert upload_response.history == []
        assert upload_response.status_code == 202

        # and we should be able to get those pictures
        pictures_location = upload_response.headers["Location"]

        import time

        time.sleep(1)
        # we do not use the session, we do an unauthenticated call, this should be enough since the pictures are public
        pic_response = requests.get(pictures_location)
        pic_response.raise_for_status()
        j = pic_response.json()

        # the picture should be associated to the user
        assert j["providers"] == [{"name": "elysee", "roles": ["producer"]}]


def _login_as_elysee(session, server):
    login = session.get(f"{server}/api/auth/login", allow_redirects=True)
    login.raise_for_status()
    assert login.status_code == 200

    url = get_keycloak_authenticate_form_url(login)
    authentication_response = session.post(
        url,
        data={"username": "elysee", "password": "my password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        allow_redirects=True,
    )
    authentication_response.raise_for_status()


@SEQ_IMGS
def test_logged_catalog(server, keycloak, auth_app):
    with requests.session() as s:
        # we do a first query to login (following redirect ) (inside a requests session to keep the cookies)
        login = s.get(f"{server}/api/auth/login", allow_redirects=True)
        login.raise_for_status()
        assert login.status_code == 200

        url = get_keycloak_authenticate_form_url(login)
        authentication_response = s.post(
            url,
            data={"username": "elysee", "password": "my password"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            allow_redirects=True,
        )
        authentication_response.raise_for_status()

        sequence_creation_response = s.post(f"{server}/api/collections", json={"title": "Séquence"}, allow_redirects=True)
        sequence_creation_response.raise_for_status()
        sequence_creation_response.headers["Location"]

        # Get user ID
        userDetails = s.get(f"{server}/api/users/me").json()

        url = f"{server}/api/users/{userDetails['id']}/catalog"

        # Check public response for catalog : no sequence
        publicCatalogResp = requests.get(url)

        assert publicCatalogResp.status_code == 200
        publicLinks = [l for l in publicCatalogResp.json()["links"] if l["rel"] == "child"]
        assert len(publicLinks) == 0

        # Check logged response for catalog : 1 preparing sequence
        loggedCatalogResp = s.get(url)

        assert loggedCatalogResp.status_code == 200
        loggedLinks = [l for l in loggedCatalogResp.json()["links"] if l["rel"] == "child"]
        assert len(loggedLinks) == 1
        assert loggedLinks[0]["geovisio:status"] == "waiting-for-process"

        # we should also be able to access the user's collection
        # Check public response for catalog : no sequence
        publicCollectionResp = requests.get(f"{server}/api/users/{userDetails['id']}/collection")
        assert publicCollectionResp.status_code == 200
        publicLinks = [l for l in publicCollectionResp.json()["links"] if l["rel"] == "child"]
        assert len(publicLinks) == 0

        # Check logged response for catalog : 1 preparing sequence
        loggedCollectionResp = s.get(f"{server}/api/users/me/collection")

        assert loggedCollectionResp.status_code == 200
        loggedLinks = [l for l in loggedCollectionResp.json()["links"] if l["rel"] == "child"]
        assert len(loggedLinks) == 1
        assert loggedLinks[0]["geovisio:status"] == "waiting-for-process"


def test_configuration_with_auth(server, keycloak, auth_app):
    r = requests.get(f"{server}/api/configuration")
    r.raise_for_status()

    assert r.json() == {
        "auth": {"enabled": True, "user_profile": {"url": f"{keycloak}/realms/geovisio/account/#/personal-info"}},
        "license": {"id": "proprietary"},
    }

    # we should be able to query this page
    p = requests.get(r.json()["auth"]["user_profile"]["url"])
    p.raise_for_status()


@SEQ_IMGS
def test_patch_item_with_auth(server, keycloak, datafiles, auth_app):
    with requests.session() as s:
        _login_as_elysee(s, server)

        sequence_creation_response = s.post(f"{server}/api/collections", json={"title": "Séquence"}, allow_redirects=True)
        sequence_creation_response.raise_for_status()
        sequence = sequence_creation_response.headers["Location"]

        upload_response = s.post(f"{sequence}/items", data={"position": 1}, files={"picture": (datafiles / "1.jpg").open("rb")})

        pictures_location = upload_response.headers["Location"]

        response = s.get(pictures_location)
        assert response.status_code == 102

        import time

        time.sleep(2)

        # Make picture not visible
        response = s.patch(pictures_location, data={"visible": "false"})
        assert response.status_code == 200
        assert response.json()["properties"]["geovisio:status"] == "hidden"

        # Try to retrieve hidden picture as public
        response = requests.get(pictures_location)
        assert response.status_code == 404

        # But works as 'elysee'
        response = s.get(pictures_location)
        assert response.status_code == 200
