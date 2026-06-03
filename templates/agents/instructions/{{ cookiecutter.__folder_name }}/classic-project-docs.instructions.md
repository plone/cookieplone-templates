---
name: "Instructions: Plone project with backend documentation"
description: "Standards and guidelines for documentation files for Plone projects with a backend component"
applyTo: "README.md,docs/docs/**/*.md,docs/README.md,backend/README.md"
---

# Plone project documentation standards

This document outlines the standards and guidelines for documentation files in a repository for a Plone project containing a backend component that will be deployed using a container.

## 0. General guidelines

Always read the general rules for Plone documentation in ./general/docs.md

## 1. All files

- ALWAYS use emojis in section titles for a friendly tone.
- ALWAYS recommend using `make` commands for installation and starting the project:
    - ALWAYS recommend using `make install` to install the project and its components, as this handles all dependencies and setup.
    - ALWAYS recommend using `make start` to start processes, as this ensures proper configuration.
- NEVER recomend using `pnpm install` or `pnpm start` directly.
- NEVER recomend using `pip install`, `uv add`  or `uv pip` directly.
- NEVER edit the paragraph refering to `cookieplone`. Usually starting with **Generated using**.

## 2. README.md at the top level of the repository

- Must provide a clear overview of the backend part of the addon
- Will be viewed on GitHub
- Must provide installation for developers willing to contribute to this add-on.
- Must describe the features.
    - Example:
        - ✅: `- Register a behavior providing additiional fields representing contact information` .
        - ❌: `- Behavior` .
    - Review the code if necessary to explain it.

## 3. backend/README.md

- Must provide a clear overview of the addon
- Will be viewed only on GitHub
- Must link to the top-level README of the repository for developers willing to contribute to this add-on.
- Must describe the features.
    - Example:
        - ✅: `- Register a behavior providing additiional fields representing contact information` .
        - ❌: `- Behavior` .
    - Review the code if necessary to explain it.

## 4. docs/README.md
- Must provide detailed documentation for developers **documenting** the project
