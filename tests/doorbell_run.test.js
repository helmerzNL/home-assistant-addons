'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { buildEnv, keptSecrets } = require('../doorbell-map/run.js');

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

test('a missing or broken address stops with a message', () => {
  assert.throws(() => buildEnv({}, kept), /Set origin/);
  assert.throws(() => buildEnv({ origin: 'map.example.com' }, kept), /not an address/);
  assert.throws(() => buildEnv({ origin: 'https://m.example.com', rp_id: 'm.example.com:443' }, kept), /domain name only/);
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
