import os
from urllib.parse import urlparse
import datetime
import logging


class DefaultConfig:
    API_VIEWER_PAGE = "viewer.html"
    API_MAIN_PAGE = "main.html"
    # we default we keep the session cookie 7 days, users would have to renew their loggin after this
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7).total_seconds()
    API_FORCE_AUTH_ON_UPLOAD = False
    PICTURE_PROCESS_DERIVATES_STRATEGY = "ON_DEMAND"
    API_BLUR_URL = None
    PICTURE_PROCESS_THREADS_LIMIT = 1
    API_PICTURES_LICENSE_SPDX_ID = None
    API_PICTURES_LICENSE_URL = None


def read_config(app, test_config):
    app.config.from_object(DefaultConfig)

    # All env variables prefixed by 'FLASK_' are loaded (and striped from the prefix)
    app.config.from_prefixed_env()

    confFromEnv = [
        # Filesystems parameters
        "FS_URL",
        "FS_TMP_URL",
        "FS_PERMANENT_URL",
        "FS_DERIVATES_URL",
        # Database parameters
        "DB_URL",
        "DB_PORT",
        "DB_HOST",
        "DB_USERNAME",
        "DB_PASSWORD",
        "DB_NAME",
        # API
        "API_BLUR_URL",
        "API_VIEWER_PAGE",
        "API_MAIN_PAGE",
        "API_LOG_LEVEL",
        "API_FORCE_AUTH_ON_UPLOAD",
        "API_PERMANENT_PICTURES_PUBLIC_URL",
        "API_DERIVATES_PICTURES_PUBLIC_URL",
        "API_PICTURES_LICENSE_SPDX_ID",
        "API_PICTURES_LICENSE_URL",
        # Picture process
        "PICTURE_PROCESS_DERIVATES_STRATEGY",
        "PICTURE_PROCESS_THREADS_LIMIT",
        # OAUTH
        "OAUTH_PROVIDER",
        "OAUTH_OIDC_URL",
        "OAUTH_CLIENT_ID",
        "OAUTH_CLIENT_SECRET",
        # Infrastructure
        "INFRA_NB_PROXIES",
    ]
    for e in confFromEnv:
        if os.environ.get(e):
            app.config[e] = os.environ.get(e)

    legacyVariables = {
        "BLUR_URL": "API_BLUR_URL",
        "VIEWER_PAGE": "API_VIEWER_PAGE",
        "MAIN_PAGE": "API_MAIN_PAGE",
        "LOG_LEVEL": "API_LOG_LEVEL",
        "FORCE_AUTH_ON_UPLOAD": "API_FORCE_AUTH_ON_UPLOAD",
        "DERIVATES_STRATEGY": "PICTURE_PROCESS_DERIVATES_STRATEGY",
        "OIDC_URL": "OAUTH_OIDC_URL",
        "CLIENT_ID": "OAUTH_CLIENT_ID",
        "CLIENT_SECRET": "OAUTH_CLIENT_SECRET",
        "NB_PROXIES": "INFRA_NB_PROXIES",
        "SECRET_KEY": "FLASk_SECRET_KEY",
        "SESSION_COOKIE_DOMAIN": "FLASK_SESSION_COOKIE_DOMAIN",
    }
    for legacyKey, newKey in legacyVariables.items():
        l = os.environ.get(legacyKey)
        if l:
            logging.warn(f"A legacy parameter '{legacyKey}' has been set, this has been replaced with '{newKey}")
            app.config[newKey] = l

    # overriding from test_config
    if test_config is not None:
        app.config.update(test_config)

    if "API_LOG_LEVEL" in app.config:
        logging.getLogger("geovisio").setLevel(app.config["API_LOG_LEVEL"].upper())

    # Create DB_URL from separated parameters
    if "DB_PORT" in app.config or "DB_HOST" in app.config or "DB_USERNAME" in app.config or "DB_PASSWORD" in app.config:
        username = app.config.get("DB_USERNAME", "")
        passw = app.config.get("DB_PASSWORD", "")
        host = app.config.get("DB_HOST", "")
        port = app.config.get("DB_PORT", "")
        dbname = app.config.get("DB_NAME", "")

        app.config["DB_URL"] = f"postgres://{username}:{passw}@{host}:{port}/{dbname}"

    if app.config.get("API_BLUR_URL") is not None and len(app.config.get("API_BLUR_URL")) > 0:
        try:
            urlparse(app.config.get("API_BLUR_URL"))
        except:
            raise Exception("Blur API URL is invalid: " + app.config.get("API_BLUR_URL"))
    else:
        app.config["API_BLUR_URL"] = None

    if app.config["PICTURE_PROCESS_DERIVATES_STRATEGY"] not in ["ON_DEMAND", "PREPROCESS"]:
        raise Exception(
            f"Unknown picture derivates strategy: '{app.config['PICTURE_PROCESS_DERIVATES_STRATEGY']}'. Please set to one of ON_DEMAND, PREPROCESS"
        )

    # The default is to use only one only 1 thread to process uploaded pictures
    # if set to 0 no background worker is run, if set to -1 all cpus will be used
    app.config["PICTURE_PROCESS_THREADS_LIMIT"] = _get_threads_limit(app.config["PICTURE_PROCESS_THREADS_LIMIT"])

    # Auth on upload
    app.config["API_FORCE_AUTH_ON_UPLOAD"] = app.config.get("API_FORCE_AUTH_ON_UPLOAD") == "true"

    if app.config.get("WEBP_METHOD") is not None and app.config.get("WEBP_METHOD") != "":
        raise Exception("WEBP_METHOD is deprecated and should not be used")

    if app.config.get("WEBP_CONVERSION_THREADS_LIMIT") is not None and app.config.get("WEBP_CONVERSION_THREADS_LIMIT") != "":
        raise Exception("WEBP_CONVERSION_THREADS_LIMIT is deprecated and should not be used")

    if app.config.get("PICTURE_PROCESS_DERIVATES_STRATEGY") != "PREPROCESS" and app.config.get("API_DERIVATES_PICTURES_PUBLIC_URL"):
        raise Exception(
            "Derivates can be served though another url only if they are all pregenerated, either unset `API_DERIVATES_PICTURES_PUBLIC_URL` or set `PICTURE_PROCESS_DERIVATES_STRATEGY` to `PREPROCESS`"
        )

    if (app.config.get("API_PICTURES_LICENSE_SPDX_ID") is None) + (app.config.get("API_PICTURES_LICENSE_URL") is None) == 1:
        raise Exception(
            "API_PICTURES_LICENSE_SPDX_ID and API_PICTURES_LICENSE_URL should either be both unset (thus the pictures are under a proprietary license) or both set"
        )
    if app.config.get("API_PICTURES_LICENSE_SPDX_ID") is None:
        app.config["API_PICTURES_LICENSE_SPDX_ID"] = "proprietary"
    #
    # Add generated config vars
    #
    app.url_map.strict_slashes = False
    app.config["COMPRESS_MIMETYPES"].append("application/geo+json")
    app.config["EXECUTOR_MAX_WORKERS"] = app.config["PICTURE_PROCESS_THREADS_LIMIT"]
    app.config["EXECUTOR_PROPAGATE_EXCEPTIONS"] = True  # propagate the excecutor's exceptions, to be able to trace them


def _get_threads_limit(param: str) -> int:
    """Computes maximum thread limit depending on environment variables and available CPU.

    Value returned is the minimum between the value and the available number of cpus

    Parameters
    ----------
    param : str
        Read value from environment variable. If value is -1, uses default or CPU count instead

    Returns
    -------
    int
        The appropriate max thread value
    """
    p = int(param)

    nb_cpu = os.cpu_count()
    if p == -1:
        if nb_cpu is None:
            logging.warn("Number of cpu is unknown, using only 1 thread")
            return 1
        return nb_cpu
    return min(p, os.cpu_count() or 1)
