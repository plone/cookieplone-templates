---
myst:
  html_meta:
    "description": "{{ cookiecutter.description }}"
    "property=og:description": "{{ cookiecutter.description }}"
    "property=og:title": "{{ cookiecutter.title }}"
    "keywords": "{{ cookiecutter.title }}, documentation, {{ cookiecutter.description }}"
---

# {{ cookiecutter.title }}

Welcome to the documentation for {{ cookiecutter.__folder_name }}!
{{ cookiecutter.description }}

This scaffold provides a ready-to-use environment for creating comprehensive documentation for Plone projects, based on [Plone Sphinx Theme](https://github.com/plone/plone-sphinx-theme).

Built with [Markedly Structured Text (MyST)](https://myst-parser.readthedocs.io/en/latest/), this environment supports rich formatting, directives, and extensions tailored for technical documentation.

It is structured following the [Diátaxis](https://diataxis.fr/) documentation framework.

```{toctree}
:caption: How to guides
:maxdepth: 2
:hidden: true

how-to-guides/index
```

```{toctree}
:caption: Reference
:maxdepth: 2
:hidden: true

reference/index
```

```{toctree}
:caption: Tutorials
:maxdepth: 2
:hidden: true

tutorials/index
```

```{toctree}
:caption: Concepts
:maxdepth: 2
:hidden: true

concepts/index
```

```{toctree}
:caption: Appendices
:maxdepth: 2
:hidden: true

glossary
genindex
```
