"""Test Generator: .devcontainer and docker-compose-devcontainers.yml"""

import pytest
import yaml

from .conftest import VOLTO_VERSION


@pytest.mark.parametrize(
    "file_path,path,expected",
    [
        ["backend/devcontainer.json", "name", "Plone Brasil: Backend"],
        ["backend/devcontainer.json", "service", "backend"],
        ["backend/devcontainer.json", "remoteUser", "plone"],
        [
            "backend/devcontainer.json",
            "dockerComposeFile/0",
            "../../docker-compose-devcontainers.yml",
        ],
        ["frontend/devcontainer.json", "name", "Plone Brasil: Frontend"],
        ["frontend/devcontainer.json", "service", "frontend"],
        ["frontend/devcontainer.json", "remoteUser", "node"],
        ["frontend/devcontainer.json", "runServices/0", "backend"],
        ["frontend/devcontainer.json", "runServices/1", "frontend"],
    ],
)
def test_devcontainer_settings(
    cutter_result, load_json, traverse, file_path: str, path: str, expected: str
):
    data = load_json(cutter_result.project_path / ".devcontainer" / file_path)
    assert traverse(data, path) == expected


@pytest.mark.parametrize(
    "file_path,expected",
    [
        ["backend/Dockerfile", "FROM plone-org-br-devcontainer-backend-base"],
        ["frontend/Dockerfile", "FROM plone-org-br-devcontainer-frontend-base"],
    ],
)
def test_devcontainer_dockerfile_base_image(
    cutter_result, file_path: str, expected: str
):
    content = (cutter_result.project_path / ".devcontainer" / file_path).read_text()
    assert expected in content.splitlines()


def test_devcontainer_compose(cutter_result):
    path = cutter_result.project_path / "docker-compose-devcontainers.yml"
    data = yaml.safe_load(path.read_text())
    assert data["name"] == "plone-org-br-devcontainer"
    services = data["services"]
    assert set(services) == {
        "backend-base",
        "backend-dev",
        "backend",
        "frontend-base",
        "frontend-dev",
        "frontend",
    }
    # Dev images extend the project images
    contexts = services["backend-dev"]["build"]["additional_contexts"]
    assert contexts == {
        "plone-org-br-devcontainer-backend-base": "service:backend-base"
    }
    assert services["frontend-base"]["build"]["args"] == [
        f"VOLTO_VERSION=${{VOLTO_VERSION:-{VOLTO_VERSION}}}"
    ]
    # Containers used by the Dev Containers tooling must not have a build section
    assert "build" not in services["backend"]
    assert "build" not in services["frontend"]
    assert services["frontend"]["network_mode"] == "service:backend"
    assert (
        "frontend-addon-node-modules:"
        "/workspace/frontend/packages/volto-ploneorgbr/node_modules"
        in services["frontend"]["volumes"]
    )


def test_devcontainer_compose_scoped_frontend_package(
    cutter_result_scoped_frontend_package,
):
    path = (
        cutter_result_scoped_frontend_package.project_path
        / "docker-compose-devcontainers.yml"
    )
    data = yaml.safe_load(path.read_text())
    assert (
        "frontend-addon-node-modules:"
        "/workspace/frontend/packages/volto-ploneorgbr/node_modules"
        in data["services"]["frontend"]["volumes"]
    )
