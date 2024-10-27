"""Init and utils."""
import logging
from zope.i18nmessageid import MessageFactory


PACKAGE_NAME = "{{ cookiecutter.python_package_name }}"

_ = MessageFactory(PACKAGE_NAME)

logger = logging.getLogger(PACKAGE_NAME)
