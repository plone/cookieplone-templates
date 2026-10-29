// Standalone Playwright config for the meta-CI integration smoke tests.
// The generated add-on ships its own playwright.config.ts (testDir:
// acceptance/tests), which would otherwise be auto-discovered and hide the
// smoke test we copy into the frontend root. Pointing at this config keeps the
// smoke tests independent of whatever config the generated project ships.
module.exports = {
  testDir: '.',
  testMatch: ['aurora-*.test.js', 'volto-*.test.js'],
};
