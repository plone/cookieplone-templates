# {{ cookiecutter.title }} backend

{{ cookiecutter.description }}

The backend is a [Nick](https://nick.docs.plone.org) site. Its code and content
live in the add-on `{{ cookiecutter.backend_addon_name }}`, in
`packages/{{ cookiecutter.__backend_addon_folder }}`: profiles, migrations,
content types, behaviors and REST services. See
[Add-ons](https://nick.docs.plone.org/developer-guide/addons).

## Development

Install the dependencies. This checks out Nick in `src/develop/nick`:

```shell
make install
```

Configure the PostgreSQL connection in `config.ts`, then run the migrations
and install the profiles (`@plone/nick:core` and
`{{ cookiecutter.backend_addon_name }}:default`):

```shell
make migrate
```

Start the backend:

```shell
make start
```

## Container image

`Dockerfile` builds the production image on the official
[`plone/nick`](https://hub.docker.com/r/plone/nick) image: it copies the
add-ons in `packages` into it and installs the profiles of
`{{ cookiecutter.backend_addon_name }}`. Configure it with environment
variables (`DB_HOST`, `DB_PASSWORD`, `SECRET`, ...).

```shell
make build-image
```

`docker compose up` runs the image with a PostgreSQL database.

## Repository

https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}

## Credits

Crafted with care by {{ cookiecutter.author }} <{{ cookiecutter.email }}>.

{{ cookiecutter.__generator_signature }}
