import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

from binaryornot.check import is_binary
from git import Repo

PATTERN = "{{ ?(cookiecutter)[.]([a-zA-Z0-9-_]*)"
RE_OBJ = re.compile(PATTERN)

cwd = Path().cwd()
reports = cwd / ".reports"

repo = Repo(cwd)
last_commit = repo.head.commit

report_filename = f"{date.today()}-{last_commit.hexsha[:7]}-usage.json"

folders = ["backend_addon", "frontend_addon"]
ignore = [
    "__prompts__",
]


def as_sorted_list(value: set) -> list:
    """Convert a set to a list and sort it."""
    value = list(value)
    return sorted(value)


def find_and_add_keys(used_keys: set, data: str) -> set:
    matches = RE_OBJ.findall(data) or []
    for match in matches:
        used_keys.add(match[1])
    return used_keys


def valid_key(key: str) -> bool:
    """Check if we will check for this key."""
    return all(
        [
            key not in ignore,
            key.startswith("__") or not key.startswith("_"),
        ]
    )


keys = defaultdict(dict)
for folder in folders:
    base_path = cwd / folder
    file_ = base_path / "cookiecutter.json"
    template_folder = base_path / "{{ cookiecutter.__folder_name }}"
    raw_context = file_.read_text()
    used_keys = find_and_add_keys({"__folder_name"}, raw_context)
    questions = json.loads(raw_context)
    items = {key for key in questions.keys() if valid_key(key)}
    all_files = template_folder.glob("**/*")
    # Already add __folder_name
    for filepath in all_files:
        data = filepath.name
        is_file = filepath.is_file()
        if is_file and is_binary(f"{filepath}"):
            continue
        if is_file:
            data = f"{data} {filepath.read_text()}"
        used_keys = find_and_add_keys(used_keys, data)
    keys[folder]["all"] = as_sorted_list(items)
    keys[folder]["used"] = as_sorted_list(used_keys & items)
    keys[folder]["not_used"] = as_sorted_list(items.difference(used_keys))
    keys[folder]["missing"] = as_sorted_list(used_keys.difference(items))


report_path = reports / report_filename
with open(report_path, "w") as fout:
    json.dump(keys, fout, indent=2)

print(f"Report available at {report_path}")
