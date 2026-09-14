[![Cookieplone Volto Nick CI](https://github.com/plone/cookieplone-templates/actions/workflows/frontend_addon.yml/badge.svg)](https://github.com/plone/cookieplone-templates/actions/workflows/frontend_addon.yml)
[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
![GitHub](https://img.shields.io/github/license/plone/cookiecutter-plone)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Plone Volto using Nick as backend

Powered by [cookieplone](https://github.com/plone/cookieplone) and [Cookiecutter](https://github.com/cookiecutter/cookiecutter), this template generates a Plone Volto project using Nick as backend.

## Getting Started

Generate a project with:

```shell
uvx cookieplone project volto_nick
```

## Project Generation Options

| Option | Description | Example |
| ------ | ----------- | ------- |
| `title` | Human-readable project title. | `Plone` |
| `project_slug` | Output folder and technical project identifier. | `plone` |
| `description` | Short project description. | `Plone Volto using Nick as backend.` |
| `author` | Author or organization. | `Plone Community` |
| `email` | Contact email for the project. | `collective@plone.org` |
| `github_organization` | GitHub organization or username. | `collective` |
| `npm_package_name` | Nick backend package name. | `plone` |
| `frontend_addon_name` | Volto frontend add-on package name. | `volto-plone` |
| `use_prerelease_versions` | Allow prerelease Volto versions. | `false` |
| `volto_version` | Volto version used by the frontend. | `19.0.0` |

## Development

Run the template tests with:

```shell
make test
```

