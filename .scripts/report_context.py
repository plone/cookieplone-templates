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

for folder in folders:
    file_ = templates / folder / "cookiecutter.json"
    questions = json.loads(file_.read_text())
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
