import json
from datetime import date
from pathlib import Path

from git import Repo

cwd = Path().cwd()
templates = cwd / "templates"
reports = cwd / ".reports"

repo = Repo(cwd)
last_commit = repo.head.commit

report_filename = f"{date.today()}-{last_commit.hexsha[:7]}-report.csv"

folders = ["backend_addon", "frontend_addon"]
ignore = ["__prompts__", "_copy_without_render", "_extensions"]
data = []


def _load_template_questions(base_path: Path) -> dict:
    """Load template questions, supporting v1 and v2 formats.

    For v2 (``cookieplone.json``) the schema's ``properties`` dict is
    flattened to a ``{key: default}`` mapping so the report keeps the
    same shape regardless of the template's format.
    """
    v2 = base_path / "cookieplone.json"
    if v2.is_file():
        raw = json.loads(v2.read_text())
        properties = raw.get("schema", {}).get("properties", {})
        return {key: prop.get("default", "") for key, prop in properties.items()}
    v1 = base_path / "cookiecutter.json"
    if v1.is_file():
        return json.loads(v1.read_text())
    return {}


for folder in folders:
    questions = _load_template_questions(templates / folder)
    items = [
        (folder, key, value) for key, value in questions.items() if key not in ignore
    ]
    data.extend(items)

report_path = reports / report_filename
with open(report_path, "w") as fout:
    fout.write("template\tkey\tvalue\n")
    for addon, key, value in data:
        fout.write(f'"{addon}"\t"{key}"\t"{value}"\n')

print(f"Report available at {report_path}")
