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

VERSIONS_PATTERNS = (
    re.compile(r"versions[.](?P<key>[a-zA-Z0-9_]+)"),
    re.compile(r'versions\["(?P<key>[a-zA-Z0-9_]+)"\]'),
)

IGNORED_KEYS = (
    "_extensions",
    "_copy_without_render",
    "__prompts__",
    "__cookieplone_subtemplates",
    "__cookieplone_template",
)


def _read_template_config(base_path: Path) -> dict:
    """Read a template configuration, supporting v1 and v2 formats.

    Tries ``cookieplone.json`` (v2) first then falls back to
    ``cookiecutter.json`` (v1).  For v2, the schema's ``properties``
    dict is flattened to a ``{key: default}`` mapping so the rest of
    the analyser can keep treating it like a v1 dict.
    """
    v2 = base_path / "cookieplone.json"
    if v2.is_file():
        data = json.loads(v2.read_text())
        properties = data.get("schema", {}).get("properties", {})
        return {key: prop.get("default", "") for key, prop in properties.items()}
    v1 = base_path / "cookiecutter.json"
    if v1.is_file():
        return json.loads(v1.read_text())
    return {}


def _read_repository_config(repo_root: Path) -> dict:
    """Read the repository-level config, supporting v1 and v2 formats."""
    v2 = repo_root / "cookieplone-config.json"
    if v2.is_file():
        return json.loads(v2.read_text())
    v1 = repo_root / "cookiecutter.json"
    if v1.is_file():
        return json.loads(v1.read_text())
    return {}


def _read_global_versions(repo_root: Path) -> set[str]:
    """Return the set of version keys declared in ``cookieplone-config.json``."""
    config = _read_repository_config(repo_root)
    return set(config.get("config", {}).get("versions", {}).keys())


SYMBOLS = {
    "not_found": {"title": "Not present in cookiecutter.json", "icon": "-"},
    "used": {"title": "Used by the template", "icon": "✅"},
    "not_used": {"title": "Not used in template", "icon": "❗"},
    "missing": {
        "title": "Used by the template, not present in cookiecutter.json",
        "icon": "🚫",
    },
}

VERSIONS_SYMBOLS = {
    "not_used": {"title": "Not referenced by the template", "icon": "-"},
    "used": {"title": "Used by the template", "icon": "✅"},
    "missing": {
        "title": "Used by the template, not declared in cookieplone-config.json",
        "icon": "🚫",
    },
}


def load_template_definitions(repo_root: Path) -> list[tuple[str, Path]]:
    templates = []
    data = _read_repository_config(repo_root)
    for name, template in data.get("templates", {}).items():
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


def extract_versions_keys(existing_keys: set, content: str) -> set:
    """Find references to ``versions.<key>`` and ``versions["<key>"]`` in *content*."""
    for pattern in VERSIONS_PATTERNS:
        matches = {match.groupdict()["key"] for match in pattern.finditer(content)}
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
    payload = {
        "templates": report_data["templates"],
        "versions_templates": report_data.get("versions_templates", {}),
    }
    with open(report_path, "w") as fout:
        json.dump(payload, fout, indent=2)

    return report_path


def _write_csv_report(report_data: dict, report_path: Path) -> Path:
    header = report_data["keys"]["header"]
    rows = report_data["keys"]["rows"]
    versions_header = report_data.get("versions", {}).get("header", [])
    versions_rows = report_data.get("versions", {}).get("rows", [])
    with open(report_path, "w") as fout:
        writer = csv.DictWriter(fout, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
        if versions_rows:
            fout.write("\n")
            versions_writer = csv.DictWriter(fout, fieldnames=versions_header)
            versions_writer.writeheader()
            versions_writer.writerows(versions_rows)
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


def _md_versions_table(report_data: dict) -> list[str]:
    versions_section = report_data.get("versions", {})
    data_rows = versions_section.get("rows", [])
    if not data_rows:
        return []
    rows: list[str] = ["\n", "# Repository versions usage in templates\n\n"]
    columns = versions_section["header"]
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


def _md_versions_legend() -> list[str]:
    rows: list[str] = ["\n", "## Versions Legend\n\n"]
    columns = ["Icon", "Description"]
    rows.extend(_md_table_header_rows(columns))
    for item in VERSIONS_SYMBOLS.values():
        title, icon = item.values()
        rows.append(f"| {icon} | {title} |\n")
    return rows


def _write_md_report(report_data: dict, report_path: Path) -> Path:
    with open(report_path, "w") as fout:
        for row in _md_report_table(report_data):
            fout.write(row)
        for row in _md_legend():
            fout.write(row)
        for row in _md_versions_table(report_data):
            fout.write(row)
        for row in _md_versions_legend():
            fout.write(row)
    return report_path


REPORT_FORMATS = {
    "json": _write_json_report,
    "csv": _write_csv_report,
    "md": _write_md_report,
}


def _analyze_template_folder(
    folder: Path,
    used_keys: set[str],
    used_versions: set[str],
) -> tuple[set[str], set[str]]:
    all_files = folder.glob("**/*")
    for filepath in all_files:
        data = filepath.name
        is_file = filepath.is_file()
        if is_file and is_binary(f"{filepath}"):
            continue
        if is_file:
            data = f"{data} {filepath.read_text()}"
        used_keys = extract_template_keys(used_keys, data)
        used_versions = extract_versions_keys(used_versions, data)
    return used_keys, used_versions


def analyze_template_usage(
    templates: list[tuple[str, Path]],
    global_versions: set[str],
) -> tuple[set, dict, set, dict]:
    all_keys: set[str] = set()
    template_keys: dict[str, dict[str, list[str]]] = defaultdict(dict)
    all_versions: set[str] = set(global_versions)
    template_versions: dict[str, dict[str, list[str]]] = defaultdict(dict)
    for name, base_path in templates:
        questions = _read_template_config(base_path)
        # Scan the raw config file for variable references too (jinja
        # expressions in default values).
        raw_context = ""
        for fname in ("cookieplone.json", "cookiecutter.json"):
            config_file = base_path / fname
            if config_file.is_file():
                raw_context = config_file.read_text()
                break
        # Already add __folder_name, used in folder name
        used_keys = extract_template_keys({"__folder_name"}, raw_context)
        used_versions = extract_versions_keys(set(), raw_context)
        items = {key for key in questions if is_valid_key(key)}
        template_folders = (
            base_path / "hooks",
            base_path / "{{ cookiecutter.__folder_name }}",
        )
        for template_folder in template_folders:
            used_keys, used_versions = _analyze_template_folder(
                template_folder, used_keys, used_versions
            )

        template_keys[name]["all"] = sorted_list(items)
        template_keys[name]["used"] = sorted_list(used_keys & items)
        template_keys[name]["not_used"] = sorted_list(items.difference(used_keys))
        template_keys[name]["missing"] = sorted_list(used_keys.difference(items))
        occurrences = items.union(used_keys)
        all_keys = all_keys.union(occurrences)

        template_versions[name]["used"] = sorted_list(used_versions & global_versions)
        template_versions[name]["missing"] = sorted_list(
            used_versions.difference(global_versions)
        )
        all_versions = all_versions.union(used_versions)
    return all_keys, template_keys, all_versions, template_versions


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


def generate_versions_usage_matrix(
    all_versions: set,
    template_versions: dict,
    all_templates: list[str],
) -> list[dict]:
    versions_usage = []
    for key in sorted(all_versions):
        key_report = {"version": key}
        for template in all_templates:
            status = VERSIONS_SYMBOLS["not_used"]["icon"]
            versions = template_versions.get(template, {})
            if key in versions.get("used", []):
                status = VERSIONS_SYMBOLS["used"]["icon"]
            elif key in versions.get("missing", []):
                status = VERSIONS_SYMBOLS["missing"]["icon"]
            key_report[template] = status
        versions_usage.append(key_report)
    return versions_usage


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
    global_versions = _read_global_versions(repo_root)
    all_keys, template_keys, all_versions, template_versions = analyze_template_usage(
        templates, global_versions
    )
    keys_usage = generate_key_usage_matrix(all_keys, template_keys, all_templates)
    versions_usage = generate_versions_usage_matrix(
        all_versions, template_versions, all_templates
    )
    report_data = {
        "templates": template_keys,
        "keys": {
            "header": ["key", *all_templates],
            "rows": keys_usage,
        },
        "versions_templates": template_versions,
        "versions": {
            "header": ["version", *all_templates],
            "rows": versions_usage,
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
