# Cookieplone cache settings

[![Cookieplone Cache Settings CI](https://github.com/plone/cookieplone-templates/actions/workflows/sub_cache.yml/badge.svg)](https://github.com/plone/cookieplone-templates/actions/workflows/sub_cache.yml)
[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
![GitHub](https://img.shields.io/github/license/plone/cookieplone-templates)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

This is a sub-template -- used by other templates, in automated tests, and for OCI image generation -- accessible with **cookieplone** at the path `sub/cache`.

## Prerequisites

-   [uv](https://docs.astral.sh/uv/) is the recommended tool for managing Python versions and project dependencies.


### uv

To install uv, use the following command, or visit the [uv installation page](https://docs.astral.sh/uv/getting-started/installation/) for alternative methods.

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```


## Generate your cache settings 🎉

```shell
uvx cookieplone sub/cache
```


## Project generation options 🛠️

The table below describes the options you can customize using the [Cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) during the generation process.

| Option                | Description                                                                                                                                          | Example                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `title`  | Your project's human-readable name, capitals and spaces allowed.                                                                                     | **Cache Settings**                |
| `author`              | This is you! The value goes into places like ``LICENSE``, ``package.json`` and such.                                                                     | **Our Company**               |
| `email`               | The email address you want to identify yourself in the project.                                                                                      | **email@example.com**         |
| `volto_version` | Volto version to be used. | **18.10.0**    |


## Code quality assurance 🧐

Your project comes equipped with linters to ensure code quality.
Run the following command to automatically format your code.

```shell
make format
```


## License 📜

This project is licensed under the [MIT License](/LICENSE).


## Let's get building! 🚀

Happy coding!
