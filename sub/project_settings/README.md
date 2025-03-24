[![Cookieplone Project Settings CI](https://github.com/plone/cookieplone-templates/actions/workflows/sub_project_settings.yml/badge.svg)](https://github.com/plone/cookieplone-templates/actions/workflows/sub_project_settings.yml)
[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
![GitHub](https://img.shields.io/github/license/plone/cookieplone-templates)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Cookieplone Project Settings

This is a sub-template -- used by other templates, in automated tests, and for OCI image generation -- accessible with **cookieplone** at the path `sub/project_settings`.

## Getting Started 🏁

### Prerequisites

- **pipx**: A handy tool for installing and running Python applications.

### Installation Guide 🛠️

1. **pipx**

```shell
pip install pipx
```
### Generate Your Project Settings 🎉

```shell
pipx run cookieplone sub/project_settings
```

## Project Generation Options

These are all the template options that will be prompted by the [Cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) before generating your project.

| Option                | Description                                                                                                                                          | Example                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `title`  | Your project's human-readable name, capitals and spaces allowed.                                                                                     | **Project Settings**                |
| `author`              | This is you! The value goes into places like ``LICENSE``, ``package.json`` and such.                                                                     | **Our Company**               |
| `email`               | The email address you want to identify yourself in the project.                                                                                      | **email@example.com**         |
| `volto_version` | Volto version to be used. | **18.0.0-alpha.31**    |


## Code Quality Assurance 🧐

Your package comes equipped with linters to ensure code quality. Run the following to automatically format your code:

```shell
make format
```

## License 📜

This project is licensed under the [MIT License](/LICENSE).

## Let's Get Building! 🚀

Happy coding!
