# Install Geovisio on a classic server

Geovisio can be deployed manually on a classic server, offering best performance and high-level of customization. If you prefer a more _plug & play_ deployment, you can look at the [Docker install documentation](./14_Running_Docker.md).

## Dependencies

GeoVisio best runs with a recent Linux server and needs these components:

- Python __3.9+__
- An up and running database, as seen in [database setup documentation](./07_Database_setup.md)

## Install

You have to run following commands for installing classic dependencies:

```bash
# Retrieve API source code
git clone https://gitlab.com/geovisio/api.git geovisio-api
cd geovisio-api/

# Enable Python environment
python3 -m venv env
source ./env/bin/activate

# Install Python dependencies
pip install -e .
pip install -e .[dev] # Only for dev or testing purposes
```

## Next step

You can read more about [server settings](./11_Server_settings.md).
