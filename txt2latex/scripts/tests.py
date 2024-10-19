# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Wrapper for starting tests process.
# ---------------------------------------------------------
# ./scripts/tests.py

""" CLI for testing the application.

This script is a wrapper for executing the differents test of the application,
one at a time, or every tests.
"""

from tests.run_tests import run_all

def main():
    """ Entry-point

        Function responsible to treat command-line arguments and start process
    """

    # Start process:
    # --------------
    print("-- DEV TEST --")
    run_all()


if __name__ == "__main__":
    main()