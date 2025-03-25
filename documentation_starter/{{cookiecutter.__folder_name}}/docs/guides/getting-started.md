---
myst:
  html_meta:
    "description": "Get started with {{ cookiecutter.title }}"
    "property=og:description": "Set up {{ cookiecutter.title }} in {{ cookiecutter.__folder_name }} for your Plone project."
    "property=og:title": "Getting Started - {{ cookiecutter.title }}"
    "keywords": "plone, {{ cookiecutter.title }}, setup, installation"
---
# Getting Started

This guide helps you set up **{{ cookiecutter.title }}**, a Plone project documented here. 

{{ cookiecutter.description }}.

Follow these steps to install and start using it in your Plone environment.

## Prerequisites

Here are some example prerequisites for using {{ cookiecutter.title }}:
- **Python 3.7+**: Required for Plone and its dependencies.
- **pip**: For installing Python packages.
- **[Plone](https://plone.org/download)**: A running Plone instance or the ability to create one.

## Installation

These are example steps to install {{ cookiecutter.title }} — adjust them for your project:

1. **Add the add-on to your Plone Environment**:

   If **{{ cookiecutter.title }}** is a Plone add-on with the package name ``{{ cookiecutter.__folder_name }}``, include it in your Plone buildout or package setup:
   ```bash
   echo "{{ cookiecutter.__folder_name }}" >> requirements.txt
   pip install -r requirements.txt
   ```
