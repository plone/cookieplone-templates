---
myst:
  html_meta:
    "description": "This is where description of your Documentation environment will be placed."
    "property=og:description": "Open graph description to your hosted documentation."
    "property=og:title": "{{cookiecutter.title}}"
    "keywords": "documentation, Documentation, docs"  # Space to add your own personal keywords!
---

# {{ cookiecutter.title }}

Welcome to the documentation for **{{ cookiecutter.title }}** !

{{ cookiecutter.description }}.

This template provides a ready-to-use environment for creating comprehensive documentation for Plone projects, powered by the [Plone Sphinx Theme](https://github.com/plone/plone-sphinx-theme).
Whether you're documenting a Plone add-on, a training guide, or a custom deployment, this setup combines the simplicity of Markdown with the power of Sphinx.

The documentation lives in ``{{ cookiecutter.__folder_name }}``

Built with [Markedly Structured Text (MyST)](https://myst-parser.readthedocs.io/en/latest/), this environment supports rich formatting, directives, and extensions tailored for technical documentation.
It’s designed to work seamlessly with Plone’s ecosystem, requiring Python 3.7 or higher.

To get started, explore the sections below or customize this introduction to reflect your project’s unique goals and features through it's documentation.
As this documentation is powered by Plone Sphinx Theme, documentation for the same can be referenced and found [here](https://plone-sphinx-theme.readthedocs.io/).
<!-- Need to add the updated link of documentation here -->

```{todo}
Replace this section with your project introduction and key features.
```

```{toctree}
:caption: How to guides
:hidden: true
:maxdepth: 2

guides/getting-started
guides/usage
```

```{toctree}
:caption: Reference
:hidden: true
:maxdepth: 2

reference/file-system-structure
reference/theme-elements
```

```{toctree}
:maxdepth: 2
:hidden: true
:caption: Appendices

glossary
```
