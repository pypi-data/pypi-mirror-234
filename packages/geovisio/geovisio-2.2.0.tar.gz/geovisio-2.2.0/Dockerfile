FROM python:3.9-slim

# Install system dependencies
RUN apt update \
    && apt install -y git \
    && pip install waitress \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /opt/360app /data/360app

WORKDIR /opt/360app

# Install Python dependencies
COPY ./README.md ./LICENSE ./pyproject.toml ./
COPY ./geovisio/__init__.py ./geovisio/
RUN pip install -e .[dev]


# Add source files
COPY ./images ./images/
COPY ./docker/docker-entrypoint.sh ./
RUN chmod +x ./docker-entrypoint.sh
COPY ./geovisio ./geovisio
COPY ./migrations ./migrations

# Add tests files (needed by the CI)
COPY ./tests ./tests

# Environment variables
ENV FLASK_APP=geovisio
ENV DB_URL="postgres://user:pass@host/dbname"
ENV FS_URL="osfs:///data/360app"
ENV PICTURE_PROCESS_DERIVATES_STRATEGY="ON_DEMAND"

# Expose service
EXPOSE 5000
ENTRYPOINT ["./docker-entrypoint.sh"]
