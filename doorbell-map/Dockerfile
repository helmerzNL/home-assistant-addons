# Home Assistant app: the published app image, started by run.js so the options of the app become its environment.
# The Supervisor builds this on the device and passes BUILD_VERSION (= `version` in config.yaml); the image tag is that version with a v.
ARG BUILD_VERSION=latest
FROM ghcr.io/helmerznl/doorbell-map:v${BUILD_VERSION}

COPY run.js /run.js

# The image's own entrypoint (it makes /data writable for the app user, then drops root) is started by run.js.
ENTRYPOINT []
CMD ["node", "/run.js"]
