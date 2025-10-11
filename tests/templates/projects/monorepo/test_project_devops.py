"""Test Generator: /devops."""

import pytest
import yaml

ANSIBLE_FILES = [
    "devops/ansible/.ansible-lint",
    "devops/ansible/.editorconfig",
    "devops/ansible/.env_dist",
    "devops/ansible/.gitignore",
    "devops/ansible/.vault_pass",
    "devops/ansible/ansible.cfg",
    "devops/ansible/etc/.ssh/.gitkeep",
    "devops/ansible/etc/.ssh/ansible-ssh-config",
    "devops/ansible/etc/base/apt_proxy.j2",
    "devops/ansible/etc/base/environment.j2",
    "devops/ansible/etc/docker/systemd/http-proxy.conf.j2",
    "devops/ansible/etc/keys/.gitkeep",
    "devops/ansible/etc/ssh/default_ssh_config.j2",
    "devops/ansible/etc/stacks/cronjob.yml",
    "devops/ansible/etc/stacks/traefik.yml",
    "devops/ansible/inventory/group_vars/all/base.yml",
    "devops/ansible/inventory/group_vars/all/disks.yml",
    "devops/ansible/inventory/group_vars/all/docker.yml",
    "devops/ansible/inventory/group_vars/all/packages.yml",
    "devops/ansible/inventory/group_vars/all/proxy.yml",
    "devops/ansible/inventory/group_vars/all/sshd.yml",
    "devops/ansible/inventory/group_vars/all/stacks.yml",
    "devops/ansible/inventory/group_vars/all/swap.yml",
    "devops/ansible/inventory/group_vars/all/swarm.yml",
    "devops/ansible/inventory/group_vars/all/ufw.yml",
    "devops/ansible/inventory/group_vars/all/users.yml",
    "devops/ansible/inventory/group_vars/all/vault.yml",
    "devops/ansible/inventory/hosts.yml",
    "devops/ansible/Makefile",
    "devops/ansible/playbooks/_connect.yml",
    "devops/ansible/playbooks/deploy.yml",
    "devops/ansible/playbooks/setup.yml",
    "devops/ansible/playbooks/stacks.yml",
    "devops/ansible/pyproject.toml",
    "devops/ansible/README.md",
    "devops/ansible/requirements.yml",
    "devops/ansible/tasks/base/task_base_packages.yml",
    "devops/ansible/tasks/base/task_hostname.yml",
    "devops/ansible/tasks/base/task_mount_points.yml",
    "devops/ansible/tasks/base/task_proxy.yml",
    "devops/ansible/tasks/base/task_ssh.yml",
    "devops/ansible/tasks/base/task_ufw.yml",
    "devops/ansible/tasks/base/task_user.yml",
    "devops/ansible/tasks/docker/task_setup.yml",
    "devops/ansible/tasks/docker/task_stack.yml",
    "devops/ansible/tasks/docker/task_swarm.yml",
    "devops/ansible/tasks/handlers/common.yml",
    "devops/ansible/tasks/stacks/task_deploy.yml",
]

GHA_ACTIONS_CI = [
    ".github/workflows/backend.yml",
    ".github/workflows/frontend.yml",
]

GHA_ACTIONS_DEPLOY = [
    ".github/workflows/manual_deploy.yml",
    "devops/.env_gha",
    "devops/README-GHA.md",
]

STACKS = [
    "devops/stacks/plone.org.br.yml",
    "docker-compose.yml",
]

DEVOPS_FILES = ANSIBLE_FILES + GHA_ACTIONS_CI + GHA_ACTIONS_DEPLOY + STACKS


@pytest.mark.parametrize("filepath", DEVOPS_FILES)
def test_project_devops_files(cutter_result, filepath: str):
    """Test created files."""
    folder = cutter_result.project_path
    path = folder / filepath
    assert path.is_file()


@pytest.mark.parametrize(
    "filepath",
    [filepath for filepath in DEVOPS_FILES if filepath.endswith(".yml")],
)
def test_valid_yaml_files(cutter_result, filepath: str):
    """Test generated yaml files are valid."""
    folder = cutter_result.project_path
    path = folder / filepath
    with open(path) as fh:
        content = yaml.full_load(fh)
    assert content


@pytest.mark.parametrize("filepath", ANSIBLE_FILES)
def test_project_devops_no_ansible(cutter_result_devops_no_ansible, filepath: str):
    """Test Ansible files are not present."""
    folder = cutter_result_devops_no_ansible.project_path
    path = folder / filepath
    assert path.exists() is False


@pytest.mark.parametrize("filepath", GHA_ACTIONS_DEPLOY)
def test_project_devops_no_gha_deploy(
    cutter_result_devops_no_gha_deploy, filepath: str
):
    """Test GHA deploy files are not present."""
    folder = cutter_result_devops_no_gha_deploy.project_path
    path = folder / filepath
    assert path.exists() is False


def test_ansible_inventory_stacks_replacement(cutter_result):
    """Test GHA deploy files are not present."""
    folder = cutter_result.project_path
    path = folder / "devops/ansible/inventory/group_vars/all/stacks.yml"
    assert "{{ cookiecutter.hostname }}" not in path.read_text()
