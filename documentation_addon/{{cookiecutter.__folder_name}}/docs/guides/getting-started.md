---
myst:
  html_meta:
    "description": "Get started with {{ cookiecutter.__folder_name }}"
    "property=og:description": "Set up {{ cookiecutter.__folder_name }} for your Plone project."
    "property=og:title": "Getting Started - {{ cookiecutter.title }}"
    "keywords": "plone, {{ cookiecutter.__folder_name }}, setup, installation"
---
# Getting Started

This guide helps you set up **{{ cookiecutter.__folder_name }}**, a Plone project documented here. {{ cookiecutter.description }} Follow these steps to install and start using it in your Plone environment.

## Prerequisites

Here are some example prerequisites for using {{ cookiecutter.__folder_name }}:
- **Python 3.7+**: Required for Plone and its dependencies.
- **pip**: For installing Python packages.
- **[Plone](https://plone.org/download)**: A running Plone instance or the ability to create one.

## Installation

These are example steps to install {{ cookiecutter.__folder_name }} —adjust them for your project:

1. **Add to Your Plone Environment**:
   If {{ cookiecutter.__folder_name }} is a Plone add-on, include it in your Plone buildout or package setup:
   ```bash
   echo "{{ cookiecutter.__folder_name }}" >> requirements.txt
   pip install -r requirements.txt
   ```
