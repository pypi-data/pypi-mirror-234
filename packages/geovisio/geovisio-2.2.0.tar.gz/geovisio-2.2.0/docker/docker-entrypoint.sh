#!/bin/bash

usage() {
    echo "./docker-entrypoint.sh <COMMAND>: "
    echo -e "\tThis script simplifies running GeoVisio backend in a certain mode"
    echo "Commands: "
    echo -e "\tapi (default): Starts web API for production on port 5000 by default"
    echo -e "\tdev-api: Starts web API for development on port 5000 by default"
    echo -e "\tpicture-worker: Starts an independant background worker to process pictures"
    echo -e "\ttest: Test suite"
    echo -e "\ttest-ci: Test suite (skipping heavy processes)"
    echo -e "\tcleanup: Cleans database and remove Geovisio derivated files (it doesn't delete your original pictures)"
    echo -e "\tdb-upgrade: Upgrade the database schema"
}

# default value is api
command=${1:-"api"}
shift

echo "Executing \"${command}\" command"

case $command in
"api")
    python3 -m waitress --port 5000 --call 'geovisio:create_app'
    ;;
"ssl-api")
    python3 -m waitress --port 5000 --url-scheme=https --call 'geovisio:create_app'
    ;;
"picture-worker")
    python3 -m flask picture-worker
    ;;
"dev-api")
    python3 -m flask --debug run --host=0.0.0.0
    ;;
"cleanup")
    python3 -m flask cleanup
    ;;
"db-upgrade")
    python3 -m flask db upgrade
    ;;
"test")
    python3 -m pytest
    ;;
"test-ci")
    python3 -m pytest -m "not skipci"
    ;;
*)
    usage
    ;;
esac
