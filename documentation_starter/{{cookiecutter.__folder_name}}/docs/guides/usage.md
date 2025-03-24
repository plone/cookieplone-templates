---
myst:
  html_meta:
    "description": "How to use {{ cookiecutter.__folder_name }}"
    "property=og:description": "Learn how to use {{ cookiecutter.__folder_name }}."
    "property=og:title": "Usage - {{ cookiecutter.title }}"
    "keywords": "plone, {{ cookiecutter.__folder_name }}, usage, documentation"
---

# Usage

This guide explains how to use **{{ cookiecutter.__folder_name }}** in your Plone project. {{ cookiecutter.description }} Below, you’ll find basic steps and examples to get the most out of this documentation environment.

## Basic Usage

Once set up (see [Getting Started](getting-started.md)), you can start using your project. Here are example steps to get you started.

1. **Edit Markdown Files**:
   - Update `index.md` and add content to files in `guides/` or `reference/`.
   - Use MyST Markdown for rich formatting (see [Features](../reference/features.md)).

2. **Build the Docs**:
   ```bash
   cd project_name
   make html
   ```
