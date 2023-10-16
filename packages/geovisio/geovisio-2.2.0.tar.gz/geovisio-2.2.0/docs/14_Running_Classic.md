# Available commands on classic deployment

Various operations can be run on GeoVisio API : start HTTP API, migrate or clean-up database... This documentation cover available commands on a classic instance, if you're using Docker please [see this doc instead](./14_Running_Docker.md).

[[_TOC_]]

## Available commands

Server commands can be run using `flask` entrypoint:

```bash
flask <command>
```

Available commands are:

```
cleanup                Cleans up GeoVisio files and database.
db                     Commands to handle database operations
set-sequences-heading  Changes pictures heading metadata.
```

### Start API

This command starts the HTTP API to serve pictures & sequences to users.

```bash
# Development API
flask --debug run
```

For production context, you may want a more robust WSGI server than the Flask's embedded one. [Flask team recommend](https://flask.palletsprojects.com/en/2.3.x/deploying/waitress/) [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/).

```bash
# Production HTTPS API
pip install waitress
python3 -m waitress --port 5000 --url-scheme=https --call 'geovisio:create_app'
```

You can pass more parameters to `waitress`, like `--threads` to define the number of worker threads run, check the documentation for fine tuning if needed.

### Database migration

As GeoVisio is actively developed, when updating from a previous version, some database migration could be necessary. If so, when starting GeoVisio, an error message will show up and warn about necessary migration. The following command has to be ran:

```bash
flask db upgrade
```

There might be no reason to do so, but if necessary, a migration rollback can also be done:

```bash
flask db rollback
```

A full database rollback (ie. removing all structures and data created by Geovisio) can also be done with this command:

```bash
flask db rollback --all
```

### Force pictures heading in sequence

Since version 1.4.0, you can import pictures without heading metadata. By default, heading is computed based on sequence movement path (looking in front), but you can edit manually after import using this command:

```bash
flask set-sequences-heading \
	--value <DEGREES_ROTATION_FROM_FORWARD> \
	--overwrite \
	<SEQUENCE_ID_1> <SEQUENCE_ID_2> ...
```

### Clean-up

Eventually, if you want to clear database and delete derivate versions of pictures (it __doesn't__ delete original pictures), you can use the `cleanup` command:

```bash
flask cleanup
```

You can cleanup only certain sequences:

```bash
flask cleanup <SEQUENCE_ID_1> <SEQUENCE_ID_2> ...
```

You can also run some partial cleaning with the same cleanup command and one of the following options:

```bash
flask cleanup \
    --database \ # Removes entries from database
    --cache \ # Removes picture derivates (tiles, SD and thumbnail)
    --permanent-pictures # Removes permanent (original) pictures
```

### Sequences reorder

You can sort all sequences by pictures capture time with the following command:

```bash
flask sequences reorder
```

If you want to reorder some specific sequences, you need their ID (the UUID):

```bash
flask sequences reorder <SEQUENCE_ID_1> <SEQUENCE_ID_2>
```

## Next step

Your server is up and running, you may want to:
- [Work with the HTTP API](./16_Using_API.md)
- [Organize your pictures and sequences](./15_Pictures_requirements.md)
