"""Init and utils."""

from zope.i18nmessageid import MessageFactory

import logging


__version__ = "{{ cookiecutter.__version_package }}"

PACKAGE_NAME = "{{ cookiecutter.python_package_name }}"

_ = MessageFactory(PACKAGE_NAME)

logger = logging.getLogger(PACKAGE_NAME)
