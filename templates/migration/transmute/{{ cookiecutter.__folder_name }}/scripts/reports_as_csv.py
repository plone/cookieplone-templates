from collective.transmute.settings import get_settings

import csv
import json


def generate_csv_reports() -> None:
    """Generate csv reports from the main report.json file."""
    settings = get_settings()
    reports_location = settings.config.get("reports_location")
    if not reports_location or not reports_location.exists():
        raise ValueError("Invalid reports_location found in transmute.toml")

    report = reports_location / "report.json"

    if not report.exists():
        raise ValueError(f"Report not found: {report}")

    data = json.loads(report.read_text())

    reports_location = settings.config.get("reports_location")
    exports = ("creators", "subjects")
    for key in exports:
        tmp = data[key]
        if not isinstance(tmp, dict):
            continue
        values = sorted(
            [(k, v) for k, v in tmp.items()], key=lambda x: x[1], reverse=True
        )
        with open(reports_location / f"csv_{key}.csv", "w") as fh:
            writer = csv.writer(fh)
            writer.writerow(["Value", "Count"])
            for k, v in values:
                writer.writerow([k, v])


if __name__ == "__main__":
    generate_csv_reports()
