<!-- [![Cookieplone Documentation Add-on CI](https://github.com/plone/cookieplone-templates/actions/workflows/documentation_addon.yml/badge.svg)](https://github.com/plone/cookieplone-templates/actions/workflows/documentation_addon.yml)  -->
[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
![GitHub](https://img.shields.io/github/license/plone/cookiecutter-plone)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Cookieplone Documentation Add-on

Powered by [cookieplone](https://github.com/plone/cookieplone) and [Cookiecutter](https://github.com/cookiecutter/cookiecutter), [Cookieplone Documentation Add-on](https://github.com/plone/cookieplone-templates/documentation_addon) is intended to be used by Plone developers to create comprehensive documentation packages for Plone add-ons using Sphinx.

## Getting Started 🏁

### Prerequisites

- **pipx**: A tool for installing and running Python applications.

### Installation Guide 🛠️

1. **Install pipx** (if not already installed):

```shell
pip install pipx
```

2. **Generate Your Documentation using Add-on🎉**

```shell
pipx run cookie
```
Follow the prompts to customize your documentation project.

## Project Generation Options

These are all the template options that will be prompted by the [Cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) before generating your project.

| Option                | Description                                                                                                                                          | Example                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `title`               | Your documentation's human-readable name, capitals and spaces allowed.
| `description`         | Describes your documentation add-on and gets used in places like ``README.md`` and such.                                                                          | **Create awesome blogs with Plone.** |
| `github_organization` | Used for GitHub and Docker repositories.                                                                                                             | **collective**                |
| `author`              | This is you! The value goes into places like ``LICENSE``, ``setup.py`` and such.                                                                     | **Our Company**               |
| `email`               | The email address you want to identify yourself in the project.                                                                                      | **email@example.com**         |

## Building and Viewing Documentation📖

1. Navigate to the project.

```shell
cd <documentation_title>
```

2. Run the following command to take look at available make modes.

```shell
make -l
```

3. Use the following command to build the documentation.

```shell
make html
```

Your documentation will be built in the `_build` directory.

## License 📜

This project is licensed under the [MIT License](/LICENSE).
