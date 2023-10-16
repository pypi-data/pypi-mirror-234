# Database setup

Geovisio relies on a [PostgreSQL](https://www.postgresql.org/) 10+ database with [PostGIS](https://postgis.net/) 3+ extension to run.

This documentation is important to read __if you're installing manually Geovisio__. If you want to deploy using __Docker__, you can go directly to [Docker install documentation](./14_Running_Docker.md).

First step is to install both [PostgreSQL](https://www.postgresql.org/) and [PostGIS](https://postgis.net/). Please refer to these software documentation to know more about their install.

Once your PostgreSQL server is ready and running, we recommend you to do the following:

- Add a system/OS user named `geovisio`, for example under Linux:

```bash
sudo useradd geovisio
```

- Create a PostgreSQL role `geovisio` with this command:

```bash
sudo su - postgres -c "psql -c \"CREATE ROLE geovisio LOGIN PASSWORD 'mypassword'\""
```

- Create a new database (with __UTF-8 encoding__) using this command:

```bash
sudo su - postgres -c "psql -c \"CREATE DATABASE geovisio ENCODING 'UTF-8' TEMPLATE template0 OWNER geovisio\""
```

- Enable PostGIS extension in your database:

```bash
sudo su - postgres -c "psql -d geovisio -c \"CREATE EXTENSION postgis\""
```


## Next step

Once your database is ready, you can install Geovisio, either with [Docker](./14_Running_Docker.md) or directly [on server](./10_Install_Classic.md).


## Troubleshooting

Got some issues on this part ? Here are a few hints that may help.

* PostgreSQL server is not listening ?
  * Check the [postgresql.conf](https://www.postgresql.org/docs/current/config-setting.html#CONFIG-SETTING-CONFIGURATION-FILE) file and verify that `listen_adresses` is set to `*`
* PostgreSQL says `Peer authentication failed` ?
  * Check your [pg_hba.conf](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html) file and verify that a rule exist to allow your geovisio or any other OS user to login into your GeoVisio database
  * This is particularly useful if you're running only GeoVisio API in Docker, with a PostgreSQL database server on your host, where database IP address might look like `172.17.0.*`. You may have to add an entry like this to allow login:

```
host	geovisio	geovisio	172.17.0.0/24	trust
```
