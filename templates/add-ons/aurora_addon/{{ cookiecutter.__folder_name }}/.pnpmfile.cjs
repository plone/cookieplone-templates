// The core overlay: develop against an unreleased Plone Aurora.
//
// Without a `core/` folder, this file does nothing, and the app installs the
// released `@plone/*` packages of the lock file.
//
// With a checkout of the Plone Aurora repository in `core/`, which `make core`
// creates, `pnpm install` links every `@plone/*` package of the app and the
// add-ons, and of their dependencies, to the one in `core/packages`, through
// the `core/packages/*` entry of `pnpm-workspace.yaml`. The packages of the
// checkout get the versions of its catalog, unless this repository's catalog
// sets them. The lock file stays as it is: it keeps the released packages for
// everybody else, and a frozen install, as in CI or in the Docker image,
// refuses the overlay. Run `make remove-core` to use the released packages
// again.
const fs = require('fs');
const path = require('path');

const coreDir = path.join(__dirname, 'core');
const corePackagesDir = path.join(coreDir, 'packages');
const hasCore = fs.existsSync(path.join(corePackagesDir, 'aurora', 'package.json'));

function readJSON(file) {
  return JSON.parse(fs.readFileSync(file, 'utf-8'));
}

// The public packages of the checkout. The Volto packages stay out, as in the
// Plone Aurora repository.
function corePackageNames() {
  return fs
    .readdirSync(corePackagesDir)
    .filter((dir) => !dir.startsWith('volto'))
    .map((dir) => path.join(corePackagesDir, dir, 'package.json'))
    .filter((file) => fs.existsSync(file))
    .map(readJSON)
    .filter((pkg) => pkg.name && !pkg.private)
    .map((pkg) => pkg.name);
}

module.exports = {
  hooks: {
    updateConfig(config) {
      if (!hasCore) return config;
      config.lockfile = false;
      const catalogFile = path.join(coreDir, 'catalog.json');
      if (fs.existsSync(catalogFile)) {
        config.catalogs ??= {};
        config.catalogs.default = {
          ...readJSON(catalogFile),
          ...config.catalogs.default,
        };
      }
      config.overrides ??= {};
      for (const name of corePackageNames()) {
        config.overrides[name] = 'workspace:*';
      }
      return config;
    },
  },
};
