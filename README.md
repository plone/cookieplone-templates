<p align="center">
    <img alt="Plone Logo" width="200px" src="https://raw.githubusercontent.com/plone/.github/main/plone-logo.png">
</p>

<h1 align="center">
  Cookieplone Templates
</h1>

<div align="center">

![GitHub](https://img.shields.io/github/license/plone/cookieplone-templates)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

</div>

## About

This project is a collection of templates for Plone integrators to use through [Cookieplone](https://github.com/plone/cookieplone "Link to the GitHub repository of Cookieplone").


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


## Choose a template 🛠️

Select a template with the following command:

```shell
uvx cookieplone
```

```text
[1/1] Select a template
  1 - A Plone Project
  2 - Backend Add-on for Plone
  3 - Frontend Add-on
```

| Template | Description |  |
| --------- | --------- | --------- |
| `A Plone Project`  | Create a new Plone project with backend and frontend components. | [Read More](./project/README.md) |
| `Backend Add-on for Plone`  | Create a new Python package to be used with Plone. | [Read More](./backend_addon/README.md) |
| `Frontend Add-on for Plone`  | Create a new Node package to be used with Volto. | [Read More](./frontend_addon/README.md) |

## License 📜

This project is licensed under the [MIT License](/LICENSE).

## Let's Get Building! 🚀

Happy coding!
