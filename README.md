<p align="center">
    <img alt="Plone Logo" width="200px" src="https://raw.githubusercontent.com/plone/.github/main/plone-logo.png">
</p>

<h1 align="center">
  Cookieplone Templates
</h1>

<div align="center">

![License](https://img.shields.io/github/license/plone/cookieplone-templates)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
  1 - Volto Project
  2 - Classic UI Project
  3 - Backend Add-on for Plone
  4 - Frontend Add-on for Plone
  5 - Documentation scaffold for Plone projects
```

| Template | Description | `README.md` |
| --------- | --------- | --------- |
| `Volto Project`  | Create a new Plone project that uses the Volto frontend. | [Read more](./templates/projects/monorepo/README.md) |
| `Classic UI Project`  | Create a new Plone project that uses Classic UI. | [Read More](./templates/projects/classic/README.md) |
| `Backend Add-on for Plone`  | Create a new Python package to be used with Plone. | [Read more](./templates/add-ons/backend/README.md) |
| `Frontend Add-on for Plone`  | Create a new Node.js package to be used with Volto. | [Read more](./templates/add-ons/frontend/README.md) |
| `Documenation scaffold`  | Create a documentation scaffold for your package. | [Read more](./templates/add-ons/documentation_starter/README.md) |


## Contribute 🤝

We welcome contributions to `cookieplone-templates`.

You can create an issue in the issue tracker, or contact a maintainer.

- [Issue Tracker](https://github.com/plone/cookieplone-templates/issues)
- [Source Code](https://github.com/plone/cookieplone-templates/)


### Development requirements

See [Installation](#installation-).

For source control through Git and continuous integration and delivery (CI/CD), you'll also need a Git repository either under your personal or organization's account.
Both [GitHub](https://github.com/) and [GitLab](https://about.gitlab.com/) are currently supported Git repository and CI/CD service providers.
However, only GitHub is currently supported for documentation hosting.


### Setup

Create a local Python virtual environment with the following command.

```shell
make install
```

### Run the checked out branch of `cookieplone-templates`.

```shell
COOKIEPLONE_REPOSITORY=~/YOUR_PATH_TO/cookieplone-templates uvx cookieplone project --no-input
```


### Run a remote branch of `cookieplone-templates`.

```shell
COOKIEPLONE_REPOSITORY_TAG=<REMOTE_BRANCH_NAME> uvx cookieplone
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

[`pytest`](https://docs.pytest.org/en/stable/) is this package's test runner.

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


### Publish to Git service provider

To publish your project to your Git service provider, first create an empty remote repository with your Git service provider.
Then navigate to the root of your generated project folder.
Finally, issue the following commands.

> [!NOTE]
> If your remote repository is private, you'll need to manage authorization when you push commits upstream.

```shell
git status
git commit -m "first commit"
git remote add origin https://<git_service_provider>/<organization_or_username>/<project_slug>.git
git branch -M main
git push
```

Your remote repository should now be populated with your generated project.


### Publish documentation to Read the Docs

The Cookieplone template `documentation_starter` supports publishing documentation and pull request preview builds on Read the Docs.

First, create an account on Read the Docs, then follow their documentation to add a documentation project and configure pull request previews.

-   [Adding a documentation project](https://docs.readthedocs.com/platform/stable/intro/add-project.html)
-   [How to configure pull request builds](https://docs.readthedocs.com/platform/stable/guides/pull-requests.html)
-   [Pull request previews](https://docs.readthedocs.com/platform/stable/pull-requests.html)

Next, update your documentation files.
Search for the string `MY_READTHEDOCS_PROJECT_SLUG` throughout your project, and replace it your project's slug that Read the Docs assigned to your project.

Finally, commit and push your changes to your remote repository.

Read the Docs will build documentation and with the next pull request, will build a pull request preview and insert a link to the preview in your pull request.

> [!NOTE]
> It's currently not supported to check for a unique slug on Read the Docs before generating your project, especially if you set up a private repository.


## License 📜

This project is licensed under the [MIT License](/LICENSE).


## Let's get building! 🚀

Happy coding!
