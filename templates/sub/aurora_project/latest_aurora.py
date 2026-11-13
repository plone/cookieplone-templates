"""Jinja filter for resolving the latest published Aurora version."""

import requests
from cookiecutter.utils import simple_filter
from cookieplone import settings
from requests import RequestException


@simple_filter
def latest_aurora(_value: object) -> str:
    """Return the latest version published for ``@plone/aurora``."""
    try:
        response = requests.get(
            "https://registry.npmjs.org/@plone/aurora",
            headers={"Accept": "application/vnd.npm.install-v1+json"},
            timeout=settings.REQUESTS_TIMEOUT,
        )
        response.raise_for_status()
        return response.json().get("dist-tags", {}).get("latest", "")
    except (RequestException, TypeError, ValueError):
        return ""
