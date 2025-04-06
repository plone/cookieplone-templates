# {{ cookiecutter.title }}

Documentation for {{ cookiecutter.__folder_name }}.
{{ cookiecutter.description }}

This project provides a Sphinx-based documentation environment for your Plone project, powered by the [Plone Sphinx Theme](https://github.com/plone/plone-sphinx-theme).
It's generated using the `documentation_starter` template from [Cookieplone](https://github.com/plone/cookieplone).


## Prerequisites

-   [uv](https://docs.astral.sh/uv/) is the recommended tool for managing Python versions and project dependencies.

To install uv, use the following command, or visit the [uv installation page](https://docs.astral.sh/uv/getting-started/installation/) for alternative methods.

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```


## Build documentation

To build the HTML documentation, issue the following command.

```shell
make html
```

To build the HTML documentation and view a live preview while editing your documentation, issue the following command.

```shell
make livehtml
```

To check for broken links in your documentation, issue the following command.

```shell
make linkcheckbroken
```

For more `make` commands, issue the following command.

```shell
make help
```


## Customize the {{ cookiecutter.title }} documentation

% TODO

