[![Cookieplone Backend Add-on CI](https://github.com/plone/cookieplone-templates/actions/workflows/backend_addon.yml/badge.svg)](https://github.com/plone/cookieplone-templates/actions/workflows/backend_addon.yml)
[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
![GitHub](https://img.shields.io/github/license/plone/cookiecutter-plone)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Cookieplone Backend Add-on

Powered by [cookieplone](https://github.com/plone/cookieplone) and [Cookiecutter](https://github.com/cookiecutter/cookiecutter), [Cookieplone Backend Add-on](https://github.com/plone/cookieplone-templates/backend_addon) is intended to be used by Plone developers to create new addon packages.

## Getting Started 🏁

### Prerequisites

- **pipx**: A handy tool for installing and running Python applications.

### Installation Guide 🛠️

1. **pipx**

```shell
pip install pipx
```
### Generate Your Plone Addon 🎉

```shell
pipx run cookieplone backend_addon
```


## Project Generation Options

These are all the template options that will be prompted by the [Cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) before generating your project.

| Option                | Description                                                                                                                                          | Example                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `title`  | Your addon's human-readable name, capitals and spaces allowed.                                                                                     | **Plone Blog**                |
| `description`         | Describes your addon and gets used in places like ``README.md`` and such.                                                                          | **Create awesome blogs with Plone.** |
| `author`              | This is you! The value goes into places like ``LICENSE``, ``setup.py`` and such.                                                                     | **Our Company**               |
| `email`               | The email address you want to identify yourself in the project.                                                                                      | **email@example.com**         |
| `github_organization` | Used for GitHub and Docker repositories.                                                                                                             | **collective**                |
| `python_package_name` | Name of the Python package used to configure your project. It needs to be Python-importable, so no dashes, spaces or special characters are allowed. | **collective.blog**    |


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
