---
myst:
  html_meta:
    "description": "Theme-specific elements of Plone Sphinx Theme"
    "property=og:description": "Theme-specific elements of Plone Sphinx Theme"
    "property=og:title": "Theme-specific elements of Plone Sphinx Theme"
    "keywords": "Plone, Sphinx, Theme, plone-sphinx-theme, elements"
---

# Theme-specific elements

This page contains a number of reference elements to see how they look in Plone Sphinx Theme, the default theme used in **{{ cookiecutter.title }}**.
Each element is followed by the MyST code used to generate the element.

````{seealso}
Plone Sphinx Theme inherits theme-specific elements from its parent themes, but are not displayed here to avoid duplication and maintenance.
You can view them on display in their documentation.

```{note}
If a parent theme's elements do not display correctly in Plone Sphinx Theme, please [open an issue](https://github.com/plone/plone-sphinx-theme/issues/new).
```

-   [Sphinx Book Theme](https://sphinx-book-theme.readthedocs.io/en/latest/reference/special-theme-elements.html)
-   [PyData Library Styles](https://pydata-sphinx-theme.readthedocs.io/en/latest/examples/pydata.html)
-   [PyData Execution Libraries](https://pydata-sphinx-theme.readthedocs.io/en/latest/examples/execution.html)
````


## Full-width container

````{container} full-width
This is some markdown that should be shown at full width.
Here's the Plone logo:

```{image} /_static/logo.svg
:width: 100%
:class: logo__image only-dark
```

```{image} /_static/logo.svg
:width: 100%
:class: logo__image only-light
```
````

`````markdown
````{container} full-width
This is some markdown that should be shown at full width.
Here's the Plone logo:

```{image} /_static/logo.svg
:width: 100%
:class: logo__image only-dark
```

```{image} /_static/logo.svg
:width: 100%
:class: logo__image only-light
```
````
`````

## Margins

Margin content can include all kinds of things, such as admonitions and images.

Note that content in margins may extend beyond the current section, making them not always useful.

Consider using sidebars instead.

`````{margin} **Notes in margins**
````{note}
Wow, a note with an image in a margin!
```{image} /_static/logo.svg
:class: logo__image only-dark
```

```{image} /_static/logo.svg
:class: logo__image only-light
```
````
`````

``````markdown
`````{margin} **Notes in margins**
````{note}
Wow, a note with an image in a margin!
```{image} /_static/logo.svg
:class: logo__image only-dark
```

```{image} /_static/logo.svg
:class: logo__image only-light
```
````
`````
``````


## `versionremoved`

```{versionremoved} v0.1.1
Here's a version removed message.

We also support *italic*, **bold**, `code`, [links](https://www.sphinx-doc.org/), and more.
```
