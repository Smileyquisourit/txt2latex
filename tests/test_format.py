# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Tests for the parser
# ---------------------------------------------------------
# ./tests/test_format.py

import unittest

from txt2latex.src.baseComponent.logicalComponent import *
from txt2latex.src.baseComponent.latexComponent import *
from txt2latex.src.baseComponent.loadOperator import _LEVEL0_OPERATORS_DICT, _nullOperator

class formatExpression(unittest.TestCase):
    """ Test Class for the string representation

    This class test that the LatexExpression are correctly represented.

    This class may be changed before version 1.0.0 to test the entire
    LatexExpression class, and some other Test Class may be add to test
    each of the component in baseComponent.
    """

    expected_simpleLatexExpression = r"p^{2} - omega_{BdG}^{2} + 2omega_{BdG}pzeta_{BdG}"
    
    def construct_SimpleLatexExpression(self):
        """ Construct the object associated with the 'simpleLatexExpression'

        Simple latex expression:
        ------------------------

        Expression: p^2 - omega_BdG^2 + 2*omega_BdG*p*zeta_BdG
        component:  aaa b bbbbbbbbbbb c cddddddddddeefffffffff
        """

        # Logical block:
        # --------------
        self.simplelogic_element = LogicalElement("p^2 - omega_BdG^2 + 2*omega_BdG*p*zeta_BdG")

        # Components :
        # ------------
        A = LatexElement("p",superScript="2")
        B = LatexElement("omega","BdG","2")
        C = LatexElement("2")
        D = LatexElement("omega","BdG")
        E = LatexElement("p")
        F = LatexElement("zeta","BdG")

        # Operators :
        # -----------
        B_op = _LEVEL0_OPERATORS_DICT["-"]
        C_op = _LEVEL0_OPERATORS_DICT["+"]
        D_op = _LEVEL0_OPERATORS_DICT["*"]
        E_op = _LEVEL0_OPERATORS_DICT["*"]
        F_op = _LEVEL0_OPERATORS_DICT["*"]

        # Simple expression:
        # ------------------
        self.simpleLatexExpression = LatexExpression(LatexDelimitor())
        self.simpleLatexExpression.add_children(_nullOperator, A)
        self.simpleLatexExpression.add_children(B_op, B)
        self.simpleLatexExpression.add_children(C_op, C)
        self.simpleLatexExpression.add_children(D_op, D)
        self.simpleLatexExpression.add_children(E_op, E)
        self.simpleLatexExpression.add_children(F_op, F)

    def setUp(self):
        self.construct_SimpleLatexExpression()
    
    def simpleLatexExpression(self):
        """ Tests the representation of a simple latex expression """

        self.assertEqual(
            self.expected_simpleLatexExpression,
            str(self.simpleLatexExpression)
        )