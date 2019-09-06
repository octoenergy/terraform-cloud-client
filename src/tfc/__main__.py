"""
Entrypoint module, à la PEP 0338, allowing `python -m tfc`

The `main` function in this module is also installed as a `console_scripts`
entry_point, which installs `tfc` as an executable script.
"""
import sys

# We need to use an absolute import here. Relative imports don't work from
# __main__ modules.
from tfc.cli import main

if __name__ == "__main__":
    sys.exit(main())
