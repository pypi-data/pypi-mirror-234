#!/bin/bash

# This scripts checks API conformance against various specifications
# Dependencies: wget, jq (and pip modules)

#################################################
#
# Init
#

trap 'jobs -p | xargs kill' EXIT

ENDPOINT="http://localhost:5000/api"

DIR="$(dirname "${BASH_SOURCE[0]}")"
DIR="$(realpath "${DIR}")"
cd "$DIR/../"
LOG_FILE="./test_api_conformance.log"
DIR_SEQS="/tmp/geovisio_sequences"

pip install stac-api-validator==0.6.1 geovisio_cli==0.2.0 openapi-spec-validator

# Start server with test.env if exists
if [[ -f "./test.env" ]]; then
	echo "Loading test.env config file..."
	export $(grep -v '^#' ./test.env | xargs)
else
	echo "Default API config will be used"
fi

echo "Starting API..."
flask run > $LOG_FILE 2>&1 &

# Wait for a few seconds for startup
sleep 10

# Test if server is available
if wget -q "$ENDPOINT" > /dev/null 2>&1 ; then
	echo "Server started"
else
	echo "Server not started"
	wget -q -S -O - "$ENDPOINT"
	exit 1
fi

# Populate test server with data if $NO_IMPORT has not been set to '1'
if [[ "$NO_IMPORT" != "1" ]]; then
	echo "Reloading mock data in DB..."
	flask cleanup --full

	rm -rf "$DIR_SEQS"
	mkdir -p $DIR_SEQS

	for seq in {1..5}; do
		mkdir -p $DIR_SEQS/"sequence_$seq"

		for img in {1..5}; do
			cp $DIR/data/$img.jpg $DIR_SEQS/"sequence_$seq"/
		done
	done

	for seq in $DIR_SEQS/sequence_*; do
		geovisio upload --api-url http://localhost:5000 --wait $seq
	done
else
	echo "Using existing data in server"
fi

# Get a single collection ID
COLLECTION_ID=$(wget -q -S -O - "$ENDPOINT/search?limit=1" | jq '.features[0].collection')
COLLECTION_ID=${COLLECTION_ID//\"/}

# Geometry for intersection
GEOM_INTERSECT='{"type": "Polygon", "coordinates": [[[-4.04,51.30],[-4.04,42.05],[9.19,42.05],[9.19,51.30],[-4.04,51.30]]]}'


#################################################
#
# API conformance testing
#

# STAC API
# Other conformances to check: item-search (bugged for now), features (tiled-assets extension issue)
# Conformances we don't use: children
stac-api-validator \
	--root-url "$ENDPOINT" \
	--conformance core \
	--conformance collections \
	--conformance browseable \
	--conformance filter \
	--collection "$COLLECTION_ID" \
	--geometry "$GEOM_INTERSECT"

RES_STAC="$?"
rm ./api ./api.*
rm -rf "$DIR_SEQS"


# OpenAPI specifications
wget -q "$ENDPOINT/docs/specs.json" -O - \
	| openapi-spec-validator -
RES_OPENAPI="$?"


if [[ "$RES_STAC" == "0" ]] && [[ "$RES_OPENAPI" == "0" ]]; then
	echo "All tests done without errors"
else
	exit 2
fi
