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

## Add features using plonecli/bobtemplates.plone

This package provides plonecli/bobtemplates.plone compatible entrypoints to add all kind of subtemplates provided by them.

To use them, you need to use bobtemplates.plone version > X.X.X and run your command as follows:

```shell
plonecli add -b .mrbob.ini content_type
```

This way we are passing the `.mrbob.ini` configuration file to plonecli to set some configuration variables needed to properly run the subtemplates.


## Contribute

- [Issue Tracker](https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.python_package_name }}/issues)
- [Source Code](https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.python_package_name }}/)

## License

The project is licensed under GPLv2.

## Credits and Acknowledgements 🙏

Crafted with care by **{{ cookiecutter.__generator_signature }}**. A special thanks to all contributors and supporters!
