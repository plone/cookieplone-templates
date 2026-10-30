# {{ cookiecutter.title }} frontend ({{ cookiecutter.__npm_package_name }})

{{ cookiecutter.description }}

This folder contains the Plone Aurora frontend of [{{ cookiecutter.title }}](../README.md).
It is a pnpm workspace that checks out Aurora core with `mrs-developer`, and develops the `{{ cookiecutter.__npm_package_name }}` package in `packages/{{ cookiecutter.frontend_addon_name | unscoped_package_name }}`.


## Prerequisites

-   [Node.js](https://6.docs.plone.org/install/create-project.html#node-js) {{ cookiecutter.__node_version }}
-   [Make](https://6.docs.plone.org/install/create-project.html#make)
-   [jq](https://jqlang.org/)
-   [uv](https://docs.astral.sh/uv/)
-   [Docker](https://6.docs.plone.org/install/create-project.html#docker) (optional)

Install and enable the latest Corepack.
Corepack will resolve the pnpm version pinned by the `packageManager` field in `package.json`.

```shell
npm install --global corepack@latest
corepack enable
```


## Aurora version

The Aurora version is the `core.tag` value in `mrs.developer.json`.
The Makefiles read it from there, both for the checkout and for the `plone/aurora-builder` and `plone/aurora-prod-config` container base images.
To upgrade Aurora, change that tag, then run `make install`.


## Make convenience commands

Run `make help` to list the available commands, and `make debug-settings` to show the versions and image name in use.


## Development

Install the frontend.

```shell
make install
```

Start the backend.
From the root of the repository, run `make backend-start`, or start a Docker-based backend from this folder.

```shell
make backend-docker-start
```

In a separate terminal session, start the frontend.

```shell
make start
```


### Lint code

Run ESLint, Prettier, and Stylelint in analyze mode.

```shell
make lint
```


### Format code

Run ESLint, Prettier, and Stylelint in fix mode.

```shell
make format
```


### i18n

Extract the i18n messages to locales.

```shell
make i18n
```


### Unit tests

```shell
make test
```


### Acceptance tests

Install the Playwright browsers once.

```shell
make install-acceptance
```

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


## Container image

Build the frontend container image.

```shell
make build-image
```
