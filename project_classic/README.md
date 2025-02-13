[![Cookieplone Frontend Add-on CI](https://github.com/plone/cookieplone-templates/actions/workflows/project.yml/badge.svg)](https://github.com/plone/cookieplone-templates/actions/workflows/project.yml)
[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
![GitHub](https://img.shields.io/github/license/plone/cookieplone-templates)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Cookieplone Plone Classic UI project 🌟

Welcome to **Cookieplone Plone Classic UI Project**! Your one-stop solution to kickstart [Plone](https://plone.org/) 6 projects with ease and efficiency. Powered by [cookieplone](https://github.com/plone/cookieplone) and [Cookiecutter](https://github.com/cookiecutter/cookiecutter), this template is designed to save you time and ensure that you get started on the right foot. 🚀

## Features ✨

- Tailored for Plone 6
- Compatible with Python 3.10, 3.11, 3.12, 3.13

## Getting Started 🏁

### Prerequisites

- **pipx**: A handy tool for installing and running Python applications.


### Installation Guide 🛠️

1. **pipx**

```shell
pip install pipx
```


### Generate Your Plone 6 Classic UI Project 🎉

```shell
pipx run cookieplone project_classic
```

### Use options to avoid prompts

Cookieplone will ask a lot of questions.
You can use some of its options to avoid repeatedly entering the same values.


#### `--no-input`

You can use the [`--no-input`](https://cookiecutter.readthedocs.io/en/latest/cli_options.html#cmdoption-cookiecutter-no-input) option to make cookieplone not prompt for parameters and only use `cookiecutter.json` file content.


#### `--replay` and `--replay-file`
You can use the option [`--replay-file`](https://cookiecutter.readthedocs.io/en/latest/cli_options.html#cmdoption-cookiecutter-replay-file) to not prompt for parameters and only use information entered previously or from a specified file.
See [Replay Project Generation](https://cookiecutter.readthedocs.io/en/latest/advanced/replay.html) in the cookiecutter documentation for more information.

### Initial Build

```shell
make install
```

### Start Servers

```shell
make backend-start
```


### Rebuild After Changes

```shell
make install
make backend-start
```

## Project Generation Options 🛠️

Every project is unique, and we provide a variety of options to ensure that your Plone 6 project aligns with your specific needs. Here are the options you can customize during the generation process:

| Option                | Description                                                                                                                                          | Example                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `title`       | Your project's human-readable name, capitals and spaces allowed.                                                                                     | **Plone Site**                |
| `description`         | Describes your project and gets used in places like ``README.md`` and such.                                                                          | **New site for our company.** |
| `project_slug`        | Your project's slug without spaces. Used to name your repository and Docker images.                                                                  | **plone-site**                |
| `hostname`            | Hostname where the project will be deployed.                                                                                                         | **site.plone.org**            |
| `author`              | This is you! The value goes into places like ``LICENSE``, ``setup.py`` and such.                                                                     | **Our Company**               |
| `email`               | The email address you want to identify yourself in the project.                                                                                      | **email@example.com**         |
| `use_prerelease_versions`  | Use non-stable versions of Plone and Volto, (The default value could also be set via `USE_PRERELEASE` environment variable.                                   | **Yes**                       |
| `plone_version`       | Plone version to be used. This queries for the latest available Plone 6 version and presents it to you as the default value.                         | **6.0.0**                     |
| `python_package_name` | Name of the Python package used to configure your project. It needs to be Python-importable, so no dashes, spaces or special characters are allowed. | **plone_site**                |
| `language_code`       | Language to be used on the site.                                                                                                                     | **pt-br**                     |
| `github_organization` | Used for GitHub, GitLab, and Docker repositories.                                                                                                             | **collective**                |
| `container_registry`  | Container registry to be used.                                                                                                                       | **github**                    |
| `devops_ansible`      | Should we create an Ansible playbook to bootstrap and deploy this project?                                                                           | **Yes**                       |
| `devops_gha_deploy`   | Should we create a GitHub action to deploy this project?                                                                                             | **Yes**                       |


## Dive into Your Project's Structure 🏗️

Your generated project will have a well-organized structure, ensuring that both development and maintenance are a breeze. It includes separate sections for backend and devops, each tailored for its specific role.

(Include the Structure and Reasoning section from the previous README.md here, as it provides a good overview of the project structure)

## Code Quality Assurance 🧐

Your project comes equipped with linters to ensure code quality. Run the following to automatically format your code:

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
