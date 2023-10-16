from geovisio import create_app


def test_configuration(dburl, tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "DB_URL": dburl,
            "FS_URL": str(tmp_path),
            "OAUTH_PROVIDER": None,
            "FS_TMP_URL": None,
            "FS_PERMANENT_URL": None,
            "FS_DERIVATES_URL": None,
            "API_PICTURES_LICENSE_SPDX_ID": "etalab-2.0",
            "API_PICTURES_LICENSE_URL": "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE",
        }
    )

    with app.test_client() as client:
        r = client.get("/api/configuration")
        assert r.status_code == 200
        assert r.json == {
            "auth": {"enabled": False},
            "license": {
                "id": "etalab-2.0",
                "url": "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE",
            },
        }
