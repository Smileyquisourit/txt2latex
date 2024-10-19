# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Script for loading the operator to use in memory
# ---------------------------------------------------------
# ./src/baseComponent/loadOperator.py

"""Script for defining the operators used and loading them in memory

This script defines a number of common operators and contains different functions
for creating operators based on arguments or a JSON file. The idea is that
operators are defined at several levels:
- level 0: Operators defined in this script.
- level 1: Operators defined in a JSON file (dev)
- level 2: Operators defined in a configuration file (dev)
- level 3: Operators defined by arguments (dev)
This allows operators to be overridden in a durable way with those of level 1, which
will override the operators of level 0, and in a temporary way with the operators of
level 3, which will override the operators of level 2, 1, and 0. 
The level 2 (configuration file) is imagined for overriding the default operator of a user
when sharing an expression.

This script also has a function to retrieve all the defined operators, first constructing
those defined in this script, then those contained in the JSON files, then those defined
in a configuration file (if provided) and finally those created by arguments.

Common Operator:
'+' (1) -> '{expr1} + {expr2}'
'-' (1) -> '{expr1} - {expr2}'
'*' (1) -> '{expr1} {expr2}'
'/' (2) -> '\frac{expr1}{expr2}'
"""

#TODO: add level 1 and level 2 and level 3
#TODO: add selection from level
#TODO: add test for all 4 levels

from .latexComponent import LatexOperator

# Level 0:
# --------
_nullOperator = LatexOperator('',0)
_plusOperator = LatexOperator("+",1)
_minusOperator = LatexOperator("-",1)
_multOperator = LatexOperator("*",1)
_fracOperator = LatexOperator("/",2)

def _nullOperatorFormat(expr1,expr2):
    return expr1+expr2

def _multOperatorFormat(expr1,expr2):
    return f"{expr1}{expr2}"

def _fracOperatorFormat(expr1,expr2):
    return rf"\frac{"{"}{expr1}{"}"}{"{"}{expr2}{"}"}"

_nullOperator.add_formatting(_nullOperatorFormat)
_multOperator.add_formatting(_multOperatorFormat)
_fracOperator.add_formatting(_fracOperatorFormat)

_LEVEL0_OPERATORS = [_plusOperator, _minusOperator, _multOperator, _fracOperator]
_LEVEL0_OPERATORS_DICT = {'+':_plusOperator, '-':_minusOperator,
                          '*':_multOperator, '/':_fracOperator}


# Level 1:
# --------
def load_fromJSON():
    pass


# Level 2:
# --------
def create_fromArgs():
    pass

#TODO
def getOperators() -> list[LatexOperator]:
    return _LEVEL0_OPERATORS