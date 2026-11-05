# Home Assistant app: the all-in-one image of NAS Storage Analyzer (PostgreSQL, web interface and worker in one container), started
# by run.sh. The Supervisor builds this on the device and passes BUILD_VERSION (= `version` in config.yaml); the tag exists for every release.
ARG BUILD_VERSION=latest
FROM ghcr.io/helmerznl/nas-storage-analyzer-aio:${BUILD_VERSION}

# run.sh reads the options of the app with jq.
RUN apk add --no-cache jq

COPY run.sh /run.sh

ENTRYPOINT ["/sbin/tini", "--", "/bin/sh", "/run.sh"]
CMD []
