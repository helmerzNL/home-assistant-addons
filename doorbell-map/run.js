#!/usr/bin/env node
'use strict';
// Starts Doorbell Map inside a Home Assistant app. The options of the app (/data/options.json) become the variables of the .env file of the
// Docker installation; the secrets that .env would hold are made once and kept in /data/secrets.json, so sessions survive a restart.
// /data is the DATA_DIR of the app. The image's own entrypoint makes it writable for the app user and drops root.
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { spawn } = require('node:child_process');

const DATA = process.env.DATA_DIR || '/data';
const OPTIONS = process.env.OPTIONS_FILE || path.join(DATA, 'options.json');
const SECRETS = path.join(DATA, 'secrets.json');
const ENTRYPOINT = process.env.APP_ENTRYPOINT || 'docker-entrypoint.sh';

function log(message) { console.log(`[doorbell-map] ${message}`); }

function readJson(file, fallback) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch (e) { if (e.code === 'ENOENT') return fallback; throw e; }
}

// The kept secrets, with a new one for every secret that is missing. `changed` says whether the file has to be written; the made-up setup code
// is printed at every start (the Log tab is for the owner only), so it is not lost when the first start was missed.
function keptSecrets(kept, options) {
  const next = { ...kept };
  const made = [];
  if (!next.session_secret) { next.session_secret = crypto.randomBytes(32).toString('hex'); made.push('session_secret'); }
  if (!next.setup_token) { next.setup_token = crypto.randomBytes(12).toString('hex'); made.push('setup_token'); }
  return { secrets: next, changed: made.length > 0, printSetupToken: !String(options.setup_token || '').trim() };
}

// The environment of the app. Throws an Error with a readable message when the address is not set or not usable.
function buildEnv(options, kept) {
  const origin = String(options.origin || '').trim().replace(/\/+$/, '');
  if (!origin) {
    throw new Error('Set origin (the address the map is opened on, for example https://map.example.com) on the Configuration tab of this app, then start it again. '
      + 'Passkeys for the admin only work over https (see the Documentation tab).');
  }
  let url;
  try { url = new URL(origin); } catch { throw new Error(`origin "${origin}" is not an address; use the form https://map.example.com`); }
  if (url.protocol !== 'https:' && url.protocol !== 'http:') throw new Error('origin has to start with https:// (or http:// for a test on localhost).');
  const env = {
    ORIGIN: origin,
    SESSION_SECRET: kept.session_secret,
    SETUP_TOKEN: String(options.setup_token || '').trim() || kept.setup_token,
    DATA_DIR: DATA,
    PORT: '9888',
  };
  const rpId = String(options.rp_id || '').trim().toLowerCase();
  if (rpId) {
    if (/[:/]/.test(rpId)) throw new Error('rp_id must be a domain name only, without https://, a path or a port (for example map.example.com).');
    env.RP_ID = rpId;
  }
  if (String(options.site_title || '').trim()) env.SITE_TITLE = String(options.site_title).trim();
  if (options.session_hours) env.SESSION_HOURS = String(Number(options.session_hours));
  return env;
}

function main() {
  const options = readJson(OPTIONS, {});
  const { secrets, changed, printSetupToken } = keptSecrets(readJson(SECRETS, {}), options);
  let env;
  try { env = buildEnv(options, secrets); } catch (e) { console.error(`[doorbell-map] ERROR: ${e.message}`); return 1; }
  if (changed) {
    fs.mkdirSync(DATA, { recursive: true });
    const tmp = `${SECRETS}.tmp`;
    fs.writeFileSync(tmp, JSON.stringify(secrets, null, 2), { mode: 0o600 });
    fs.renameSync(tmp, SECRETS);
  }
  if (printSetupToken) log(`Setup code for the first passkey of the admin: ${secrets.setup_token}  (set your own under Configuration if you prefer)`);
  const child = spawn(ENTRYPOINT, ['node', 'server/index.js'], { env: { ...process.env, ...env }, stdio: 'inherit' });
  for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => child.kill(signal));
  child.on('exit', (code, signal) => process.exit(code ?? (signal ? 1 : 0)));
  child.on('error', (e) => { console.error(`[doorbell-map] ERROR: ${e.message}`); process.exit(1); });
  return null;
}

if (require.main === module) {
  const code = main();
  if (code !== null) process.exit(code);
}

module.exports = { buildEnv, keptSecrets };
