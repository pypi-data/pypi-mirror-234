# Install and run GeoVisio using Docker

The [Docker](https://docs.docker.com/get-docker/) deployment is a really convenient way to have a Geovisio instance running in an easy and fast way. If you prefer to not use Docker, you can see how to [install](./10_Install_Classic.md) then [run](./14_Running_Classic.md) a classic instance.

Available Docker configuration files are :

* [Dockerfile](../Dockerfile) : contains only API. An __external__ PostgreSQL database must be provided.
* [docker-compose.yml](../docker-compose.yml) : offers API and database using __Docker Hub__ `geovisio/api:develop` image by default, but can also be built using local files.
* [docker-compose-auth.yml](../docker/docker-compose-auth.yml) : offers API, database and Keycloak (for authentication).
* [docker-compose-full.yml](../docker/docker-compose-full.yml) : offers __everything__ (Website, API, database, Keycloak and blurring API).

__Contents__

[[_TOC_]]

## Run with Dockerfile

In this setup, only API and a demo website are offered. A database must be available somewhere, see [database setup documentation](./07_Database_setup.md) to set it up, or use one of the Docker compose setup offered below.

You can use the provided __Docker Hub__ `geovisio/api:develop` image directly:

```bash
docker run \
	-e DB_URL=<database connection string> \
	-p 5000:5000 \
	--name geovisio \
	-v <path where to persist pictures>:/data/360app \
	geovisio/api:develop \
	<command>
```

This will run a container bound on port 5000 and store uploaded images in the provided folder.

You can also build the image from the local source with:

```bash
docker build -t geovisio/api:latest .
```


## Run with Docker Compose

Many variants of the Docker Compose are available. The straightforward solution is to use the [docker-compose.yml](../docker-compose.yml) file, which embeds both database and GeoVisio API, without the hassle of authentication and blurring (you can use [docker-compose-full.yml](../docker/docker-compose-full.yml) for that).

You can run using __Docker Hub__ images for a faster set-up with this command:

```bash
docker-compose -f docker-compose.yml up
```

If you want to work with local files instead, add a `--build` option:

```bash
docker-compose -f docker-compose.yml up --build
```

Once all services are running, you can also run other commands for launching various chore tasks:

```bash
docker-compose -f docker-compose.yml run --rm backend <COMMAND TO RUN>
```

Note that if you use complete [docker-compose-full.yml](../docker/docker-compose-full.yml) file, the provided Keycloak configuration __should not be used in production__, it's only for testing.


## Available commands

```
api                 Starts web API for production
ssl-api             Starts web API for production with SSL enabled
dev-api             Starts web API for development
db-upgrade          Database migration
cleanup             Cleans database and remove Geovisio derivated files
```

### Start API

Commands `api`, `ssl-api` and `dev-api` allows you to start Geovisio API, either on HTTP, HTTPS or development mode.

### Database migration

As GeoVisio is actively developed, when updating from a previous version, some database migration could be necessary. If so, when starting GeoVisio, an error message will show up and warn about necessary migration. The `db-upgrade` command has to be ran then.

### Clean-up

Eventually, if you want to clear database and delete derivate versions of pictures (it __doesn't__ delete original pictures), you can use the `cleanup` command. You can also run some partial cleaning with the same cleanup command and one of the following options:

```bash
<DOCKER COMMAND> cleanup \
    --database \ # Removes entries from database
    --cache \ # Removes picture derivates (tiles, SD and thumbnail)
    --permanent-pictures # Removes permanent (original) pictures
```

### Other commands

Additional commands can be available (as documented in [classic instance running doc](./14_Running_Classic.md)). These commands can also be launched on a Docker instance using the following syntax:

```bash
# Docker container
docker exec \
	<CONTAINER NAME> \
	flask <GEOVISIO COMMAND>

# Docker compose
docker-compose -f <COMPOSE YML FILE> \
	exec \
	backend \
	flask <GEOVISIO COMMAND>
```


## Next step

Your server is up and running, you may want to:
- [Work with the HTTP API](./16_Using_API.md)
- [Fine tune your server settings](./11_Server_settings.md).
- [Organize your pictures and sequences](./15_Pictures_requirements.md)
