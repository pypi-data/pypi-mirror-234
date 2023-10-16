# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Before _1.6.0_, [Viewer](https://gitlab.com/geovisio/web-viewer) was embed in this repository, so this changelog also includes Viewer features until the split.

## [Unreleased]

## [2.2.0] - 2023-10-10

### Changed
- [GeoPic Tag Reader](https://gitlab.com/geovisio/geo-picture-tag-reader) updated to 0.4.1 to embed stronger checks on picture coordinates.

### Fixed
- If a picture was having invalid coordinates in its EXIF tags, geometry in database was landing outside of WGS84 bounding box, and `GET /api` returned an invalid spatial extent. API now limits returned bounding box to maximum authorized value for WGS84 projection.

### Added
- a new route: `/api/users/:id/collection` that returns a collection of all the users's collections (can also be accessed with `/api/users/me/collection` with authentication). It's similar to `/api/users/:id/catalog` but with more metadata since a STAC collection is an enhanced STAC catalog.

## [2.1.1] - 2023-09-05

### Added
- On picture upload, some metadata can be passed through HTTP request parameters instead of being read from picture file EXIF tags. Available metadata overrides are: GPS coordinates, capture time and picture type. This allows API clients to handle a wider set of input files (for example GeoPackage, CSV, Shapefile...) without needing to insert all information into picture file.
- To make API compatible with a broader range of clients, the `GET /api/collections/{collectionId}/items` route has new metadata in its `properties` field (`geovisio:producer`, `geovisio:image`, `geovisio:thumbnail`). These properties are duplicated regarding STAC standard (which puts them directly at _Feature_ level) to allow compatibility with clients which only reads metadata from `properties` field (like uMap or QGIS).
- A favicon is shown in default API pages.
- A RSS feed is now offered to list recently uploaded collections, it can be accessed through `GET /api/collections?format=rss` (or with `Accept: application/rss+xml` HTTP request header).
- Collections list (`/api/collections`) now also supports search with `bbox` and `datetime` parameters, as proposed in [STAC _Collection Search_ extension](https://github.com/stac-api-extensions/collection-search).

### Changed
- The Docker compose file `docker-compose-full.yml` now embeds [GeoVisio Website](https://gitlab.com/geovisio/website), available on `localhost:3000`.

### Fixed
- Database migration `20230720_01_EyQ0e-sequences-summary` was having a failing SQL request, causing invalid computed sequence metadata being present in database.
- Search parameters `collections` and `ids` for `/api/search` route where not correctly handled when passed through `POST` JSON body.


## [2.1.0] - 2023-07-20

### Added
- A way to customize the picture's license. If none is set, the pictures's license is considered to be proprietary.
- A new route `PATCH /api/collections/:cid` is offered to change visibility of a sequence
- A way to call the vector tiles as an authenticated user. It is mainly used to be able to see objects only visible for this user.
- A `hidden` property in the vector tiles, to mark a sequence or picture as only visible for the owner of this sequence or picture. If the property is not set, the object is visible by all
- A new route `DELETE /api/collections/:cid` is offered to delete a collection. The deletion is done asynchronously.
- A new route `DELETE /api/collections/:cid/items/:id` is offered to delete a picture
- [OpenAPI](https://swagger.io/specification/) conformance tests are now automatically run through `tests/test_api_conformance.sh` script
- [Support of pagination](https://github.com/radiantearth/stac-api-spec/tree/main/ogcapi-features#item-pagination) for `GET /api/collections/:cid/items` API route (`first, last, prev, next` relation types)
  * also support a `?withPicture=:picture_id` query paramater to ask for a page with a specific picture in it
- Add a `flask sequences reorder` subcommand to reorder all or some sequences using the picture's datetime.
- [Support of pagination](https://github.com/radiantearth/stac-api-spec/blob/master/ogcapi-features/README.md#collection-pagination) for `GET /api/collections` API route (`first, last, prev, next` relation types), with a default limit to 100 sequences retrieved per call
- Add 2 optional parameters to the `GET /api/collections` api: `created_after`/`created_before` used to filter the collection by their creation date.
- New properties available in vector tiles for sequences (account ID, camera model, picture type, capture day) and pictures (account ID, camera model, picture type).

### Changed
- Docker compose files now use `latest` API image instead of `develop`
- In default pages (`/` and `/viewer.html`), web viewer version is now synced to current API version instead of develop
- Algorithm used for generating smaller versions of pictures changed from _NEAREST_ to _HAMMING_ for better results
- API documentation and specifications moved to `/api/docs/swagger` and `/api/docs/specs.json`, and with improved readability of their content
- Now heading are recomputed if set to 0 because some camera use this value by default
- Hidden pictures will now always be served through the API to be able to check permissions.

### Fixed
- Raw picture bytes are sent to blurring API instead of Pillow-based version, avoiding various issues (too large files, missing EXIF)
- Docker-compose files are now compatible with MacOS (replaced `network_mode: host` to use a more classic approach)
- Some CORS HTTP headers were missing in API responses to allow client send credentials


## [2.0.2] - 2023-06-08

### Added
- [STAC extension "stats"](https://github.com/stac-extensions/stats) is used on routes `/collections` and `/collections/:id` to add number of items contained in given collection (property `stats:items.count`).
- A new route `PATCH /api/collections/:cid/items/:id` is offered to change visibility of a picture
- A new route `GET /api/collections/:cid/thumbnail.jpg` is offered to get the thumbnail of the first visible picture of a collection
- API landing page (`/api`) better advertises its capabilities:
  - [Web Map Links](https://github.com/stac-extensions/web-map-links) STAC extension is used for vector tiles availability.
  - Custom-defined links `item-preview` and `collection-preview` offer a template URL to have direct access to a thumbnail for either a sequence or a single picture.
- A `geovisio:status` field is added in various API responses (mainly in `/api/collections/:col_id/items` and `/api/collections/:col_id/items/:item_id`) to know if a picture is visible or not. This is mainly useful when retrieving your own sequences and pictures as an authenticated user.
- In vector tiles, in pictures layer, list of sequences associated to a picture is made available in its properties as `sequences` array.

### Changed
- Improved deployment docs
- API route `/users/:userId/catalog/` changes:
  - It sends different results according if you're looking for your own catalog as an authenticated user, or if you're looking to another user catalog. Your own catalog embeds all sequences, others catalogs only display publicly-available sequences.
  - It embeds more properties in a link to child sequence: title, ID, items count, start/end date

### Fixed
- Even if not necessary anymore (with the introduction of user tokens), API was checking if `OAUTH_PROVIDER` was set if you wanted to enable `API_FORCE_AUTH_ON_UPLOAD`.


## [2.0.1] - 2023-05-24

### Added
- Added a `/api/configuration` endpoint with the API configuration. This endpoint is meant to provided easy frontend configuration.
- Support of Bearer token authorization. This should improve API authentication when a browser is not available, for example in usage with the [CLI](https://gitlab.com/geovisio/cli).
- The HTTP response header `Access-Control-Expose-Headers` is added to STAC response to allow web browser using the `Location` header.
- Add API routes to generate a claimable token. By default, it's not associated to any account (created by a `POST` on `/api/auth/tokens/generate`). To be usable, this token needs to be associated to an account via a authenticated call on `/api/auth/tokens/<uuid:token_id>/claim`. This offers a nicer authentication flow on the CLI.
- Add an API route to revoke a token, a `DELETE` on `/api/users/me/tokens/<uuid:token_id>`

### Changed
- Blur picture is called with a `keep=1` URL query parameter (for a coming migration to [SGBlur](https://github.com/cquest/sgblur)) to keep original unblurred parts on blur API side.
- [GeoPic Tag Reader](https://gitlab.com/geovisio/geo-picture-tag-reader) updated to 0.1.0 : more EXIF tags are supported for date, heading, GPS coordinates. Also, warnings issued by reader are stored in GeoVisio API database.
- All sources have been moved from `./server/src` to `./geovisio` (thanks to [Nick Whitelegg](https://gitlab.com/nickw1)). Thus, sources are now imported as `import geovisio` instead of `import src`.

### Fixed
- Standard-definition pictures now embeds full EXIF tags from original picture
- Docker compose files were failing if some services were just a bit too long to start


## [2.0.0] - 2023-04-28

### Added
- Add [Providers](https://github.com/radiantearth/stac-api-spec/blob/main/stac-spec/item-spec/common-metadata.md#provider-object) to stac items and collections to have information about the account owning the collection/item
- Add the capability to require a login before creating a sequence and uploading pictures to it
- Add a `/api/users/me` route to get logged in user information, and a `/api/users/me/catalog` to get the catalog of the logged in user.
- Some background picture processes can be run using `flask picture-worker`. Those workers can run on a different server than the API
- Server settings to limit maximum threads: `PICTURE_PROCESS_THREADS_LIMIT`. Set to -1 to use all available threads, 0 to have no background threads at all (use this is you want another server running `flask picture-worker`)
- Added the collection's status in the `/geovisio_status` route.
- Use the python logger instead of print. The logging level can be changed with the `LOG_LEVEL` environment variable.
- The picture upload API route offers a `isBlurred=true` form parameter to skip blurring picture (if it is already blurred by author)
- All read EXIF metadata from pictures is stored in `pictures` tables in a `exif` column
- Filesystem storage can be also configured into 3 different variables for a more flexible storage: `FS_TMP_URL`, `FS_PERMANENT_URL`, `FS_DERIVATES_URL`
- STAC API responses gives `created` time for sequences and pictures (when it was imported), and `updated` time for sequences (last edit time)

### Changed
- Move auth apis from `/auth` to `/api/auth`.
- Docker image moved to [`geovisio/api`](https://hub.docker.com/r/geovisio/api) (was previously `panieravide/geovisio`)
- After the OAuth process launched by `/api/auth/login`, we are redirected to the home page
- Pictures blurring is now __externalized__ : GeoVisio API calls a third-party _blurring API_ (which is [available as a part of the whole GeoVisio stack](https://gitlab.com/geovisio/blurring)) instead of relying on internal scripts. This allows more flexible deployments. This changes settings like `BLUR_STRATEGY` which becomes `BLUR_URL`.
- Reading of EXIF tags from pictures is now done by a separated library called [Geopic Tag Reader](https://gitlab.com/geovisio/geo-picture-tag-reader).
- Pictures derivates are now (again) stored in JPEG format. API still can serve images in both JPEG or WebP formats, but with improved performance if using JPEG
- Thumbnail image is always generated, no matter of `DERIVATES_STRATEGY` value, for better performance on viewer side
- When picture blurring is enabled, original uploaded image is not stored, only blurred version is kept
- Change several environement variables to ensure coherence (but the retrocompatibility has been maintained)
  * `BLUR_URL` => `API_BLUR_URL`
  * `VIEWER_PAGE` => `API_VIEWER_PAGE`
  * `MAIN_PAGE` => `API_MAIN_PAGE`
  * `LOG_LEVEL` => `API_LOG_LEVEL`
  * `FORCE_AUTH_ON_UPLOAD` => `API_FORCE_AUTH_ON_UPLOAD`
  * `DERIVATES_STRATEGY` => `PICTURE_PROCESS_DERIVATES_STRATEGY`
  * `OIDC_URL` => `OAUTH_OIDC_URL`
  * `CLIENT_ID` => `OAUTH_CLIENT_ID`
  * `CLIENT_SECRET` => `OAUTH_CLIENT_SECRET`
  * `NB_PROXIES` => `INFRA_NB_PROXIES`
- Commands `flask set-sequences-heading` and `flask cleanup` now takes in input sequences IDs instead of sequences folder names
- Command `flask cleanup` offers to delete original images, and can't delete blur masks anymore (as they are not used anymore)
- The python files are now directly in the working directory of the docker image, no longer in a `./server` sub directory. It should be transparent for most users though.

### Fixed
- Tests were failing when using PySTAC 1.7.0 due to unavaible `extra_fields['id']` on links
- EXIF tags filled with blank spaces or similar characters were not handled as null, causing unnecessary errors on pictures processing (issues [#65](https://gitlab.com/geovisio/api/-/issues/65) and [#66](https://gitlab.com/geovisio/api/-/issues/66))
- Make sure picture EXIF orientation is always used and applied ([#71](https://gitlab.com/geovisio/api/-/issues/71))
- Updates on DB table `pictures` and deletes on DB table `sequences_pictures` now updates `sequences.geom` column automatically

### Removed
- Removed `SERVER_NAME` from configuration. This parameter was used for url generation, but was causing problems in some cases (cf. [related issue](https://gitlab.com/geovisio/geovisio/-/issues/48))
- Removed `BACKEND_MODE` from configuration. This parameter was only used in docker/kubernetes context and can be changed from a environment variable to an argument.
- Removed the `process-sequences` and `redo-sequences` flask's targets. All pictures upload now pass through the API, and the easiest way to do this is to use [geovisio cli](https://gitlab.com/geovisio/cli).
- Removed the `fill-with-mock-data` Flask command
- Pictures and sequences file paths are removed from database (all storage is based on picture ID)


## [1.5.0] - 2023-02-10

### Added
- Viewer sets [various hash URL parameters](./docs/22_Client_URL_settings.md) to save map position, picture ID, focused element and viewer position
- The pictures and sequences are now linked to an account. When importing the sequence, pictures and sequences are either associated to the instance's default account or to the provided `account-name` in the metadata.txt file (cf [documentation](./docs/12_Pictures_storage.md#metadatatxt-configuration-file))
- New index in database for pictures timestamps (to speed up temporal queries)
- API offers an `extent` property in its landing page (`/api/` route), defining spatio-temporal extent of available data (in the same format as [STAC Collection extent](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md#extent-object)). Note that this is __not STAC-standard__, it may evolve following [ongoing discussions](https://github.com/radiantearth/stac-spec/issues/1210).
- Documentation to [deploy GeoVisio API on Scalingo](./docs/10_Install_Scalingo.md)
- Authentication handling using an external OAuth2 provider. See the [external identity provider documentation](./docs/12_External_Identity_Providers.md) and [Api usage documentation](./docs/16_Using_API.md#authentication)
- Refactor docker-compose files. Removal of the docker-compose-dev.yaml (integrated in the main docker-compose.yml file), and add of several other docker-compose files in the [docker/](./docker/) directory.

### Changed
- Viewer displays picture date when picture is focused instead of static text "GeoVisio"
- Conformance of API against STAC specifications is improved:
  - List of conformance URLs is more complete
  - Collection temporal extent is always returned in UTC timezone
  - Summaries of some fields are provided in collections
  - Links in collections have now titles
  - Empty fields are now not returned at all, instead of returned with `null` values
  - Content types for GeoJSON routes are now set precisely
  - Providers list is set to an empty array for collections
  - Listing of all users catalogs in main catalog (landing)
  - `/search` route supports `POST` HTTP method

### Fixed
- Some picture metadata fields were duplicated in database (existing both as standalone columns and in `metadata` field), now `metadata` only contains info not existing in other columns.
- More robust testing of `None` values for server settings

### Removed
- The configuration cannot be stored in a `config.py` file anymore, either use environment variables, or install [python-dotenv](https://github.com/theskumar/python-dotenv) (it's in the requirements-dev.txt file) and persist the variables in either the default `.env` file or a custom `*.env` file (like `prod.env`) and pass this file to flask with the `--env-file` (or `-e`) option.

```bash
flask --env-file prod.env run
```
- The `TEST_DB_URL` environment variable is no longer available for the tests, replaced by the standard `DB_URL`


## [1.4.1] - 2023-02-01

### Fixed
- Improve checks to avoid failures due to invalid `WEBP_METHOD` parameter


## [1.4.0] - 2023-01-04

__About upgrading from versions <= 1.3.1__ : many changes have been done on storage and settings during pictures import, to avoid issues you may do a full re-import of your pictures and sequences. This can be done with following command (to adapt according to your setup):

```bash
cd server/
FLASK_APP="src" flask cleanup
FLASK_APP="src" flask process-sequences
```

### Added
- Home and viewer pages can be changed using `MAIN_PAGE` and `VIEWER_PAGE` settings (thanks to Nick Whitelegg)
- Docker compose file for local development (in complement of existing file which uses pre-built Docker image)
- Explicitly document that database should be in UTF-8 encoding (to avoid [binary string issues with Psycopg](https://www.psycopg.org/psycopg3/docs/basic/adapt.html#strings-adaptation))
- Server tests can be run through Docker
- API can serve pictures in both JPEG and WebP formats
- Viewer now supports WebP assets, and are searched for in priority
- Mock images and sequences can be generated for testing with `fill-mock-data` server command (thanks to Antoine Desbordes)
- Viewer map updates automatically URL hash part with a `map` string
- API map tiles offers a `sequences` layer for display sequences paths
- Database migrations are handled with the [Yoyo migrations framework](https://ollycope.com/software/yoyo/latest/)

### Changed
- Derivates picture files are now by default generated on-demand on first API request. Pre-processing of derivates (old method) can be enabled using `DERIVATES_STRATEGY=PREPROCESS` setting when calling `process-sequences` command.
- Internal storage format for pictures is now WebP, offering same quality with reduce disk usage.
- If not set, `SERVER_NAME` defaults to `localhost.localdomain:5000`
- Reduced size of Docker image by limiting YOLOv6 repository download and removing unused torchaudio dependency
- Server dependencies are now separated in 3 pip requirements files for faster CI: `requirements.txt`, `requirements-dev.txt` and `requirements-blur.txt`
- During sequences processing, ready pictures can be shown and queried even if whole sequences is not ready yet
- Improved CLI commands documentation (which appears using `FLASK_APP="src" flask --help`)
- Heading in pictures metadata is now optional, and is set relatively to sequence movement path if missing
- New CLI command `set-sequences-heading` allows user to manually change heading values
- Viewer supports STAC items not having `view:azimuth` property defined
- All documentation files are now in `docs/` folder, with better readability and consistency

### Fixed
- Some sequences names were bytestring instead of string, causing some STAC API calls to fail
- YOLOv6 release number is now fixed in code to avoid issues in downloaded models
- Docker-compose files explicitly wait for PostgreSQL database to be ready to prevent random failures
- With `COMPROMISE` blur strategies, image not needing blurring failed
- URL to API documentation written without trailing `/` was not correctly handled
- Pictures with partial camera metadata are now correctly handled

### Removed
- No progressive JPEG is used anymore for classic (non-360°) HD pictures.


## [1.3.1] - 2022-08-03

### Added
- A cleaner progress bar (tqdm) is used for progress of sequences processing
- Picture heading is also read from `PoseHeadingDegrees` XMP EXIF tag

### Changed
- Pictures derivates folder is renamed from `gvs_derivates` to `geovisio_derivates` for better readability
- Sequences folder can skip processing if their name starts with either `ignore_`, `gvs_` or `geovisio_`
- Status of pictures and sequences is now visible in real-time in database (instead of one transaction commited at the end of single sequence processing)

### Fixed
- Add version in docker-compose file for better compatibility


## [1.3.0] - 2022-07-20

### Added
- Support of flat / non-360° pictures in viewer and server
- List of contributors and special thanks in readme
- Introduced changelog file (the one you're reading 😁)
- Allow direct access to MapLibre GL map object in viewer using `getMap`
- Allow passing all MapLibre GL map settings through viewer using `options.map` object

### Changed
- Pictures blurring now offers several strategies (`BLUR_STRATEGY` setting) and better performance (many thanks to Albin Calais)
- Viewer has a wider zoom range
- Separate stages for building viewer and server in Dockerfile (thanks to Pascal Rhod)

### Fixed
- Test pictures had some corrupted EXIF tags (related to [JOSM issue](https://josm.openstreetmap.de/ticket/22211))


## [1.2.0] - 2022-06-07

### Added
- A demonstration page is available, showing viewer and code examples
- A map is optionally available in viewer to find pictures more easily
- New API route for offering vector tiles (for map) : `/api/map/<z>/<x>/<y>.mvt`
- GeoVisio now has a logo

### Changed
- Improved Dockerfile :
  - Both server and viewer are embed
  - Add list of available environment variables
  - Remove need for a config file
  - A Docker compose file is offered for a ready-to-use GeoVisio with database container
- Server processing for sequences pre-render all derivates versions of pictures to limit I/O with remote filesystems
- Viewer displays a default picture before a real picture is loaded
- Documentation is more complete

### Fixed
- Reading of negative lat/lon coordinates from EXIF tags


## [1.1.0] - 2022-05-09

### Added
- Support of [STAC API scheme](https://github.com/radiantearth/stac-api-spec) for both server and viewer
- New environment variables for database to allow set separately hostname, port, username... : `DB_PORT`, `DB_HOST`, `DB_USERNAME`, `DB_PASSWORD`, `DB_NAME`

### Changed
- All API routes are prefixed with `/api`

### Removed
- `/sequences` API routes, as they are replaced by STAC compliant routes named `/collections`
- Some `/pictures` API routes, as they are replaced by STAC compliant routes named `/collections/<id>/items`


## [1.0.0] - 2022-03-22

### Added
- Server scripts for processing 360° pictures and loading into database
- Support of various filesystems (hard disk, FTP, S3 Bucket...) using PyFilesystem
- API offering sequences, pictures (original, thumbnail and tiled) and various metadata
- Blurring of people, cars, trucks, bus, bicycles on pictures
- Viewer based on Photo Sphere Viewer automatically calling API to search and retrieve pictures
- Dockerfile for easy server setup


[Unreleased]: https://gitlab.com/geovisio/api/-/compare/2.2.0...develop
[2.2.0]: https://gitlab.com/geovisio/api/-/compare/2.1.1...2.2.0
[2.1.1]: https://gitlab.com/geovisio/api/-/compare/2.1.0...2.1.1
[2.1.0]: https://gitlab.com/geovisio/api/-/compare/2.0.2...2.1.0
[2.0.2]: https://gitlab.com/geovisio/api/-/compare/2.0.1...2.0.2
[2.0.1]: https://gitlab.com/geovisio/api/-/compare/2.0.0...2.0.1
[2.0.0]: https://gitlab.com/geovisio/api/-/compare/1.5.0...2.0.0
[1.5.0]: https://gitlab.com/geovisio/api/-/compare/1.4.1...1.5.0
[1.4.1]: https://gitlab.com/geovisio/api/-/compare/1.4.0...1.4.1
[1.4.0]: https://gitlab.com/geovisio/api/-/compare/1.3.1...1.4.0
[1.3.1]: https://gitlab.com/geovisio/api/-/compare/1.3.0...1.3.1
[1.3.0]: https://gitlab.com/geovisio/api/-/compare/1.2.0...1.3.0
[1.2.0]: https://gitlab.com/geovisio/api/-/compare/1.1.0...1.2.0
[1.1.0]: https://gitlab.com/geovisio/api/-/compare/1.0.0...1.1.0
[1.0.0]: https://gitlab.com/geovisio/api/-/commits/1.0.0
