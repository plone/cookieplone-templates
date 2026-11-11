# {{ cookiecutter.title }} 🚀

[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookieplone-0083be.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)

{{ cookiecutter.description }}

## Quick start

### Prerequisites

- Node.js {{ cookiecutter.__node_version }}
- pnpm
- Make
- PostgreSQL

### Installation

```shell
git clone {{ cookiecutter.__repository_git }}.git
cd {{ cookiecutter.__project_slug }}
make install
```

Configure the PostgreSQL connection in `backend/config.ts`, then run the
migrations and install the profiles:

```shell
make backend-migrate
```

Start the Nick backend and Aurora frontend in separate terminal sessions:

```shell
make backend-start
make frontend-start
```

The backend is available at http://localhost:8080 and Aurora at http://localhost:3000.

## Project structure

- `backend`: the Plone API powered by Nick, with the project's Nick add-on in
  `backend/packages/{{ cookiecutter.__backend_addon_folder }}`.
- `frontend`: the Aurora application and project add-on.
- `news`: project-level Towncrier entries.

## Repository

{{ cookiecutter.__repository_url }}

## Credits

Crafted with care by {{ cookiecutter.author }} <{{ cookiecutter.email }}>.

{{ cookiecutter.__generator_signature }}
