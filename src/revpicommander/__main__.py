# -*- coding: utf-8 -*-
"""Start main application of this package."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv2"

# If we are running from a wheel, add the wheel to sys.path
if __package__ == "":
    from os.path import dirname
    from sys import path

    # __file__ is package-*.whl/package/__main__.py
    # Resulting path is the name of the wheel itself
    package_path = dirname(dirname(__file__))
    path.insert(0, package_path)

if __name__ == "__main__":
    import sys

    try:
        # Use absolut import in the __main__ module
        from revpicommander.revpicommander import main

        # Run the main application of this package
        sys.exit(main())

    except Exception as e:
        sys.stdout.write(f"Can not start __main__ module: {e}")
        sys.stdout.write("\n")
        sys.exit(1)
