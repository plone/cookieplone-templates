import csv
import json
import os
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

from binaryornot.check import is_binary
from git import Repo

PATTERNS = (
    re.compile(r" ?(cookiecutter)[.](?P<key>[a-zA-Z0-9-_]*) "),
    re.compile(r"(context\.get\(\")(?P<key>[a-zA-Z0-9-_]*)\""),
)

IGNORED_KEYS = (
    "_extensions",
    "_copy_without_render",
    "__prompts__",
    "__cookieplone_subtemplates",
)

SYMBOLS = {
    "not_found": {"title": "Not present in cookiecutter.json", "icon": "-"},
    "used": {"title": "Used by the template", "icon": "✅"},
    "not_used": {"title": "Not used in template", "icon": "❗"},
    "missing": {
        "title": "Used by the template, not present in cookiecutter.json",
        "icon": "🚫",
    },
}


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
    for pattern in PATTERNS:
        matches = {match.groupdict()["key"] for match in pattern.finditer(content)}
        matches = {key for key in matches if is_valid_key(key)}
        existing_keys = existing_keys.union(matches)
    return existing_keys


def is_valid_key(key: str) -> bool:
    """Should we check for this key."""
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


def _md_table_header_rows(columns: list[str], align: str = "default") -> list[str]:
    rows: list[str] = [" | ".join(columns).strip()]
    # Divider
    divider = []
    for idx, fieldname in enumerate(columns):
        item = "-" * len(fieldname)
        if idx and align == "auto":
            item = f":{item[1:-1]}:"
        divider.append(item)
    rows.append(" | ".join(divider).strip())
    return [f"| {row} |\n" for row in rows]


def _md_report_table_body(data_rows: list[dict]) -> list[str]:
    rows: list[str] = []
    for key_report in data_rows:
        row = " | ".join(list(key_report.values())).strip()
        rows.append(f"| {row} |\n")
    return rows


def _md_report_table(report_data: dict) -> list[str]:
    rows: list[str] = ["# Key usage in templates\n\n"]
    columns = report_data["keys"]["header"]
    data_rows = report_data["keys"]["rows"]
    rows.extend(_md_table_header_rows(columns, align="auto"))
    rows.extend(_md_report_table_body(data_rows))
    return rows


def _md_legend() -> list[str]:
    rows: list[str] = ["\n", "## Legend\n\n"]
    columns = ["Icon", "Description"]
    rows.extend(_md_table_header_rows(columns))
    for item in SYMBOLS.values():
        title, icon = item.values()
        rows.append(f"| {icon} | {title} |\n")
    return rows


def _write_md_report(report_data: dict, report_path: Path) -> Path:
    with open(report_path, "w") as fout:
        for row in _md_report_table(report_data):
            fout.write(row)
        for row in _md_legend():
            fout.write(row)
    return report_path


REPORT_FORMATS = {
    "json": _write_json_report,
    "csv": _write_csv_report,
    "md": _write_md_report,
}


def _analyze_template_folder(folder: Path, used_keys: set[str]) -> set[str]:
    all_files = folder.glob("**/*")
    for filepath in all_files:
        data = filepath.name
        is_file = filepath.is_file()
        if is_file and is_binary(f"{filepath}"):
            continue
        if is_file:
            data = f"{data} {filepath.read_text()}"
        used_keys = extract_template_keys(used_keys, data)
    return used_keys


def analyze_template_usage(templates: list[tuple[str, Path]]) -> tuple[set, dict]:
    all_keys: set[str] = set()
    template_keys: dict[str, dict[str, list[str]]] = defaultdict(dict)
    for name, base_path in templates:
        template_config = base_path / "cookiecutter.json"
        raw_context = template_config.read_text()
        questions = json.loads(raw_context)
        # Already add __folder_name, used in folder name
        used_keys = extract_template_keys({"__folder_name"}, raw_context)
        items = {key for key in questions if is_valid_key(key)}
        template_folders = (
            base_path / "hooks",
            base_path / "{{ cookiecutter.__folder_name }}",
        )
        for template_folder in template_folders:
            used_keys = _analyze_template_folder(template_folder, used_keys)

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
            status = SYMBOLS["not_found"]["icon"]
            keys = template_keys[template]
            if key in keys["used"]:
                status = SYMBOLS["used"]["icon"]
            elif key in keys["not_used"]:
                status = SYMBOLS["not_used"]["icon"]
            elif key in keys["missing"]:
                status = SYMBOLS["missing"]["icon"]
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
    formats = tuple(REPORT_FORMATS.keys())
    if env_formats := os.environ.get("REPORT_FORMATS", ""):
        formats = tuple(fmt for fmt in env_formats.split(",") if fmt in REPORT_FORMATS)

    run_report_generation(repo_root, formats)
