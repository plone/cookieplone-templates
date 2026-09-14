# syntax=docker/dockerfile:1
ARG VARNISH_VERSION={{ versions.devops_varnish_version }}
FROM varnish:${VARNISH_VERSION}

LABEL maintainer="{{ cookiecutter.author }} <{{ cookiecutter.email }}>" \
      org.label-schema.name="{{ cookiecutter.project_slug }}-varnish" \
      org.label-schema.description="{{ cookiecutter.title }} Varnish image." \
      org.label-schema.vendor="{{ cookiecutter.author }}"

COPY etc/varnish.vcl /etc/varnish/default.vcl
