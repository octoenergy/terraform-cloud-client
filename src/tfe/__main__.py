"""
Entrypoint module, à la PEP 0338, allowing `python -m tfe`

The `main` function in this module is also installed as a `console_scripts`
entry_point, which installs `tfe` as an executable script.
"""
import sys


def main(args=None):
    """The entry point when running `tfe` as a script"""
    if args is None:
        args = sys.argv[1:]

    print("You are running the main() function in the tfe.__main__ Python package.")


if __name__ == "__main__":
    sys.exit(main())
