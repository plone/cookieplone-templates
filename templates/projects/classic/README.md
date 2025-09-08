# Cookieplone Plone Classic UI Project 🌟

[![Cookieplone Templates: CI](https://github.com/plone/cookieplone-templates/actions/workflows/main.yml/badge.svg)](https://github.com/plone/cookieplone-templates/blob/main/.github/workflows/main.yml)
[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
[![License](https://img.shields.io/github/license/plone/cookieplone-templates)](../../../LICENSE)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Welcome to **Cookieplone Plone Classic UI Project**!
Your one-stop solution to kickstart [Plone](https://plone.org/) 6 projects with ease and efficiency.
Powered by [Cookieplone](https://github.com/plone/cookieplone) and [Cookiecutter](https://github.com/cookiecutter/cookiecutter), these templates are designed to save you time and ensure that you get started on the right foot. 🚀


## Prerequisites

-   [uv](https://docs.astral.sh/uv/) is the recommended tool for managing Python versions and project dependencies.


### uv

To install uv, use the following command, or visit the [uv installation page](https://docs.astral.sh/uv/getting-started/installation/) for alternative methods.

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```


## Generate your Plone 6 project 🎉

```shell
uvx cookieplone classic_project
```


### Use options to avoid prompts

Cookieplone will ask a lot of questions, as described under [Project generation options](#project-generation-options).
You can use some of its options to avoid repeatedly entering the same values.


#### `--no-input`

You can use the [`--no-input`](https://cookiecutter.readthedocs.io/en/latest/cli_options.html#cmdoption-cookiecutter-no-input) option to make cookieplone not prompt for parameters and only use `cookiecutter.json` file content.


#### `--replay` and `--replay-file`

You can use the option [`--replay-file`](https://cookiecutter.readthedocs.io/en/latest/cli_options.html#cmdoption-cookiecutter-replay-file) to not prompt for parameters and only use information entered previously or from a specified file.
See [Replay Project Generation](https://cookiecutter.readthedocs.io/en/latest/advanced/replay.html) in the cookiecutter documentation for more information.


## Develop your project

This section provides commands that you will frequently use during development.


### Initial build

```shell
make install
```


### Start servers

Start the backend server with the following command.

```shell
make backend-start
```


### Rebuild after changes

After you make changes to your code, you will need to install the changes and restart the server.

```shell
make install
make backend-start
```


## Project generation options 🛠️

The table below describes the options you can customize using the [Cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) during the generation process.

| Option                | Description                                                                                                                                          | Example                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `title`       | Your project's human-readable name, capitals and spaces allowed.                                                                                     | `Plone Site`                |
| `description`         | Describes your project and gets used in places like ``README.md`` and other files.                                                                          | `New site for our company.` |
| `project_slug`        | Your project's slug without spaces. Used to name your repository and Docker images.                                                                  | `plone-site`                |
| `hostname`            | Hostname where the project will be deployed.                                                                                                         | `site.plone.org`            |
| `author`              | This is you! Its value goes into places like ``LICENSE``, ``pyproject.toml`` and other files.                                                                     | `Our Company`               |
| `email`               | The email address to contact the project maintainer.                                                                                      | `email@example.com`         |
| `use_prerelease_versions`  | Use pre-release versions of Plone, including alpha and beta releases. The default value could also be set via `USE_PRERELEASE` environment variable.                                   | `Yes`                       |
| `plone_version`       | Plone version to be used. This queries for the latest available Plone 6 version and presents it to you as the default value.                         | `6.0.0`                     |
| `python_package_name` | Name of the Python package used to configure your project. It needs to be Python-importable, so no dashes, spaces or special characters are allowed. | `plone_site`                |
| `language_code`       | Language to be used on the site.                                                                                                                     | `pt-br`                     |
| `github_organization` | Used for GitHub, GitLab, and Docker repositories.  GitHub or GitLab username or organization slug from URL.                                           | `collective`                |
| `container_registry`  | Container registry to be used.                                                                                                                       | `github`                    |
| `devops_storage`      | Storage backend to be used in the deployment stack.                                                                                                  | `relstorage`                |
| `devops_ansible`      | Should we create an Ansible playbook to bootstrap and deploy this project?                                                                           | `Yes`                       |
| `devops_gha_deploy`   | Should we create a GitHub action to deploy this project?                                                                                             | `Yes`                       |


## Dive into your project's structure 🏗️

Your generated project will have a well-organized structure, ensuring that both development and maintenance are a breeze.
It includes separate sections for backend and devops, each tailored for its specific role.

(Include the Structure and Reasoning section from the previous README.md here, as it provides a good overview of the project structure)


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
