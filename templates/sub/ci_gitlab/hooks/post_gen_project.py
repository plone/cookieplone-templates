"""Pre generation hook."""

from collections import OrderedDict
from pathlib import Path
import shutil

output_path = Path().resolve()

context: OrderedDict = {{cookiecutter}}


def main():
    """Validate context."""
    if context.get("feature_headless", "0") == "0":
        # We need to remove the frontend folder, because
        # We are using the classic template and it doesn't have it
        shutil.rmtree(output_path / "frontend", dir_fd=True)


if __name__ == "__main__":
    main()
