<p align="center">
    <img alt="Plone Logo" width="200px" src="https://raw.githubusercontent.com/plone/.github/main/plone-logo.png">
</p>

<h1 align="center">
  Cookieplone Templates
</h1>

<div align="center">

![GitHub](https://img.shields.io/github/license/plone/cookiecutter-plone)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

</div>

## About

This project is a collection of templates for Plone integrators to use through [Cookieplone](https://github.com/plone/cookieplone "Link to the GitHub repository of Cookieplone").

## Prerequisites

- **[pipx](https://pipx.pypa.io/stable/ "Link to the website of pipx")**: A tool for installing and running Python applications.

## Installation 💾

Install `pipx` with the following command:

```shell
pip install pipx
```

## Choose a template 🛠️

Select a template with the following command:

```shell
pipx run cookieplone
```

```text
[1/1] Select a template
  1 - A Plone Project
  2 - A Plone Project with Classic UI
  3 - Backend Add-on for Plone
  4 - Frontend Add-on
```

| Template | Description |  |
| --------- | --------- | --------- |
| `A Plone Project`  | Create a new Plone project with backend and frontend components. | [Read More](./project/README.md) |
| `A Plone Classic UI project`  | Create a new Plone project that uses Classic UI (Python only project). | [Read More](./project_classic/README.md) |
| `Backend Add-on for Plone`  | Create a new Python package to be used with Plone. | [Read More](./backend_addon/README.md) |
| `Frontend Add-on for Plone`  | Create a new Node package to be used with Volto. | [Read More](./frontend_addon/README.md) |

## License 📜

This project is licensed under the [MIT License](/LICENSE).

## Let's Get Building! 🚀

Happy coding!
