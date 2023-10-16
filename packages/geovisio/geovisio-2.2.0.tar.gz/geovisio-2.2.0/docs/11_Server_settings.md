# Available API settings

GeoVisio API is highly configurable. Depending on your install, you may want to pass settings through different methods:

- Using environment variables (`-e` option for Docker commands)
- Using [python-dotenv](https://github.com/theskumar/python-dotenv) and either using the default `.env` file or providing path to a custom .env file to Flask with the `--env-file` (`-e`) flag (cf [Flask's documentation](https://flask.palletsprojects.com/en/2.2.x/cli/?highlight=dotenv#environment-variables-from-dotenv))

### Mandatory parameters

The following parameters must always be defined, otherwise Geovisio will not run. Note that they are automatically set-up when using __Docker compose__ install.

- `DB_URL` : [connection string](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING) to access the PostgreSQL database. You can alternatively use a set of `DB_PORT`, `DB_HOST`, `DB_USERNAME`, `DB_PASSWORD`, `DB_NAME` parameters to configure database access.
- __Filesystem URLs__ : to set where all kind of files can be stored. You have two alternatives here. Note that all the following variables use the [PyFilesystem format](https://docs.pyfilesystem.org/en/latest/openers.html) (example: `/path/to/pic/dir` for disk storage, `s3://mybucket/myfolder?endpoint_url=https%3A%2F%2Fs3.fr-par.scw.cloud&region=fr-par` for S3 storage)
  - __Single filesystem__ (for simple deployments) : `FS_URL`. In that case, GeoVisio will create automatically three subdirectories there (`tmp`, `permanent` and `derivates`).
  - __Separate filesystems__ (for large scale deployments) : you have then to set 3 filesystems URLs
    - `FS_TMP_URL` : temporary storage for pictures waiting for blurring (if blur is enabled and necessary for a given picture)
    - `FS_PERMANENT_URL` : definitive storage of original, high-definition, eventually blurred pictures
    - `FS_DERIVATES_URL` : cache storage for serving pictures derivates (thumbnail, tiles, standard-definition version)

### Optional parameters

#### API parameters

- `API_BLUR_URL` : URL of the blurring API to use. Keep empty for disabling picture blur. See [blur documentation](./17_Blur_Algorithms.md) for more info.
- `API_MAIN_PAGE` and `API_VIEWER_PAGE` : changes the template to use for display main and viewer page. This should be the name of an existing HTML template in `/geovisio/templates` folder, for example `main.html` or `viewer.html`.
- `API_LOG_LEVEL`: change the logging level. Can be `debug`, `info`, `warn` or `error`. Defaults to `info`.
- `API_FORCE_AUTH_ON_UPLOAD`: require a login before using the upload API (collection creation and picture upload). Values are `true` or `false` (defaults to `false`)

##### Parameters to serve the pictures externaly
- `API_PERMANENT_PICTURES_PUBLIC_URL`: External accessible URL for the permanent pictures (the main HD pictures).
- `API_DERIVATES_PICTURES_PUBLIC_URL`: External accessible URL for the derivates pictures.

For performance, it might be handy to serve the pictures by another mean. It's especially true for S3-based storage, where we can save some time and API ressources by serving the pictures directly from S3. One could also imagine serving the pictures through an Nginx web server or equivalent. If you set those parameters, the given pictures location will be returned by the STAC API in collections and search results. Also, `/api/pictures/:id/:kind` routes will redirect to the external URL.

The pictures must be accessible through those URLs, and stored in the same way as geovisio does.

For example if `FS_PERMANENT_URL` has been set to `s3://geovisio:SOME_VERY_SECRET_KEY@panoramax-pulic/main-pictures?endpoint_url=http%3A%2F%2Flocalhost:9090`, `API_PERMANENT_PICTURES_PUBLIC_URL` needs to be set to `http://localhost:9090/panoramax-public/main-pictures` (notice the `main-pictures` sub directory in both variables).
If only `FS_URL` has been set, the sub directory needs to be specified too (it's `/permanent` for permanent pictures and `/derivates` for the derivates).

For the moment `API_DERIVATES_PICTURES_PUBLIC_URL` is only possible if all the derivates are pregenerated (`PICTURE_PROCESS_DERIVATES_STRATEGY=PREPROCESS`).

###### S3 particularity

For S3-based storage, the easiest way is to set the bucket used for permanent pictures (and derivates if you also want them) to public read.

This can be done with a command like (if `geovisio-storage-public` is the bucket):

```bash
aws s3api put-bucket-acl --bucket geovisio-storage-public --acl public-read
```

Note: This ACL can also be set on bucket creation.

In minio the command is
```bash
mc anonymous set download myminio/geovisio-storage-public;
```

#### Picture's license

- `API_PICTURES_LICENSE_SPDX_ID`: [SPDX](https://spdx.org) id of the picture's license. If none is set, the pictures's license is considered to be `proprietary`. 
- `API_PICTURES_LICENSE_URL`: url to the license.

Only 1 license can be defined per GeoVisio instance, and the API will always link the returned pictures to their license.

The instance's license can also be seen in landing page (`/api`), in a `link` with the relation type `license`, as defined by [STAC specification](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md#license). It can also be accessed through the `/api/configuration` route.

Both those paramaters should be either not defined or defined together.

Note: [Panoramax](https://panoramax.fr/) advise the license to either be:
* [etalab-2.0](https://www.etalab.gouv.fr/licence-ouverte-open-licence/)
* [CC-BY-SA-4.0](https://spdx.org/licenses/CC-BY-SA-4.0.html)

#### Picture processing parameters

- `PICTURE_PROCESS_DERIVATES_STRATEGY` : sets if picture derivates versions should be pre-processed (value `PREPROCESS` to generate all derivates during `process-sequences`) or created on-demand at user query (value `ON_DEMAND` by default to generate at first API call needing the picture).
- `PICTURE_PROCESS_THREADS_LIMIT`: limit the number of thread used to process pictures ([more details in Pictures processing doc](./13_Pictures_processing.md)). Values are: -1 for as many threads as CPU can handle, 0 to disable processing (to run in a separate worker), positive integer for a fixed amount of thread.

#### Flask parameters

All [Flask's parameters](https://flask.palletsprojects.com/en/2.2.x/config/#builtin-configuration-values) can be set by prefixing them with `FLASK_`.

Some notables parameters that a production instance will want to set are:

- `FLASK_SECRET_KEY`: [Flask's secret key](https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY). A secret key used among other things for securely signing the session cookie. For production should be provided with a long random string as stated in flask's documentation.
- `FLASK_PERMANENT_SESSION_LIFETIME`: [Flask's cookie lifetime](https://flask.palletsprojects.com/en/2.2.x/config/#PERMANENT_SESSION_LIFETIME), number of second before a cookie is invalided (and thus time before the user should log in again). Default is 7 days.
- `FLASK_SESSION_COOKIE_DOMAIN`: [Flask's cookie domain](https://flask.palletsprojects.com/en/2.2.x/config/#SESSION_COOKIE_DOMAIN), should be set to the domain of the instance.

#### OAuth configuration

These parameters are useful if you want to enable authentication on your GeoVisio instance. A short summary of available parameters is listed below, and more details about setting up authentication is available in [External identity providers documentation](./12_External_Identity_Providers.md).

- `OAUTH_PROVIDER`: external OAuth provider used to authenticate users. If provided can be either `oidc` (for [OpenIdConnect](https://openid.net/connect/)) or `osm`.
- `OAUTH_OIDC_URL`: if `OAUTH_PROVIDER` is `oidc`, url of the realm to use (example: `http://localhost:3030/realms/geovisio` for a Keycloack deployed locally on port `3030`)
- `OAUTH_CLIENT_ID`: OAuth client id as set in the identity provider
- `OAUTH_CLIENT_SECRET`: OAuth client secret as set in the identity provider

#### Infrastructure

- `INFRA_NB_PROXIES` : tell GeoVisio that it runs behind some proxies, so that it can trust the `X-Forwarded-` headers for URL generation (more details in the [Flask documentation](https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/)).


## Next step

- Check how to [add an external identity provider](./12_External_Identity_Providers.md)
- [Setup picture processing](./13_Pictures_processing.md)
- [Run your classic server](./14_Running_Classic.md)
- [Run using docker](./14_Running_Docker.md)
