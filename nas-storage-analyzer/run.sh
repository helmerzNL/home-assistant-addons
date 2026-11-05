#!/bin/sh
# Home Assistant app for NAS Storage Analyzer: turns the options of the app (/data/options.json) into the environment of the
# all-in-one image and starts it (nasa-aio: PostgreSQL in /data/postgres, the web interface and the worker; see
# https://github.com/helmerzNL/NAS-Storage-Analyzer/blob/beta/docs/adr/0013-all-in-one-image.md).
#
# The encryption key of the app (it seals the stored SMB passwords) is made on the first start and kept in /data/encryption.key,
# unless the option encryption_key is set. /data is part of the backups of this app, which Home Assistant encrypts.
# The variables HA_* only exist for the tests (tests/test_nas_storage_analyzer_run.py).
set -eu

DATA="${HA_DATA_DIR:-/data}"
OPTIONS="${HA_OPTIONS_FILE:-$DATA/options.json}"
KEYFILE="$DATA/encryption.key"
AIO="${HA_AIO_COMMAND:-/usr/local/bin/nasa-aio}"

log() { printf '[nas-storage-analyzer] %s\n' "$*" >&2; }
fail() { printf '[nas-storage-analyzer] ERROR: %s\n' "$*" >&2; exit 1; }

# The value of one option as text, or nothing when it is missing or empty.
opt() {
  [ -f "$OPTIONS" ] || return 0
  jq -r --arg k "$1" 'if has($k) and .[$k] != null then .[$k] | tostring else empty end' "$OPTIONS"
}

# A key is base64 of exactly 32 bytes (what `nasa genkey` makes).
valid_key() {
  [ "$(printf %s "$1" | base64 -d 2>/dev/null | wc -c | tr -d ' ')" = 32 ]
}

key="$(opt encryption_key)"
if [ -n "$key" ]; then
  valid_key "$key" || fail "encryption_key must be base64 of 32 bytes, as made by: openssl rand -base64 32"
  log "using the encryption key from the option encryption_key"
else
  if [ ! -s "$KEYFILE" ]; then
    (umask 077; head -c 32 /dev/urandom | base64 | tr -d '\n' > "$KEYFILE.tmp")
    mv "$KEYFILE.tmp" "$KEYFILE"
    log "made a new encryption key in /data/encryption.key; it is part of the backups of this app"
  fi
  key="$(tr -d '[:space:]' < "$KEYFILE")"
  valid_key "$key" || fail "/data/encryption.key does not hold a valid key; restore it from a backup, or set the option encryption_key"
fi
NASSA_ENCRYPTION_KEY="$key"
export NASSA_ENCRYPTION_KEY

set_from() { # set_from <option> <variable>
  value="$(opt "$1")"
  if [ -n "$value" ]; then
    export "$2=$value"
    set_options="${set_options:+$set_options, }$1"
  fi
}
set_options=
set_from setup_token NASSA_SETUP_TOKEN
set_from public_url NASSA_PUBLIC_URL
set_from rp_id NASSA_RP_ID
set_from rp_origins NASSA_RP_ORIGINS
set_from trusted_proxies NASSA_TRUSTED_PROXIES
set_from worker_parallel NASSA_WORKER_PARALLEL
set_from update_check NASSA_UPDATE_CHECK

if [ -n "${NASSA_RP_ID:-}" ] && [ -z "${NASSA_RP_ORIGINS:-}" ]; then
  fail "rp_id is set, so rp_origins is needed too: the full https address(es) you open the app on, for example https://nassa.example.com"
fi

# The folders this app maps (config.yaml: share and media) are below /mnt/shares, the folder the app may scan. A Home Assistant box is
# smaller than the servers the defaults of the app are sized for, so PostgreSQL starts smaller unless told otherwise.
NASSA_SHARES_ROOT=/mnt/shares
PG_SHARED_BUFFERS="${PG_SHARED_BUFFERS:-256MB}"
PG_EFFECTIVE_CACHE_SIZE="${PG_EFFECTIVE_CACHE_SIZE:-1GB}"
export NASSA_SHARES_ROOT PG_SHARED_BUFFERS PG_EFFECTIVE_CACHE_SIZE

log "options set: ${set_options:-none} (secrets are not printed)"
exec "$AIO"
