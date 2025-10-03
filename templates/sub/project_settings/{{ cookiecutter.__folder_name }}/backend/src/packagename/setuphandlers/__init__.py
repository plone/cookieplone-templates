from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide initial profile from site-creation and quickinstaller."""
        return [
            "{{ cookiecutter.python_package_name }}:initial",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return [
            "{{ cookiecutter.python_package_name }}.upgrades",
        ]
