# Cookieplone documentation starter

[![Cookieplone Templates: CI](https://github.com/plone/cookieplone-templates/actions/workflows/main.yml/badge.svg)](https://github.com/plone/cookieplone-templates/blob/main/.github/workflows/main.yml)
[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
![GitHub](https://img.shields.io/github/license/plone/cookieplone-templates)

Powered by [Cookieplone](https://github.com/plone/cookieplone) and [Cookiecutter](https://github.com/cookiecutter/cookiecutter), [Cookieplone documentation starter](https://github.com/plone/cookieplone-templates/tree/main/templates/docs/starter) is intended to be used by Plone developers to create comprehensive documentation for Plone add-ons using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) and [MyST](https://myst-parser.readthedocs.io/en/latest/) or [reStructuredText](https://www.docutils.org/rst.html).

## Prerequisites

[uv](https://docs.astral.sh/uv/) is the recommended tool for managing Python versions and project dependencies.

To install uv, use the following command, or visit the [uv installation page](https://docs.astral.sh/uv/getting-started/installation/) for alternative methods.

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Generate your documentation scaffold 🎉

```shell
uvx cookieplone project
```

Follow the prompts to create and customize your documentation scaffold.


### Use options to avoid prompts

Cookieplone will ask a lot of questions, as described under [Project generation options](#project-generation-options).
You can use some of its options to avoid repeatedly entering the same values.


#### `--no-input`

You can use the [`--no-input`](https://cookiecutter.readthedocs.io/en/latest/cli_options.html#cmdoption-cookiecutter-no-input) option to make cookieplone not prompt for parameters and only use `cookiecutter.json` file content.


## Project generation options

These are all the template options that will be prompted by the [Cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) before generating your project.

| Option | Description | Example |
| ------ | ----------- | ------- |
| `title` | Your documentation's human-readable name, capitals and spaces allowed. | `My Project Title` |
| `description` | Describes your documentation and gets used in places such as `README.md`. | `Create awesome blogs with Plone.` |
| `github_organization` | Used for GitHub and Docker repositories. | `collective` |
| `author` | This is you! Its value goes into `LICENSE`, `pyproject.toml`, and other files. | `Our Company` |
| `email` | The email address to contact the project maintainer. | `email@example.com` |


## Build and view documentation 📖

Navigate to your project.

```shell
cd <project_title>/docs
```

Use the following command to build the documentation.

```shell
make html
```

Your documentation will be built in the `_build` directory.

For additional make commands, run the following command in `<project_title>/docs`.

```shell
make help
```


## Create documentation for an existing project

If you have an existing project created by Cookieplone, you can create documentation for it.

Run Cookieplone with the following command, making the same choices as your existing project.

```shell
uvx cookieplone project
```

Then copy your project files into the new Cookieplone file structure.
See also the first note in the [Upgrade Guide](https://6.docs.plone.org/volto/upgrade-guide/index.html).


## License 📜

This project is licensed under the [MIT License](/LICENSE).


## Let's get writing! 🚀

Happy documenting!
