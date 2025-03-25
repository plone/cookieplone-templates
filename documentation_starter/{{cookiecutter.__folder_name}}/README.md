# {{ cookiecutter.title }}

Documentation for **{{ cookiecutter.title }}**. {{ cookiecutter.description }}.

This project provides a Sphinx-based documentation environment for your Plone project, powered by the [Plone Sphinx Theme](https://github.com/plone/plone-sphinx-theme). It’s generated using the `documentation_starter` template from [Cookieplone](https://github.com/plone/cookieplone).

## Prerequisites

- **Python 3.7+**: Ensure you have a compatible Python version installed.
- **pip**: For installing dependencies.

## Setup

1. **Install Dependencies**:
   Install the required Python packages, including the latest `plone-sphinx-theme`, using `pip`:
   ```bash
   pip install -e ".[dev]"
   ```

## Building the Documentation
- Build HTML:
Generate the HTML documentation.
    ```bash
    make html
    ```
    or
    ```bash
    make live html
    ```
## Customizing the {{ cookiecutter.title }} Documentation
- Edit Content: Modify files in ``docs/``
- ``index.md``: Main entry point.
- ``guides``: Add how-to guides(e.g., ``guides/getting-started.md``).
- ``reference``: Add reference material(e.g., ``reference/file-system-structure.md``).
- ``appendices``: Add appendices(e.g., ``glossary.md``).
These can be customized as per your need. As the whole docs is traversed, new directory and MyST markdown files are supported.

- Add Styles: For custom CSS, add to ``docs/_static/css/custom.css`` and update ``conf.py``.
```python
html_static_path = ['_static']
html_css_files = ['custom.css']
```

## Checking Links
- To verify links in the documentation, run:
```bash
make linkcheck
```

## Updating Dependencies
- To update dependencies, run:
```bash
make update-deps
```
## License

The project is licensed under GPLv2.

## Project Details
- Author: {{ cookiecutter.author }}
- Version: v1.0

{{ cookiecutter.__generator_signature }} using the ``documentation_starter`` template.
A special thanks to all contributors and supporters!