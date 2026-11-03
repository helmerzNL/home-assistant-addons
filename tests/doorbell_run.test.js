'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { buildEnv, keptSecrets, appFollowsAddress } = require('../doorbell-map/run.js');

const kept = { session_secret: 'x'.repeat(64), setup_token: 'abcdef012345' };

test('the address becomes ORIGIN without a trailing slash', () => {
  const env = buildEnv({ origin: 'https://map.example.com/' }, kept);
  assert.equal(env.ORIGIN, 'https://map.example.com');
  assert.equal(env.PORT, '9888');
  assert.equal(env.SETUP_TOKEN, 'abcdef012345');
  assert.equal(env.RP_ID, undefined);
});

test('optional settings are passed on when set', () => {
  const env = buildEnv({ origin: 'https://map.example.com', rp_id: 'Map.Example.com', site_title: ' Onze wijk ', setup_token: 'mine', session_hours: 24 }, kept);
  assert.equal(env.RP_ID, 'map.example.com');
  assert.equal(env.SITE_TITLE, 'Onze wijk');
  assert.equal(env.SETUP_TOKEN, 'mine');
  assert.equal(env.SESSION_HOURS, '24');
});

test('without origin a newer app follows the address it is opened on', () => {
  const env = buildEnv({ rp_id: 'map.example.com' }, kept, true);
  assert.equal(env.ORIGIN, undefined);
  assert.equal(env.RP_ID, 'map.example.com');
  assert.equal(env.PORT, '9888');
  assert.equal(buildEnv({ origin: '  ' }, kept, true).ORIGIN, undefined);
});

test('an older app still needs origin', () => {
  assert.throws(() => buildEnv({}, kept, false), /still needs origin/);
  assert.equal(buildEnv({ origin: 'http://192.168.1.10:9888' }, kept, false).ORIGIN, 'http://192.168.1.10:9888');
});

test('a broken address stops with a message', () => {
  for (const follows of [true, false]) {
    assert.throws(() => buildEnv({ origin: 'map.example.com' }, kept, follows), /not an address/);
    assert.throws(() => buildEnv({ origin: 'ftp://map.example.com' }, kept, follows), /has to start with https/);
    assert.throws(() => buildEnv({ origin: 'https://m.example.com', rp_id: 'm.example.com:443' }, kept, follows), /domain name only/);
  }
});

test('the app follows the address when its image ships server/origin.js', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'doorbell-app-'));
  assert.equal(appFollowsAddress(dir), false);
  fs.mkdirSync(path.join(dir, 'server'));
  fs.writeFileSync(path.join(dir, 'server', 'origin.js'), '');
  assert.equal(appFollowsAddress(dir), true);
});

test('secrets are made once and then kept', () => {
  const first = keptSecrets({}, {});
  assert.equal(first.changed, true);
  assert.equal(first.secrets.session_secret.length, 64);
  const second = keptSecrets(first.secrets, {});
  assert.equal(second.changed, false);
  assert.deepEqual(second.secrets, first.secrets);
});

test('the made-up setup code is not printed when the owner sets one', () => {
  assert.equal(keptSecrets(kept, {}).printSetupToken, true);
  assert.equal(keptSecrets(kept, { setup_token: 'mine' }).printSetupToken, false);
});
