# syntax=docker/dockerfile:1
ARG VOLTO_VERSION=latest
FROM plone/frontend-builder:${VOLTO_VERSION} AS builder

COPY --chown=node packages/{{cookiecutter.__frontend_addon_name}} /app/packages/{{cookiecutter.__frontend_addon_name}}
COPY --chown=node volto.config.js /app/
COPY --chown=node package.json /app/package.json.temp
COPY --chown=node mrs.developer.json /app/
COPY --chown=node pnpm-workspace.yaml /app/
COPY --chown=node pnpm-lock.yaml /app/pnpm-lock.yaml

RUN --mount=type=cache,id=pnpm,target=/app/.pnpm-store,uid=1000 <<EOT
    set -e
    python3 <<'PYTHON'
import json

with open("package.json.temp") as fh:
    project = json.load(fh)
with open("package.json") as fh:
    data = json.load(fh)
data["dependencies"].update(project["dependencies"])
# Use the project's pnpm version and settings, not the image's ones
data["packageManager"] = project["packageManager"]
data.pop("pnpm", None)
if "pnpm" in project:
    data["pnpm"] = project["pnpm"]
with open("package.json", "w") as fh:
    json.dump(data, fh, indent=2)
PYTHON
    rm package.json.temp
    pnpm dlx mrs-developer missdev --no-config --fetch-https
    pnpm install && pnpm build:deps
    pnpm build
    # This is necessary because the build is trying to recreate the node_modules folder
    # by telling it to CI=1 it will just recreate them
    CI=1 pnpm install --prod
EOT

FROM plone/frontend-prod-config:${VOLTO_VERSION}

LABEL maintainer="{{ cookiecutter.author }} <{{ cookiecutter.email }}>" \
      org.label-schema.name="{{ cookiecutter.project_slug }}-frontend" \
      org.label-schema.description="{{ cookiecutter.title }} frontend image." \
      org.label-schema.vendor="{{ cookiecutter.author }}"

COPY --from=builder /app/ /app/

RUN <<EOT
    set -e
    CI=1 npm i -g corepack@latest && corepack enable pnpm
    CI=1 corepack use pnpm@{{ cookiecutter.__version_pnpm }}
    CI=1 corepack prepare pnpm@{{ cookiecutter.__version_pnpm }} --activate
EOT
