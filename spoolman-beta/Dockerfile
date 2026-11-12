# Home Assistant app, beta: the `edge` image of the app, which moves with every build of its master branch. The Supervisor builds this on the
# device and pulls the base image again for every update; `version` in config.yaml is only the marker of the build.
ARG BUILD_VERSION=latest
FROM ghcr.io/donkie/spoolman:edge

COPY run.py /run.py

# run.py hands /data/spoolman to the image's user and then starts the image's own entrypoint (which drops root and runs uvicorn).
ENTRYPOINT []
CMD ["python3", "/run.py"]
