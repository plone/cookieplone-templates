# Plone Sphinx Theme change log

<!-- Do *NOT* add new change log entries to this file.
     Instead create a file in the news directory.
     For helpful instructions, see:
     https://6.docs.plone.org/contributing/index.html#change-log-entry
-->

<!-- towncrier release notes start -->

## 1.0.4 (2025-01-19)

### New features

- Shift admonition title icon to the top of the paragraph for multi-line admonition titles. @stevepiercy [Issue #49](https://github.com/plone/plone-sphinx-theme/issues/49)

### Documentation

- Add documentation for development server. @stevepiercy [Issue #49](https://github.com/plone/plone-sphinx-theme/issues/49)

## 1.0.3 (2024-12-20)

### New features

- Add support for `versionremoved` directive. @stevepiercy [Issue #48](https://github.com/plone/plone-sphinx-theme/issues/48)

### Documentation

- Fix `suppress_warnings` syntax for `SPHINXOPTS`. @stevepiercy [Issue #47](https://github.com/plone/plone-sphinx-theme/issues/47)

## 1.0.2 (2024-12-05)

### Internal changes

- Build the pull request preview for CSS and JavaScript changes. @stevepiercy [Issue #46](https://github.com/plone/plone-sphinx-theme/issues/46)

### Documentation

- Bump the minimum level of page contents sidebar from 1 to 2. @stevepiercy [Issue #45](https://github.com/plone/plone-sphinx-theme/issues/45)

### New features

- Override styles for `menuselection` and `guilabel` from PyData Sphinx Theme. @stevepiercy [Issue #46](https://github.com/plone/plone-sphinx-theme/issues/46)

## 1.0.1 (2024-11-22)

### Bug fixes

- Fix line item spacing to allow for paragraphs within a list item. @stevepiercy [Issue #44](https://github.com/plone/plone-sphinx-theme/issues/44)

## 1.0.0 (2024-11-19)

### New features

- Add support for sphinxcontrib-youtube. @stevepiercy [Issue #41](https://github.com/plone/plone-sphinx-theme/issues/41)
- Pin dependencies to resolve primary sidebar display toggle. This is the first stable release of Plone Sphinx Theme. @stevepiercy [Issue #43](https://github.com/plone/plone-sphinx-theme/issues/43)

## 0.3.1 (2024-11-18)

### New features

- Add VSCode editor settings. @stevepiercy [Issue #39](https://github.com/plone/plone-sphinx-theme/issues/39)

### Documentation

- Add documentation for how to override build configuration options. @stevepiercy [Issue #40](https://github.com/plone/plone-sphinx-theme/issues/40)

## 0.3.0 (2024-11-14)

### New features

- Restore support for Mermaid. @stevepiercy [Issue #38](https://github.com/plone/plone-sphinx-theme/issues/38)

## 0.2.1 (2024-11-11)

### New features

- Move the icon links from the primary sidebar to the page content footer. @stevepiercy [Issue #37](https://github.com/plone/plone-sphinx-theme/issues/37)

## 0.2.0 (2024-11-11)

### Internal changes

- Adapt Makefile to use uv's preferred virtual environment location of `/.venv/`. @stevepiercy [Issue #34](https://github.com/plone/plone-sphinx-theme/issues/34)
- Update project requirements. @stevepiercy [Issue #35](https://github.com/plone/plone-sphinx-theme/issues/35)

### New features

- Update styles and configuration to latest. @stevepiercy
  - Update styles from upstream Sphinx Book Theme.
  - In todo directive, replace pencil icon with a clipboard list icon.
  - For video directive, limit the width to 100% of the page content container.
  - Add YouTube social icon to configuration.
  - Rename Twitter social icon to X (formerly Twitter). [Issue #36](https://github.com/plone/plone-sphinx-theme/issues/36)

## 0.1.0 (2024-10-08)

### New features

#### Vale improvements

- Upgrade and pin Vale to v3. @stevepiercy
  - Follow some of Vale's suggestions and fix errors and warnings. @stevepiercy
  - Add GitHub Workflow to build docs and run checks on links, spelling, grammar, and style. @stevepiercy [Issue #31](https://github.com/plone/plone-sphinx-theme/issues/31)

#### Makefile improvements

- Purged unused and broken Make build targets. @stevepiercy
- Categorized Make targets with comments. @stevepiercy
- Add test requirement `sphinx.ext.doctest` so that `make doctest` will work in some Plone projects. @stevepiercy
- Add targets to correctly install, clean, and initialize the project. @stevepiercy
- Updated documentation with correct make commands. @stevepiercy
- Move release command from `README.md` to `contribute.md`. @stevepiercy [Issue #33](https://github.com/plone/plone-sphinx-theme/issues/33)

#### Miscellaneous changes

- Switch to `uv` from `pip`. @stevepiercy
- Fixed which changed files will build docs on RTD. @stevepiercy
- Use a replacement for supported Python versions. @stevepiercy


### Bug fixes

- Add Python script to enable `make html_meta`. @stevepiercy [Issue #32](https://github.com/plone/plone-sphinx-theme/issues/32)

## 0.0.15 (2024-09-19)

### New features

- Override sphinxcontrib-httpexample tabs background color for sure this time. @stevepiercy [Issue #29](https://github.com/plone/plone-sphinx-theme/issues/29)

## 0.0.14 (2024-09-19)

### New features

- Override sphinxcontrib-httpexample tabs background color. @stevepiercy [Issue #28](https://github.com/plone/plone-sphinx-theme/issues/28)

## 0.0.13 (2024-09-19)

### Bug fixes

- Remove support for Mermaid. See https://github.com/mgaitan/sphinxcontrib-mermaid/issues/137. @stevepiercy [Issue #27](https://github.com/plone/plone-sphinx-theme/issues/27)

## 0.0.12 (2024-09-19)

### Bug fixes

- Update parent theme, and compile for dist. @stevepiercy [Issue #26](https://github.com/plone/plone-sphinx-theme/issues/26)

## 0.0.11 (2024-09-19)

### Bug fixes

- Remove style that causes code blocks in sphinxcontrib.httpexample to blow out off-screen. @stevepiercy [Issue #25](https://github.com/plone/plone-sphinx-theme/issues/25)

## 0.0.10 (2024-06-17)

### Internal changes

- Unpin mermaid and specify which version of the JavaScript library to load. @stevepiercy [Issue #23](https://github.com/plone/plone-sphinx-theme/issues/23)

## 0.0.9 (2024-06-17)

- Clean up release. @stevepiercy

## 0.0.8 (2024-06-17)

### New features

- Add support for Mermaid Sphinx extension. @stevepiercy [Issue #22](https://github.com/plone/plone-sphinx-theme/issues/22)

## 0.0.5 (2024-05-21)

### Internal changes

- Change build-system to use setuptools. Fix manifest. @stevepiercy [Issue #21](https://github.com/plone/plone-sphinx-theme/issues/21)

## 0.0.4 (2024-05-20)

### Internal changes

- Steal towncrier config from Volto. Clean up `CHANGES.md`. @stevepiercy [Issue #18](https://github.com/plone/plone-sphinx-theme/issues/18)
- Fix towncrier template path. @stevepiercy [Issue #19](https://github.com/plone/plone-sphinx-theme/issues/19)

## 0.0.3 (2024-05-19)

### Internal changes:

- Add .gitkeep to news directory to preserve it upon releases. @stevepiercy ([Issue #garden](https://github.com/plone/plone-sphinx-theme/garden))
- Fix CHANGES.md content for automatic updates upon releases. @stevepiercy ([Issue #garden1](https://github.com/plone/plone-sphinx-theme/garden1))
- Add GitHub action to deploy documentation to Read the Docs. @stevepiercy ([Issue #garden2](https://github.com/plone/plone-sphinx-theme/garden2))
- Add pull request preview on Read the Docs. @stevepiercy ([Issue #garden3](https://github.com/plone/plone-sphinx-theme/garden3))
- Clean up conf.py. @stevepiercy ([Issue #garden4](https://github.com/plone/plone-sphinx-theme/garden4))

### Documentation:

- Fix glossary syntax. @stevepiercy ([Issue #glossary](https://github.com/plone/plone-sphinx-theme/glossary))


## 0.0.2 (2024-05-06)

### New features:

- Add towncrier. @stevepiercy ([Issue #1](https://github.com/plone/plone-sphinx-theme/1))


## 0.0.1 (2024-05-06)

- Initial release.
