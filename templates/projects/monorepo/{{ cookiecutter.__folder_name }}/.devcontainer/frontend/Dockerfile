# syntax=docker/dockerfile:1
# Development container for the frontend.
# The base image is the project frontend image (frontend/Dockerfile), built by
# the frontend-base service in docker-compose-devcontainers.yml.
FROM {{ cookiecutter.__devops_compose_name }}-devcontainer-frontend-base

USER root

COPY --from=ghcr.io/astral-sh/uv:{{ versions.devcontainer_uv }} /uv /uvx /usr/local/bin/

RUN <<EOT
    set -e
    apt-get update
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        jq \
        less \
        make \
        openssh-client \
        python3 \
        sudo \
        vim-tiny
    rm -rf /var/lib/apt/lists/*
    mkdir -p /home/node/.cache
    chown -R node:node /home/node
    echo "node ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/node
EOT

USER node
WORKDIR /workspace

# The base image checks a running server, which is started by hand here
HEALTHCHECK NONE
ENTRYPOINT []
CMD ["sleep", "infinity"]
