# {{ cookiecutter.title }} ({{ cookiecutter.__npm_package_name }})

{{ cookiecutter.description }}

[![npm](https://img.shields.io/npm/v/{{ cookiecutter.__npm_package_name }})](https://www.npmjs.com/package/{{ cookiecutter.__npm_package_name }})
[![](https://img.shields.io/badge/-Storybook-ff4785?logo=Storybook&logoColor=white&style=flat-square)](https://{{ cookiecutter.github_organization }}.github.io/{{ cookiecutter.frontend_addon_name }}/)
[![Code analysis checks]({{ cookiecutter.__repository_url }}/actions/workflows/code.yml/badge.svg)]({{ cookiecutter.__repository_url }}/actions/workflows/code.yml)
[![Unit tests]({{ cookiecutter.__repository_url }}/actions/workflows/unit.yml/badge.svg)]({{ cookiecutter.__repository_url }}/actions/workflows/unit.yml)

## Features

<!-- List your awesome features here -->

## Installation

To install your project, you must choose the method appropriate to your version of Volto.


### Volto 18 and later

Add `{{ cookiecutter.__npm_package_name }}` to your `package.json`:

```json
"dependencies": {
    "{{ cookiecutter.__npm_package_name }}": "*"
}
```

Add `{{ cookiecutter.__npm_package_name }}` to your `volto.config.js`:

```javascript
const addons = ['{{ cookiecutter.__npm_package_name }}'];
```

If this package provides a Volto theme, and you want to activate it, then add the following to your `volto.config.js`:

```javascript
const theme = '{{ cookiecutter.__npm_package_name }}';
```

### Volto 17 and earlier

Create a new Volto project (you can skip this step if you already have one):

```
npm install -g yo @plone/generator-volto
yo @plone/volto my-volto-project --addon {{ cookiecutter.__npm_package_name }}
cd my-volto-project
```

Add `{{ cookiecutter.__npm_package_name }}` to your package.json:

```JSON
"addons": [
    "{{ cookiecutter.__npm_package_name }}"
],

"dependencies": {
    "{{ cookiecutter.__npm_package_name }}": "*"
}
```

Download and install the new add-on by running:

```
yarn install
```

Start volto with:

```
yarn start
```

## Test installation

Visit http://localhost:3000/ in a browser, login, and check the awesome new features.


## Development

The development of this add-on is done in isolation using a new approach using pnpm workspaces and latest `mrs-developer` and other Volto core improvements.
For this reason, it only works with pnpm and Volto 18 (currently in alpha).


### Prerequisites ✅

-   An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
-   [nvm](https://6.docs.plone.org/install/create-project-cookieplone.html#nvm)
-   [Node.js and pnpm](https://6.docs.plone.org/install/create-project.html#node-js) {{ cookiecutter.__node_version }}
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
-   [Docker](https://docs.docker.com/get-started/get-docker/) (optional)

### Installation 🔧

1.  Clone this repository, then change your working directory.

    ```shell
    git clone {{ cookiecutter.__repository_git }}.git
    cd {{ cookiecutter.__project_slug }}
    ```

2.  Install this code base.

    ```shell
    make install
    ```


### Make convenience commands

Run `make help` to list the available commands.

```text
help                             Show this help
install                          Installs the add-on in a development environment
start                            Starts Volto, allowing reloading of the add-on during development
build                            Build a production bundle for distribution of the project with the add-on
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
acceptance-test                  Start Cypress in interactive mode
ci-acceptance-test               Run cypress tests in headless mode for CI
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

### Run Cypress tests

Run each of these steps in separate terminal sessions.

In the first session, start the frontend in development mode.

```shell
make acceptance-frontend-dev-start
```

In the second session, start the backend acceptance server.

```shell
make acceptance-backend-start
```

In the third session, start the Cypress interactive test runner.

```shell
make acceptance-test
```

## License

The project is licensed under the MIT license.

## Credits and acknowledgements 🙏

{{ cookiecutter.__generator_signature }}. A special thanks to all contributors and supporters!
