# Home Assistant app: the published Spoolman image, started by run.py so the options of the app become its environment and its data lives in /data.
# The Supervisor builds this on the device and passes BUILD_VERSION (= `version` in config.yaml); the image tag is that version.
ARG BUILD_VERSION=latest
FROM ghcr.io/donkie/spoolman:${BUILD_VERSION}

COPY run.py /run.py

# run.py hands /data/spoolman to the image's user and then starts the image's own entrypoint (which drops root and runs uvicorn).
ENTRYPOINT []
CMD ["python3", "/run.py"]
