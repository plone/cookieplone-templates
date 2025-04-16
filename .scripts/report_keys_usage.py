import csv
import json
import os
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

from binaryornot.check import is_binary
from git import Repo

PATTERN = "{{ ?(cookiecutter)[.]([a-zA-Z0-9-_]*)"
RE_OBJ = re.compile(PATTERN)

IGNORED_KEYS = ("__prompts__",)


def load_template_definitions(repo_root: Path) -> list[tuple[str, Path]]:
    templates = []
    cookiecutter_config_file = repo_root / "cookiecutter.json"
    data = json.loads(cookiecutter_config_file.read_text())
    for name, template in data["templates"].items():
        path = (repo_root / template["path"]).resolve()
        templates.append((name, path))
    return templates


def sorted_list(value: set) -> list:
    """Convert a set to a list and sort it."""
    return sorted(value)


def extract_template_keys(existing_keys: set, content: str) -> set:
    matches = {match[1] for match in RE_OBJ.findall(content)}
    return existing_keys.union(matches)


def is_valid_key(key: str) -> bool:
    """Check if we will check for this key."""
    return all(
        [
            key not in IGNORED_KEYS,
            key.startswith("__") or not key.startswith("_"),
        ]
    )


def _write_json_report(report_data: dict, report_path: Path) -> Path:
    templates = report_data["templates"]
    with open(report_path, "w") as fout:
        json.dump(templates, fout, indent=2)

    return report_path


def _write_csv_report(report_data: dict, report_path: Path) -> Path:
    header = report_data["keys"]["header"]
    rows = report_data["keys"]["rows"]
    with open(report_path, "w") as fout:
        writer = csv.DictWriter(fout, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
    return report_path


def _write_md_report(report_data: dict, report_path: Path) -> Path:
    columns = report_data["keys"]["header"]
    rows = report_data["keys"]["rows"]
    with open(report_path, "w") as fout:
        row = " | ".join(columns).strip()
        fout.write(f"| {row} |\n")
        divider = []
        for idx, fieldname in enumerate(columns):
            item = "-" * len(fieldname)
            if idx:
                item = f":{item[1:-1]}:"
            divider.append(item)
        row = " | ".join(divider).strip()
        fout.write(f"| {row} |\n")
        for key_report in rows:
            row = " | ".join(list(key_report.values())).strip()
            fout.write(f"| {row} |\n")

    return report_path


REPORT_FORMATS = {
    "json": _write_json_report,
    "csv": _write_csv_report,
    "md": _write_md_report,
}


def analyze_template_usage(templates: list[tuple[str, Path]]) -> tuple[set, dict]:
    all_keys: set[str] = set()
    template_keys: dict[str, dict[str, list[str]]] = defaultdict(dict)
    for name, base_path in templates:
        file_ = base_path / "cookiecutter.json"
        template_folder = base_path / "{{ cookiecutter.__folder_name }}"
        raw_context = file_.read_text()
        used_keys = extract_template_keys({"__folder_name"}, raw_context)
        questions = json.loads(raw_context)
        items = {key for key in questions if is_valid_key(key)}
        all_files = template_folder.glob("**/*")
        # Already add __folder_name
        for filepath in all_files:
            data = filepath.name
            is_file = filepath.is_file()
            if is_file and is_binary(f"{filepath}"):
                continue
            if is_file:
                data = f"{data} {filepath.read_text()}"
            used_keys = extract_template_keys(used_keys, data)
        template_keys[name]["all"] = sorted_list(items)
        template_keys[name]["used"] = sorted_list(used_keys & items)
        template_keys[name]["not_used"] = sorted_list(items.difference(used_keys))
        template_keys[name]["missing"] = sorted_list(used_keys.difference(items))
        occurrences = items.union(used_keys)
        all_keys = all_keys.union(occurrences)
    return all_keys, template_keys


def generate_key_usage_matrix(
    all_keys: set, template_keys: dict, all_templates: list[str]
) -> list[dict]:
    keys_usage = []
    for key in sorted(all_keys):
        key_report = {"key": key}
        for template in all_templates:
            status = "🔍"
            keys = template_keys[template]
            if key in keys["used"]:
                status = "✅"
            elif key in keys["not_used"]:
                status = "❗"
            elif key in keys["missing"]:
                status = "🚫"
            key_report[template] = status
        keys_usage.append(key_report)
    return keys_usage


def generate_report_filename(repo_root: Path):
    repo = Repo(repo_root)
    last_commit = repo.head.commit
    if not (report_filename := os.environ.get("REPORT_FILENAME", "")):
        report_filename = f"{date.today()}-{last_commit.hexsha[:7]}-usage"
    return report_filename


def run_report_generation(repo_root: Path, formats: tuple[str, ...]):
    reports_dir = repo_root / ".reports"
    report_filename = generate_report_filename(repo_root)
    templates = load_template_definitions(repo_root)
    all_templates = [t[0] for t in templates]
    all_keys, template_keys = analyze_template_usage(templates)
    keys_usage = generate_key_usage_matrix(all_keys, template_keys, all_templates)
    report_data = {
        "templates": template_keys,
        "keys": {
            "header": ["key", *all_templates],
            "rows": keys_usage,
        },
    }
    for fmt in formats:
        func = REPORT_FORMATS.get(fmt)
        if func:
            report_path = reports_dir / f"{report_filename}.{fmt}"
            func(report_data, report_path)
            print(f"- Wrote {fmt} report @ {report_path}")


if __name__ == "__main__":
    repo_root = Path().cwd()
    env_formats = os.environ.get("REPORT_FORMATS", "")
    if env_formats:
        formats = (fmt for fmt in env_formats.split(",") if fmt in REPORT_FORMATS)
    else:
        formats = tuple(REPORT_FORMATS.keys())
    run_report_generation(repo_root, formats)
