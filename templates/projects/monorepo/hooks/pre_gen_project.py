"""Pre generation hook."""

import sys
from collections import OrderedDict
from pathlib import Path
from textwrap import dedent

from cookieplone import data
from cookieplone.utils import console, validators

output_path = Path().resolve()

context: OrderedDict = {{cookiecutter}}


def check_errors(context: dict) -> data.ContextValidatorResult:
    """Check for errors in the provided data."""
    validations = [
        data.ItemValidator("plone_version", validators.validate_plone_version),
        data.ItemValidator("volto_version", validators.validate_volto_version),
        data.ItemValidator("language_code", validators.validate_language_code),
        data.ItemValidator("hostname", validators.validate_hostname),
        data.ItemValidator(
            "python_package_name", validators.validate_python_package_name
        ),
        data.ItemValidator("frontend_addon_name", validators.validate_volto_addon_name),
    ]
    result = validators.run_context_validations(context, validations)
    return result


def main():
    """Validate context."""
    validation_result = check_errors(context)
    success = validation_result.status
    if not success:
        msg = dedent(
            """
            [bold red]Error[/bold red]
            It will not be possible to generate the project.

            Please review the errors:
            """
        )
        for validation in validation_result.validations:
            if validation.status:
                continue
            label = "red"
            msg = (
                f"{msg}\n  - {validation.key}: [{label}]{validation.message}[/{label}]"
            )
    else:
        msg = dedent(
            f"""
            Summary:

              - Plone version: [bold blue]{{ cookiecutter.plone_version }}[/bold blue]
              - Volto version: [bold blue]{{ cookiecutter.volto_version }}[/bold blue]
              - Output folder: [bold blue]{output_path}[/bold blue]

        """
        )
    console.panel(title="{{ cookiecutter.title }} generation", msg=msg)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
