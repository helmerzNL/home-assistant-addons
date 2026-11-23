# Home Assistant app, beta: the `dev` image of the app, which moves with every build of its main branch. The Supervisor builds this on the
# device and pulls the base image again for every update; `version` in config.yaml is only the marker of the build.
ARG BUILD_VERSION=latest
FROM ghcr.io/rdiger-36/haspelsync:dev

# /data is the app's own folder: it survives updates and is in Home Assistant's backups. The image keeps these files in /app/printers and /app/logs
# and creates those folders at build time; it does not create the folders DATA_DIR and LOG_DIR point to, so the start creates them first.
ENV DATA_DIR=/data/printers LOG_DIR=/data/logs

# Since 1.4.0 the image runs as the unprivileged `node` user (uid 1000) and checks at every start that DATA_DIR and LOG_DIR are writable, while /data
# of a Home Assistant app belongs to root. So the start runs as root: it creates both folders, hands them to node (with what an earlier version wrote
# there as root), and then runs the app as node with the image's own BusyBox su. su and the shell it starts replace themselves (exec), so the app is
# the main process and gets the stop signal; the environment (DATA_DIR, LOG_DIR, TZ) and the working directory /app stay as they are. Nothing is
# installed, so the build needs no package mirror. An image that still runs as root (1.3.x) runs as node this way too: it writes only to these folders.
USER root
CMD ["sh", "-c", "mkdir -p \"$DATA_DIR\" \"$LOG_DIR\" && chown -R node:node \"$DATA_DIR\" \"$LOG_DIR\" && exec su node -s /bin/sh -c 'exec node entrypoint.js'"]
