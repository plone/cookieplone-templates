# {{ cookiecutter.title }} ({{ cookiecutter.__npm_package_name }})

{{ cookiecutter.description }}

[![npm](https://img.shields.io/npm/v/{{ cookiecutter.__npm_package_name }})](https://www.npmjs.com/package/{{ cookiecutter.__npm_package_name }})
[![](https://img.shields.io/badge/-Storybook-ff4785?logo=Storybook&logoColor=white&style=flat-square)](https://{{ cookiecutter.github_organization }}.github.io/{{ cookiecutter.frontend_addon_name }}/)
[![Code analysis checks](https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.frontend_addon_name }}/actions/workflows/code.yml/badge.svg)](https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.frontend_addon_name }}/actions/workflows/code.yml)
[![Unit tests](https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.frontend_addon_name }}/actions/workflows/unit.yml/badge.svg)](https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.frontend_addon_name }}/actions/workflows/unit.yml)

## Features

<!-- List your awesome features here -->

## Installation

Add `{{ cookiecutter.__npm_package_name }}` to the dependencies of your Plone Aurora app:

```shell
pnpm add {{ cookiecutter.__npm_package_name }}
```

Then add it to the add-ons in the app's `registry.config.ts`:

```ts
import { addons } from '@plone/aurora/registry.config';

addons.push('{{ cookiecutter.__npm_package_name }}');

export { addons };
```

## Test installation

Visit http://localhost:3000/ in a browser, login, and check the awesome new features.


## Development

This repository is a Plone Aurora app that installs the add-on from `packages/{{ cookiecutter.frontend_addon_name }}`.
It's a standard React Router app: `app/`, `react-router.config.ts` and `vite.config.ts` come with `@plone/aurora`, from npm.
The add-on and the app share their dependency versions through the pnpm catalog in `pnpm-workspace.yaml`.


### Pre-requisites

-   [Node.js](https://6.docs.plone.org/install/create-project.html#node-js)
-   [Make](https://6.docs.plone.org/install/create-project.html#make)
-   [Docker](https://6.docs.plone.org/install/create-project.html#docker)

Install and enable the latest Corepack. Corepack will resolve the pnpm version
pinned by this repository's `packageManager` field.

```shell
npm install --global corepack@latest
corepack enable
```


### Make convenience commands

Run `make help` to list the available commands.

```text
help                             Show this help
install                          Installs the add-on in a development environment
start                            Starts Plone Aurora in development mode, reloading the add-on on changes
build                            Build a production bundle for distribution of the project with the add-on
typecheck                        Check the types of the app and the add-on
i18n                             Sync i18n
ci-i18n                          Check if i18n is not synced
format                           Format codebase
lint                             Lint, or catch and remove problems, in code base
release                          Release the add-on on npmjs.org
release-dry-run                  Dry-run the release of the add-on on npmjs.org
test                             Run unit tests
ci-test                          Run unit tests in CI
backend-docker-start             Starts a Docker-based backend for development
storybook-start                  Start Storybook server on port 6006
storybook-build                  Build Storybook
acceptance-frontend-dev-start    Start acceptance frontend in development mode
acceptance-frontend-prod-start   Start acceptance frontend in production mode
acceptance-backend-start         Start backend acceptance server
ci-acceptance-backend-start      Start backend acceptance server in headless mode for CI
install-acceptance               Install the Playwright browsers used by the acceptance tests
acceptance-test                  Start the acceptance tests in interactive (UI) mode
ci-acceptance-test               Run the acceptance tests in headless mode for CI
```

### Development environment set up

Install package requirements.

```shell
make install
```

### Start developing

Start the backend.

```shell
make backend-docker-start
```

In a separate terminal session, start the frontend.

```shell
make start
```

### Lint code

Run ESlint, Prettier, and Stylelint in analyze mode.

```shell
make lint
```

### Format code

Run ESlint, Prettier, and Stylelint in fix mode.

```shell
make format
```

### i18n

Extract the i18n messages to locales.

```shell
make i18n
```

### Unit tests

Run unit tests.

```shell
make test
```

### Run acceptance tests

Run each of these steps in separate terminal sessions.

In the first session, start the frontend in development mode.

```shell
make acceptance-frontend-dev-start
```

In the second session, start the backend acceptance server.

```shell
make acceptance-backend-start
```

In the third session, start the acceptance test runner (Playwright UI).

```shell
make acceptance-test
```

## License

The project is licensed under the MIT license.

## Credits and Acknowledgements 🙏

Crafted with care by **{{ cookiecutter.__generator_signature }}**. A special thanks to all contributors and supporters!
