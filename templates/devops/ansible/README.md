# Cookieplone Ansible Playbooks

[![Cookieplone Templates: CI](https://github.com/plone/cookieplone-templates/actions/workflows/main.yml/badge.svg)](https://github.com/plone/cookieplone-templates/blob/main/.github/workflows/main.yml)
[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
[![License](https://img.shields.io/github/license/plone/cookieplone-templates)](../../../LICENSE)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Powered by [Cookieplone](https://github.com/plone/cookieplone) and [Cookiecutter](https://github.com/cookiecutter/cookiecutter), [Cookieplone devops Ansible](https://github.com/plone/cookieplone-templates/tree/main/templates/devops/ansible) is intended to be used by Plone developers to create Ansible playbooks to setup a Docker Swarm cluster.


## Prerequisites

-   [uv](https://docs.astral.sh/uv/) is the recommended tool for managing Python versions and project dependencies.


### uv

To install uv, use the following command, or visit the [uv installation page](https://docs.astral.sh/uv/getting-started/installation/) for alternative methods.

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```


## Generate the playbooks 🎉

```shell
uvx cookieplone devops_ansible
```

## License 📜

This project is licensed under the [MIT License](/LICENSE).


## Let's get building! 🚀

Happy coding!
