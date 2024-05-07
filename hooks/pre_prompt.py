"""Pre Prompt hook."""

import sys

try:
    from cookieplone.utils import console

    HAS_COOKIEPLONE = True
except ModuleNotFoundError:
    HAS_COOKIEPLONE = False


def main():
    """Check if we have cookieplone installed."""
    if not HAS_COOKIEPLONE:
        print("This template should be run with cookieplone")
        sys.exit(1)
    else:
        console.print_plone_banner()


if __name__ == "__main__":
    main()
