[![Cookieplone Frontend Add-on CI](https://github.com/plone/cookieplone-templates/actions/workflows/frontend_addon.yml/badge.svg)](https://github.com/plone/cookieplone-templates/actions/workflows/frontend_addon.yml)
[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
![GitHub](https://img.shields.io/github/license/plone/cookieplone-templates)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Cookieplone frontend add-on

Powered by [cookieplone](https://github.com/plone/cookieplone) and [Cookiecutter](https://github.com/cookiecutter/cookiecutter), [Cookieplone Frontend Add-on](https://github.com/plone/cookieplone-templates/frontend_addon) is intended to be used by Plone developers to create new add-on packages for Volto.

## Getting started 🏁

### Prerequisites

- **pipx**: A handy tool for installing and running Python applications.

### Installation guide 🛠️

1. **uv**

[`uv`](https://docs.astral.sh/uv/) is the recommended tool for managing Python versions and project dependencies.

To install `uv`, use the following command, or visit the [`uv` installation page](https://docs.astral.sh/uv/getting-started/installation/) for alternative methods:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh

### Generate Your Plone Add-on 🎉

```shell
uvx cookieplone frontend_addon
```

## Project generation options

These are all the template options that will be prompted by the [Cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) before generating your project.

| Option                | Description                                                                                                                                          | Example                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `frontend_addon_name`  | Your addon's short name.                                                                                     | **volto-weather-block**                |
| `title`  | Your addon's human-readable name, capitals and spaces allowed.                                                                                     | **Weather Block for Volto**                |
| `description`         | Describes your add-on and gets used in places like ``README.md`` and such.                                                                          | **Add a weather block to your site.** |
| `author`              | This is you! The value goes into places like ``LICENSE``, ``package.json`` and such.                                                                     | **Our Company**               |
| `email`               | The email address you want to identify yourself in the project.                                                                                      | **email@example.com**         |
| `github_organization` | Used for GitHub repositories.                                                                                                             | **collective**                |
| `npm_package_name` | Name of the Node package, including the organization (if any). | **@plone-collective/volto-weather-block**    |
| `volto_version` | Volto version to be used. | **18.10.0**    |

## Code quality assurance 🧐

Your package comes equipped with linters to ensure code quality. Run the following to automatically format your code:

```shell
make format
```

## Internationalization 🌐

Generate translation files with ease:

```shell
make i18n
```

## License 📜

This project is licensed under the [MIT License](/LICENSE).

## Let's get building! 🚀

Happy coding!
