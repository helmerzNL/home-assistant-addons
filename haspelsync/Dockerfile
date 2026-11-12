# Home Assistant app: the published HaspelSync image, with its configuration (printers, settings, mappings, API keys) and its logs in /data.
# The Supervisor builds this on the device and passes BUILD_VERSION (= `version` in config.yaml); the image tag is that version.
ARG BUILD_VERSION=latest
FROM ghcr.io/rdiger-36/haspelsync:${BUILD_VERSION}

# /data is the app's own folder: it survives updates and is in Home Assistant's backups. The image keeps these files in /app/printers and /app/logs
# and creates those folders at build time; it does not create the folders DATA_DIR and LOG_DIR point to, so the start creates them first.
ENV DATA_DIR=/data/printers LOG_DIR=/data/logs
CMD ["sh", "-c", "mkdir -p \"$DATA_DIR\" \"$LOG_DIR\" && exec node entrypoint.js"]
