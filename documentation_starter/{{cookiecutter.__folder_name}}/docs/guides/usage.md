---
myst:
  html_meta:
    "description": "How to use {{ cookiecutter.title }}"
    "property=og:description": "Learn how to use {{ cookiecutter.title }}."
    "property=og:title": "Usage - {{ cookiecutter.title }}"
    "keywords": "plone, {{ cookiecutter.title }}, {{ cookiecutter.__folder_name }}, usage, documentation"
---

# Usage

This guide explains how to use **{{ cookiecutter.title }}** in your Plone project.

Below, you’ll find basic steps and examples to get the most out of this documentation environment.

## Basic Usage

Once set up (see [Getting Started](getting-started.md)), you can start using your project. Here are example steps to get you started.

1. **Edit Markdown Files**:
   - Update `index.md` and add content to files in `guides/` or `reference/`.
   - Use MyST Markdown for rich formatting (see [Features](../reference/features.md)).

2. **Build and serve the Docs**:
   ```bash
   cd {{ cookiecutter.__folder_name }}
   make livehtml
   ```
3. **Watch the documentation live while you edit it.**

   - Open your browser at the url displayed in the console  
   - Default local url is: http://127.0.0.1:8050/
   - Edit the documentation source and save.
   - Content is rebuild and updates in the browser live.
