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


## Installation 💾

Set up your system with Plone's [Prerequisites for installation](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation).


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
| `Frontend Add-on for Plone`  | Create a new Node.js package to be used with Volto. | [Read More](./frontend_addon/README.md) |


## Contribute 🤝

We welcome contributions to `cookieplone-templates`.

You can create an issue in the issue tracker, or contact a maintainer.

- [Issue Tracker](https://github.com/plone/cookieplone-templates/issues)
- [Source Code](https://github.com/plone/cookieplone-templates/)


### Development requirements

See [Installation](#installation-).


### Setup

Create a local Python virtual environment with the following command.

```shell
make install
```

### Run the checked out branch of `cookieplone-templates`.

```shell
COOKIEPLONE_REPOSITORY=~/YOUR_PATH_TO/cookieplone-templates uvx cookieplone project --no-input
```


### Format the codebase

```shell
make format
```


### Format the templates

```shell
make format_templates
```


### Run tests

[`pytest`](https://docs.pytest.org/) is this package's test runner.

Run all tests with the following command.

```shell
make test
```

Run all tests, but stop on the first error and open a `pdb` session with the following command.

```shell
uv run pytest -x --pdb
```

Run only tests that match `test_template_has_required_keys` with the following command.

```shell
uv run pytest -k test_template_has_required_keys
```

Run only tests that match `test_template_has_required_keys`, but stop on the first error and open a `pdb` session with the following command.

```shell
uv run pytest -k test_template_has_required_keys -x --pdb
```


## License 📜

This project is licensed under the [MIT License](/LICENSE).

## Let's Get Building! 🚀

Happy coding!
