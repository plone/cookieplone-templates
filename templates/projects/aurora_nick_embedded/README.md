[![Cookieplone Aurora Nick Embedded CI](https://github.com/plone/cookieplone-templates/actions/workflows/frontend_addon.yml/badge.svg)](https://github.com/plone/cookieplone-templates/actions/workflows/frontend_addon.yml)
[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
![GitHub](https://img.shields.io/github/license/plone/cookiecutter-plone)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Cookieplone Aurora with embedded Nick

Powered by [cookieplone](https://github.com/plone/cookieplone), this template creates an experimental Plone Aurora project with Nick embedded in the same Node.js workspace. The shared frontend scaffold is generated from the `aurora_addon` template.

## Getting Started 🏁

### Prerequisites

- **uv**: An extremely fast Python package and project manager.

### Installation Guide 🛠️

1. **uv**

```shell
pip install uv
```

### Generate your project 🎉

```shell
uvx cookieplone aurora_nick_embedded
```

## Project Generation Options

These are all the template options that will be prompted by the [Cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) before generating your project.

| Option                | Description                                                                                                                                          | Example                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `frontend_addon_name`  | Your Aurora add-on's short name.                                                                                     | **aurora-nick-embedded**                |
| `title`  | Your project's human-readable name, capitals and spaces allowed.                                                                                     | **Aurora with embedded Nick**                |
| `description`         | Describes your project and gets used in places like `README.md`.                                                                          | **Plone Aurora using Nick as an embedded library.** |
| `author`              | This is you! The value goes into places like ``LICENSE``, ``package.json`` and such.                                                                     | **Our Company**               |
| `email`               | The email address you want to identify yourself in the project.                                                                                      | **email@example.com**         |
| `github_organization` | Used for GitHub repositories.                                                                                                             | **collective**                |
| `npm_package_name` | Name of the Node package, including the organization (if any). | **@plone-collective/aurora-nick-embedded**    |

## Code Quality Assurance 🧐

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

## Let's Get Building! 🚀

Happy coding!
