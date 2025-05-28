# Cookieplone project settings

[![Cookieplone Templates: CI](https://github.com/plone/cookieplone-templates/actions/workflows/main.yml/badge.svg)](https://github.com/plone/cookieplone-templates/blob/main/.github/workflows/main.yml)
[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
[![License](https://img.shields.io/github/license/plone/cookieplone-templates)](../../../LICENSE)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a subtemplate used by other templates, in automated tests, and for OCI image generation—accessible with **Cookieplone** at the path `sub/project_settings`.


## Prerequisites

-   [uv](https://docs.astral.sh/uv/) is the recommended tool for managing Python versions and project dependencies.
-   Node.js and pnpm: essential for managing and running JavaScript packages.


### uv

To install uv, use the following command, or visit the [uv installation page](https://docs.astral.sh/uv/getting-started/installation/) for alternative methods.

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```


### Node.js

Follow the [Plone documentation](https://6.docs.plone.org/install/install-from-packages.html#pre-requisites-for-installation) for detailed instructions.



## Generate your project settings 🎉

```shell
uvx cookieplone sub/project_settings
```


### Project generation options 🛠️

The table below describes the options you can customize using the [Cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) during the generation process.

| Option                | Description                                                                                                                                          | Example                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `title`  | Your project's human-readable name, capitals and spaces allowed.                                                                                     | `Project Settings`                |
| `author`              | This is you! Its value goes into places like `LICENSE`, `package.json` and other files.                                                                     | `Our Company`               |
| `email`               | The email address to contact the project maintainer.                                                                                      | `email@example.com`         |
| `volto_version` | Volto version to be used. | `18.10.0`    |


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
