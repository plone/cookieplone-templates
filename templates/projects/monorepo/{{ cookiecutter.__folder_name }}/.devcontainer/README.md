# Development containers

Development containers for {{ cookiecutter.title }}, usable with [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) or any tool supporting the [Development Containers specification](https://containers.dev/).

| Container | Configuration | Base image | Forwarded ports |
| --- | --- | --- | --- |
| Backend | `.devcontainer/backend` | `backend/Dockerfile` | 8080 (Plone) |
{%- if cookiecutter.feature_headless %}
| Frontend | `.devcontainer/frontend` | `frontend/Dockerfile` | 3000 (Volto), 3001 (hot reload) |
{%- endif %}

Each development container extends the project image with development tooling (uv, git, make, compilers, jq, sudo).
The images are defined in `docker-compose-devcontainers.yml`.

## Usage

In VS Code, run **Dev Containers: Reopen in Container** and pick a configuration.
On first start the container installs the codebase with `make backend-install`{% if cookiecutter.feature_headless %} or `make frontend-install`{% endif %}.

Start Plone in the backend container:

```shell
make backend-start
```
{%- if cookiecutter.feature_headless %}

Start Volto in the frontend container:

```shell
make frontend-start
```

The frontend container shares the network of the backend container, so Volto reaches Plone on `localhost:8080`.
Opening the frontend container also starts the backend container; open the backend configuration in a second window to work on it.
{%- endif %}

## Notes

- The repository is mounted at `/workspace`.
- Platform specific files are kept in Docker volumes instead of the host checkout: `backend/.venv`{% if cookiecutter.feature_headless %}, `backend/instance` and the frontend `node_modules`{% else %} and `backend/instance`{% endif %}.
  The host and the containers each have their own installation.
- The first build also builds the project images, which takes a while.
- To rebuild the images after changing a `Dockerfile`, run **Dev Containers: Rebuild Container**.
- To remove the containers and volumes, run `docker compose -f docker-compose-devcontainers.yml down --volumes`.
