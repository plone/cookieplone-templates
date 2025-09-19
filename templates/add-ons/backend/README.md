# Cookieplone backend add-on

[![Cookieplone Templates: CI](https://github.com/plone/cookieplone-templates/actions/workflows/main.yml/badge.svg)](https://github.com/plone/cookieplone-templates/blob/main/.github/workflows/main.yml)
[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
[![License](https://img.shields.io/github/license/plone/cookieplone-templates)](../../../LICENSE)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Powered by [Cookieplone](https://github.com/plone/cookieplone) and [Cookiecutter](https://github.com/cookiecutter/cookiecutter), [Cookieplone backend add-on](https://github.com/plone/cookieplone-templates/tree/main/templates/add-ons/backend) is intended to be used by Plone developers to create new add-on packages for the Plone backend.


## Prerequisites

-   [uv](https://docs.astral.sh/uv/) is the recommended tool for managing Python versions and project dependencies.


### uv

To install uv, use the following command, or visit the [uv installation page](https://docs.astral.sh/uv/getting-started/installation/) for alternative methods.

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```


## Generate your Plone add-on 🎉

```shell
uvx cookieplone backend_addon
```


### Use options to avoid prompts

Cookieplone will ask a lot of questions, as described under [Project generation options](#project-generation-options).
You can use some of its options to avoid repeatedly entering the same values.


#### `--no-input`

You can use the [`--no-input`](https://cookiecutter.readthedocs.io/en/latest/cli_options.html#cmdoption-cookiecutter-no-input) option to make cookieplone not prompt for parameters and only use `cookiecutter.json` file content.


#### `--replay` and `--replay-file`

You can use the option [`--replay-file`](https://cookiecutter.readthedocs.io/en/latest/cli_options.html#cmdoption-cookiecutter-replay-file) to not prompt for parameters and only use information entered previously or from a specified file.
See [Replay Project Generation](https://cookiecutter.readthedocs.io/en/latest/advanced/replay.html) in the cookiecutter documentation for more information.


### Project generation options 🛠️

The table below describes the options you can customize using the [Cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) during the generation process.

| Option                | Description                                                                                                                                           | Example                            |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------|
| `title`               | Your add-on's human-readable name, capitals and spaces allowed.                                                                                       | `Plone Blog`                       |
| `description`         | Describes your add-on and gets used in places like `README.md` and other files.                                                                              | `Create awesome blogs with Plone.` |
| `author`              | This is you! Its value goes into places like `LICENSE`, `pyproject.toml` and other files.                                                                          | `Our Company`                      |
| `email`               | The email address to contact the project maintainer.                                                                                       | `email@example.com`                |
| `github_organization` | Used for GitHub and Docker repositories.                                                                                                              | `collective`                       |
| `python_package_name` | Name of the Python package used to configure your project. It needs to be Python-importable, so no dashes, spaces, or special characters are allowed. | `collective.blog`                  |


## Code quality assurance 🧐

Your project comes equipped with linters to ensure code quality.
Run the following command to automatically format your code.

```shell
make format
```


## Internationalization 🌐

Generate translation files with the following command.

```shell
make i18n
```


## License 📜

This project is licensed under the [MIT License](/LICENSE).


## Let's get building! 🚀

Happy coding!
