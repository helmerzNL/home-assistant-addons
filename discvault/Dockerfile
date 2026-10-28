# Home Assistant app: the published app image plus the PostgreSQL it needs, started by run.py.
# The Supervisor builds this on the device and passes BUILD_VERSION (= `version` in config.yaml); the tag exists for every release.
ARG BUILD_VERSION=latest
FROM ghcr.io/helmerznl/discvault:${BUILD_VERSION}

ARG BUILD_VERSION=latest
ENV DISCVAULT_HA_BUILD=${BUILD_VERSION}

# The Docker installation runs postgres:17; the data folder of one major version cannot be opened by another, so 17 is asked for by name:
# a base image whose Debian has no PostgreSQL 17 fails this build instead of starting with a different one.
USER root
# The package would otherwise make a database cluster of its own that nothing uses.
RUN mkdir -p /etc/postgresql-common && echo 'create_main_cluster = false' > /etc/postgresql-common/createcluster.conf \
    && apt-get update \
    && apt-get install -y --no-install-recommends postgresql-17 \
    && rm -rf /var/lib/apt/lists/* \
    && test -x /usr/lib/postgresql/17/bin/postgres

COPY run.py /run.py

# supervisord of the image (API, worker, MCP) is started by run.py, next to PostgreSQL.
CMD ["python", "/run.py"]
