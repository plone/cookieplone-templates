# syntax=docker/dockerfile:1
ARG NODE_VERSION=24

FROM node:${NODE_VERSION}-slim AS builder
WORKDIR /app
ENV CI=true
RUN npm install --global corepack@latest && corepack enable

# The app and its add-ons in `packages/`, without what `.dockerignore` lists.
COPY --chown=node . .
RUN --mount=type=cache,id=pnpm,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile

RUN <<EOT
    set -e
    pnpm build
    # Keep only what the server needs at runtime.
    pnpm install --prod --frozen-lockfile
EOT

FROM node:${NODE_VERSION}-slim

LABEL maintainer="{{ cookiecutter.author }} <{{ cookiecutter.email }}>" \
      org.label-schema.name="{{ cookiecutter.project_slug }}-frontend" \
      org.label-schema.description="{{ cookiecutter.title }} frontend image." \
      org.label-schema.vendor="{{ cookiecutter.author }}"

WORKDIR /app
ENV NODE_ENV=production PORT=3000
COPY --from=builder --chown=node /app /app
USER node
EXPOSE 3000
CMD ["node", "server.js", "./build/server/index.js"]
