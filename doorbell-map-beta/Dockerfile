# Home Assistant app, beta: the `beta` image of the app, which moves with every build of its beta branch. The Supervisor builds this on the
# device and pulls the base image again for every update; `version` in config.yaml is only the marker of the build.
ARG BUILD_VERSION=latest
FROM ghcr.io/helmerznl/doorbell-map:beta

# The app shows a BETA label for this tag.
ENV DOORBELL_MAP_TAG=beta

COPY run.js /run.js

# The image's own entrypoint (it makes /data writable for the app user, then drops root) is started by run.js.
ENTRYPOINT []
CMD ["node", "/run.js"]
