# Home Assistant app, beta: the `beta` image of the app, which moves with every build of its beta branch. The Supervisor builds this on the
# device and pulls the base image again for every update; `version` in config.yaml is only the marker of the build.
ARG BUILD_VERSION=latest
FROM ghcr.io/helmerznl/discvault:beta

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
