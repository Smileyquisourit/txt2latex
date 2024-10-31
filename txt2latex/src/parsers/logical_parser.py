# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Functions to parse aa expression to a logical one
# ---------------------------------------------------------
# ./src/parsers/logical_parser.py

""" A class for parsing a text expression to a logical one.

This module contains a class that allow separating a complex expression
and building the logical groups that make it up.
"""


# Import statements:
# ==================
from ..baseComponent import logicalComponent
from py_utils import Logueur


# Class definition:
# =================

class LogicalParser():
    """ LogicalParser class.

    An instance of this class can translate a given text expression
    to a logical expression. Some configuration is possible when
    constructing an instance, like the character used for delimiting
    logical block.
    """

    def __init__(self, log:Logueur) -> None:
        """ Constructor of LogicalParser """
        
        # Type Check:
        # ===========
        if not isinstance(log,Logueur):
            raise ValueError(f"The log must be a Logueur, instead I've received a '{type(log)}'")
        
        # Initialyse instance:
        # --------------------
        self.log = log

    def parse(self, expr:str) -> logicalComponent.LogicalBlock:
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
        recursivity_level = 0
        self.log.info(f"Starting parsing to logical expression of {expr}")
        for char in expr:

            if char == '(':
                recursivity_level += 1
                self.log.debug(f"New children found, recursivity level = {recursivity_level}")
                if buff != "":
                    stack[-1].add_children(logicalComponent.LogicalElement(buff))
                    self.log.debug(f"Adding the predecessing children {buff}")
                    buff = ""
                stack.append(logicalComponent.LogicalBlock())

            elif char == ')':
                recursivity_level -= 1
                self.log.debug(f"End of children found, recursivity level = {recursivity_level}")
                if buff != "":
                    stack[-1].add_children(logicalComponent.LogicalElement(buff))
                    self.log.debug(f"Adding the predecessing children {buff}")
                    buff = ""
                last_block = stack.pop(-1)
                stack[-1].add_children(last_block)

            else:
                buff += char

        return root_block