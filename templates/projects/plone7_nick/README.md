[![Cookieplone Plone 7 Nick Standalone Backend CI](https://github.com/plone/cookieplone-templates/actions/workflows/frontend_addon.yml/badge.svg)](https://github.com/plone/cookieplone-templates/actions/workflows/frontend_addon.yml)
[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
![GitHub](https://img.shields.io/github/license/plone/cookiecutter-plone)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Cookieplone Plone 7 Alpha Using Nick As Standalone Backend

Powered by [cookieplone](https://github.com/plone/cookieplone) and [Cookiecutter](https://github.com/cookiecutter/cookiecutter), this template generates a standalone Node.js project based on Nick.

## Getting Started

Generate a project with:

```shell
uvx cookieplone project plone7_nick
```

## Project Generation Options

| Option | Description | Example |
| ------ | ----------- | ------- |
| `title` | Human-readable project title. | `Plone` |
| `project_slug` | Output folder and technical project identifier. | `plone` |
| `description` | Short project description. | `A standalone Nick-based Plone project.` |
| `author` | Author or organization. | `Plone Community` |
| `email` | Contact email for the project. | `collective@plone.org` |
| `github_organization` | GitHub organization or username. | `collective` |
| `npm_package_name` | Generated package name. | `plone` |

## Development

Run the template tests with:

```shell
make test
```
