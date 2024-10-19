# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Functions to parse aa expression to a logical one
# ---------------------------------------------------------
# ./src/parsers/logical_parser.py

""" A set of functions for parsing an expression.

This module contains functions that allow separating a complex expression
and building the logical groups that make it up.
"""


# Import statements:
# ==================
from ..baseComponent import logicalComponent


# Functions definitions:
# ======================
def parse_txt_expression(expr:str) -> logicalComponent.LogicalBlock:
    """Parse an expression.

    Parse a complex expression and return a LogicalBlock
    representing the expression.

    Arguments:
    expr : str
        The expression to parse

    Return:
    logicalBlock.LogicalBlock
        The LogicalBlock representing the expression.

    Raise:
    TypeError : When the given argument isn't of the correct type
    """

    # Type checking:
    # --------------
    if not isinstance(expr,str):
        raise TypeError(f"The expression to parse must be a string, instead I've received a '{type(expr)}'")

    # Initialisation:
    # ---------------
    root_block = logicalComponent.LogicalBlock(name='root')
    stack = list((root_block,))
    buff = ""

    # Parse the expression:
    # ---------------------
    for char in expr:
        
        if char == '(':
            if buff != "":
                stack[-1].add_children(logicalComponent.LogicalElement(buff))
                buff = ""
            stack.append(logicalComponent.LogicalBlock())

        elif char == ')':
            if buff != "":
                stack[-1].add_children(logicalComponent.LogicalElement(buff))
                buff = ""
            last_block = stack.pop(-1)
            stack[-1].add_children(last_block)

        else:
            buff += char

    return root_block