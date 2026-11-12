# Home Assistant app, beta: the `dev` image of the app, which moves with every build of its main branch. The Supervisor builds this on the
# device and pulls the base image again for every update; `version` in config.yaml is only the marker of the build.
ARG BUILD_VERSION=latest
FROM ghcr.io/rdiger-36/haspelsync:dev

# /data is the app's own folder: it survives updates and is in Home Assistant's backups. The image keeps these files in /app/printers and /app/logs
# and creates those folders at build time; it does not create the folders DATA_DIR and LOG_DIR point to, so the start creates them first.
ENV DATA_DIR=/data/printers LOG_DIR=/data/logs
CMD ["sh", "-c", "mkdir -p \"$DATA_DIR\" \"$LOG_DIR\" && exec node entrypoint.js"]
