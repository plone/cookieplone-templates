# syntax=docker/dockerfile:1
# Production image: the official Nick image with the add-ons of this project.
# NICK_VERSION is the plone/nick image to build on.
ARG NICK_VERSION={{ versions.backend_nick }}
FROM plone/nick:${NICK_VERSION}

LABEL maintainer="{{ cookiecutter.author }} <{{ cookiecutter.email }}>" \
      org.label-schema.name="{{ cookiecutter.project_slug }}-backend" \
      org.label-schema.description="{{ cookiecutter.title }} backend image." \
      org.label-schema.vendor="{{ cookiecutter.author }}"

# The add-ons are workspace packages of the image, and use its @plone/nick
COPY --chown=node:node packages /app/packages
RUN pnpm add "{{ cookiecutter.backend_addon_name }}@workspace:*"

ENV PROFILES=@plone/nick:core,{{ cookiecutter.backend_addon_name }}:default
