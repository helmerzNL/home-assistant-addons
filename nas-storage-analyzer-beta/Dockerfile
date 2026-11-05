# Home Assistant app, beta: the `beta` image of the app, which moves with every build of its beta branch. The Supervisor builds this on the
# device and pulls the base image again for every update; `version` in config.yaml is only the marker of the build.
ARG BUILD_VERSION=latest
FROM ghcr.io/helmerznl/nas-storage-analyzer-aio:beta

# run.sh reads the options of the app with jq.
RUN apk add --no-cache jq

COPY run.sh /run.sh

ENTRYPOINT ["/sbin/tini", "--", "/bin/sh", "/run.sh"]
CMD []
