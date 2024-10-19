# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Main entry point.
# ---------------------------------------------------------
# ./scripts/__main__.py

import argparse

from txt2latex.scripts import \
    translate, \
    tests

def main():
    """ Main entry point

    This function is solely used to parse command line arguments and start the
    corresponding process
    """

    main_parser = argparse.ArgumentParser(
        description="Application to translate text expression to latex expression",
        prog="txt2latex"
    )
    subparsers = main_parser.add_subparsers(dest="cmd")

    # Translate process:
    # ------------------
    parser_translate = subparsers.add_parser("translate",help="translate help")

    # Required arguments:
    group_translate = parser_translate.add_mutually_exclusive_group(required=True)
    group_translate.add_argument("expression", nargs='?', type=str, help="The expression to translate")
    group_translate.add_argument("-f","--file",nargs=1,type=str,help="The file containing the text to translate")

    # Optional arguments:
    #TODO


    # Tests process:
    # --------------
    parser_tests = subparsers.add_parser("tests",help="tests help")

    # Operator process:
    # -----------------
    parser_operators = subparsers.add_parser("operators",help="operators help")

    # Start process:
    # --------------
    args = main_parser.parse_args()
    if args.cmd == "translate":
        translate(args)
    elif args.cmd == "tests":
        tests()
    elif args.cmd == "operators":
        print("I should start the operators process")

if __name__ == "__main__":
    main()