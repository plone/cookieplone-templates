# syntax=docker/dockerfile:1
# Development container for the backend.
# The base image is the project backend image (backend/Dockerfile), built by
# the backend-base service in docker-compose-devcontainers.yml.
FROM {{ cookiecutter.__devops_compose_name }}-devcontainer-backend-base

COPY --from=ghcr.io/astral-sh/uv:{{ versions.devcontainer_uv }} /uv /uvx /usr/local/bin/

RUN <<EOT
    set -e
    apt-get update
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        gettext \
        jq \
        less \
        openssh-client \
        sudo \
        vim-tiny
    rm -rf /var/lib/apt/lists/*
    # The image uses /app as home of the plone user, give it a real home
    mkdir -p /home/plone/.cache
    chown -R plone:plone /home/plone
    usermod --home /home/plone --shell /bin/bash plone
    echo "plone ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/plone
EOT

USER plone
WORKDIR /workspace

# The base image checks a running server, which is started by hand here
HEALTHCHECK NONE
ENTRYPOINT []
CMD ["sleep", "infinity"]
