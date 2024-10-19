# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Wrapper for starting translating process.
# ---------------------------------------------------------
# ./scripts/translate.py

"""CLI for translating a mathematical equation into LaTeX.

This script is a wrapper that allows translating text into a LaTeX equation. 
It takes as an argument either a path to a txt file containing the text to be 
translated, or the text itself. Additionally, an argument allows specifying 
whether what is to be transcribed is a matrix or not (in upcoming version).
"""

import sys
import argparse

from txt2latex.src.parsers import logical_parser
from txt2latex.src.parsers import latex_parser

multiple_logical_block = r"a + (p^2 + 2*omega*(b - c))*(p^3 - (a*p^2)*(c - d) - a)"

def main(args):
    """ Entry-point

        Function responsible to parse an expression and translate it to a latex expression.
    """

    if args.file:
        # read the expression
        #expression_to_translate = ...
        raise NotImplementedError("Reading the expression from a file isn't implemented yet, but it will be comming soon ;)")
    else:
        expression_to_translate = args.expression

    sys.stdout.write("Starting tanslate process...\n")
    sys.stdout.flush()
    logical_expr = logical_parser.parse_txt_expression(expression_to_translate)
    latex_expr = latex_parser.parse_logical_expression(logical_expr)

    sys.stdout.write(f"I've found the following expression:\n{latex_expr}")


if __name__ == "__main__":

    # -*- COMMENT -*-
    #   Here we mimic the parser created in the main function of
    # the __main__.py in the scripts directory (this directory).
    # This enable the user to use directly the translate functionality

    # Create parser:
    parser_translate = argparse.ArgumentParser("translate",help="translate help")
    group_translate = parser_translate.add_mutually_exclusive_group(required=True)
    group_translate.add_argument("expression", nargs='?', type=str, help="The expression to translate")
    group_translate.add_argument("-f","--file",nargs=1,type=str,help="The file containing the text to translate")

    # Parse arg:
    args = parser_translate.parse_args()
    args.cmd = "translate"
    
    # Start process:
    main(args)