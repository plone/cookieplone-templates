<!-- [![Cookieplone Documentation Starter CI](https://github.com/plone/cookieplone-templates/actions/workflows/documentation_starter.yml/badge.svg)](https://github.com/plone/cookieplone-templates/actions/workflows/documentation_starter.yml)  -->
[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
![GitHub](https://img.shields.io/github/license/plone/cookiecutter-plone)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Cookieplone Documentation Starter

Powered by [Cookieplone](https://github.com/plone/cookieplone) and [cookiecutter](https://github.com/cookiecutter/cookiecutter), [Cookieplone Documentation Starter](https://github.com/plone/cookieplone-templates/documentation_starter) is intended to be used by Plone developers to create comprehensive documentation for Plone add-ons using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) and [MyST](https://myst-parser.readthedocs.io/en/latest/) or [reStructuredText](https://www.docutils.org/rst.html).

## Getting Started 🏁

### Prerequisites

[`uv`](https://docs.astral.sh/uv/) is the recommended tool for managing Python versions and project dependencies.

To install `uv`, use the following command, or visit the [`uv` installation page](https://docs.astral.sh/uv/getting-started/installation/) for alternative methods:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Generate your documentation scaffold 🎉

```shell
uvx cookieplone project
```

Follow the prompts to create and customize your documentation scaffold.

## Project Generation Options

These are all the template options that will be prompted by the [Cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) before generating your project.

| Option                | Description                                                                                                                                          | Example                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `title`               | Your documentation's human-readable name, capitals and spaces allowed.
| `description`         | Describes your documentation and gets used in places such as `README.md`.                                                                          | `Create awesome blogs with Plone.` |
| `github_organization` | Used for GitHub and Docker repositories.                                                                                                             | `collective`                |
| `author`              | This is you! The value goes into `LICENSE`, `setup.py`, and other files.                                                                     | `Our Company`               |
| `email`               | The email address you want to identify yourself in the project.                                                                                      | `email@example.com`         |

## Build and view documentation 📖

1. Navigate to the project.

```shell
cd <project_title>/docs
```

2. Use the following command to build the documentation.

```shell
make html
```

Your documentation will be built in the `_build` directory.

For additional make commands, run the following command.

```shell
make -l
```


## License 📜

This project is licensed under the [MIT License](/LICENSE).
