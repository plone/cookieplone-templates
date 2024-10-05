# {{ cookiecutter.python_package_name }}

{{ cookiecutter.description }}

## Features

TODO: List our awesome features

## Installation

Install {{ cookiecutter.python_package_name }} with `pip`:

```shell
pip install {{ cookiecutter.python_package_name }}
```
And to create the Plone site:

```shell
make create_site
```

## Add features using `plonecli` or `bobtemplates.plone`

This package provides markers as strings (`<!-- extra stuff goes here -->`) that are compatible with [`plonecli`](https://github.com/plone/plonecli) and [`bobtemplates.plone`](https://github.com/plone/bobtemplates.plone).
These markers act as hooks to add all kinds of subtemplates, including behaviors, control panels, upgrade steps, or other subtemplates from `plonecli`.

To use them, you need to use `bobtemplates.plone` version X.X.X or later, and run the following command.

```shell
plonecli add -b .mrbob.ini content_type
```

The command passes the `.mrbob.ini` configuration file to `plonecli` to set some configuration variables which are needed to properly run the subtemplates.


For instance, you could add a behavior to your package running this command:

```shell
plonecli add -b .mrbob.ini behavior
```

Or a controlpanel running this other command:

```shell
plonecli add -b .mrbob.ini controlpanel
```

You can check the list of available subtemplates in the [bobtemplates.plone README file](https://github.com/plone/bobtemplates.plone/?tab=readme-ov-file#provided-subtemplates)



## Contribute

- [Issue Tracker](https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.python_package_name }}/issues)
- [Source Code](https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.python_package_name }}/)

## License

The project is licensed under GPLv2.

## Credits and Acknowledgements 🙏

Crafted with care by **{{ cookiecutter.__generator_signature }}**. A special thanks to all contributors and supporters!
