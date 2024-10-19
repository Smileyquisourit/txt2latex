# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Tests for the parser
# ---------------------------------------------------------
# ./tests/test_parser.py

import unittest

from txt2latex.src.baseComponent.logicalComponent import *
from txt2latex.src.baseComponent.latexComponent import *
from txt2latex.src.baseComponent.loadOperator import _LEVEL0_OPERATORS, _LEVEL0_OPERATORS_DICT, _nullOperator
from txt2latex.src.parsers import logical_parser, latex_parser

class ParseExpression(unittest.TestCase):
    """ Test Class for the parsing functionality

    This class test that the different parsing function are working
    correctly.

    This will be changed before version 1.0.0 to test the ExpressionParser
    object, that will do the parsing.
    """

    multiple_logical_block = r"a + (p^2 + 2*omega*(b - c))*(p^3 - (a*p^2)*(c - d) - a)"
    simple_latex_expression = r"p^2 - omega_BdG^2 + 2*omega_BdG*p*zeta_BdG"
    multiple_latex_expression = r"-(p^2 - omega_BdG^2 + 2*omega_BdG*p/zeta_BdG)*(m_alpha + 2/Z_alpha*m_q - 2*Z_alpha*p + m_q*p - p^2)"


    def construct_MultipleLogicalBlock(self):
        """ Construct the object assiociated with the 'multiple_logical_block'

        Logical expression:
        -------------------

        Expression: a + ( p^2 + 2 * omega * ( b - c ) ) * ( p^3 - ( a * p^2 ) * ( c - d ) - a )
        level 0:        |                   |---01--| |   |       |----02---|   |---03--|     |
        level 1:        |--------------11-------------|   |-----------------12----------------|
        root   :   |---------------------------------------------------------------------------|
        """
        
        # Logical Expression:
        # ===================

        # Level 0:
        block_01 = LogicalBlock(); block_01.add_children(LogicalElement(r"b - c"))
        block_02 = LogicalBlock(); block_02.add_children(LogicalElement(r"a*p^2"))
        block_03 = LogicalBlock(); block_03.add_children(LogicalElement(r"c - d"))

        # Level 1:
        block_11 = LogicalBlock()
        block_11.add_children(LogicalElement(r"p^2 + 2*omega*"))
        block_11.add_children(block_01)
        block_12 = LogicalBlock()
        block_12.add_children(LogicalElement(r"p^3 - "))
        block_12.add_children(block_02)
        block_12.add_children(LogicalElement(r'*'))
        block_12.add_children(block_03)
        block_12.add_children(LogicalElement(r" - a"))

        # root:
        self.expected_logicalRoot = LogicalBlock(name='root')
        self.expected_logicalRoot.add_children(LogicalElement(r"a + "))
        self.expected_logicalRoot.add_children(block_11)
        self.expected_logicalRoot.add_children(LogicalElement(r"*"))
        self.expected_logicalRoot.add_children(block_12)
    def construct_SimpleLatexExpression(self):
        """ Construct the object assiociated with the 'simple_latex_expression'

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

        # Expected simple expression:
        # ---------------------------
        self.expected_simpleLatexExpression = LatexExpression(LatexDelimitor())
        self.expected_simpleLatexExpression.add_children(LatexOperator(""), A)
        self.expected_simpleLatexExpression.add_children(B_op, B)
        self.expected_simpleLatexExpression.add_children(C_op, C)
        self.expected_simpleLatexExpression.add_children(D_op, D)
        self.expected_simpleLatexExpression.add_children(E_op, E)
        self.expected_simpleLatexExpression.add_children(F_op, F)
    def construct_MultipleLatexExpression(self):
        """ Construct the object associated with the 'multiple_latex_expression'

        Multiple logical expression:
        --------------------------

        Expression: -(p^2 - omega_BdG^2 + 2*omega_BdG*p/zeta_BdG)*(m_alpha + 2/Z_alpha*m_q - 2*Z_alpha*p + m_q*p - p^2)
        level 0:     |------------------------------------------| |---------------------------------------------------|
        root:      |+ ------------------------------------------ + --------------------------------------------------- |

        Multiple latex expression:
        --------------------------

        Expression: -(p^2 - omega_BdG^2 + 2*omega_BdG*p/zeta_BdG)*(m_alpha + 2/Z_alpha*m_q - 2*Z_alpha*p + m_q*p - p^2)
        level 0:      --- + +++++++++++ - -++++++++++--+++++++++   ------- + +--------++++ - -++++++++-- + +++-- + +++
        level 1:    +++++++++++++++++++++++++++++++++++++++++++++------------------------------------------------------
        """

        # Logical Expression:
        # ===================

        block01 = LogicalBlock()
        block01.add_children(LogicalElement("p^2 - omega_BdG^2 + 2*omega_BdG*p/zeta_BdG"))
        block02 = LogicalBlock()
        block02.add_children(LogicalElement("m_alpha + 2/Z_alpha*m_q - 2*Z_alpha*p + m_q*p - p^2"))
        self.multiple_logical_block2 = LogicalBlock(name="root")
        self.multiple_logical_block2.add_children(LogicalElement("-"))
        self.multiple_logical_block2.add_children(block01)
        self.multiple_logical_block2.add_children(LogicalElement("*"))
        self.multiple_logical_block2.add_children(block02)

        # Latex Expression:
        # =================

        # Level 0:
        # --------
        component_0a = LatexExpression(LatexDelimitor("(",")"))
        component_0a.add_children(_nullOperator, LatexElement("p",superScript="2"))
        component_0a.add_children(_LEVEL0_OPERATORS_DICT["-"], LatexElement("omega","BdG","2"))
        component_0a.add_children(_LEVEL0_OPERATORS_DICT["+"], LatexElement("2"))
        component_0a.add_children(_LEVEL0_OPERATORS_DICT["*"], LatexElement("omega","BdG"))
        component_0a.add_children(_LEVEL0_OPERATORS_DICT["*"], LatexElement("p"))
        component_0a.add_children(_LEVEL0_OPERATORS_DICT["/"], LatexElement("zeta","BdG"))

        component_0b = LatexExpression(LatexDelimitor("(",")"))
        component_0b.add_children(_nullOperator, LatexElement("m","alpha"))
        component_0b.add_children(_LEVEL0_OPERATORS_DICT["+"], LatexElement("2"))
        component_0b.add_children(_LEVEL0_OPERATORS_DICT["/"], LatexElement("Z","alpha"))
        component_0b.add_children(_LEVEL0_OPERATORS_DICT["*"], LatexElement("m","q"))
        component_0b.add_children(_LEVEL0_OPERATORS_DICT["-"], LatexElement("2"))
        component_0b.add_children(_LEVEL0_OPERATORS_DICT["*"], LatexElement("Z","alpha"))
        component_0b.add_children(_LEVEL0_OPERATORS_DICT["*"], LatexElement("p"))
        component_0b.add_children(_LEVEL0_OPERATORS_DICT["+"], LatexElement("m","q"))
        component_0b.add_children(_LEVEL0_OPERATORS_DICT["*"], LatexElement("p"))
        component_0b.add_children(_LEVEL0_OPERATORS_DICT["-"], LatexElement("p",superScript="2"))

        # Level 1:
        # --------
        self.expected_multipleLatexExpression = LatexExpression(LatexDelimitor())
        self.expected_multipleLatexExpression.add_children(_LEVEL0_OPERATORS_DICT["-"],component_0a)
        self.expected_multipleLatexExpression.add_children(_LEVEL0_OPERATORS_DICT["*"],component_0b)

    def setUp(self):
        self.construct_MultipleLogicalBlock()
        self.construct_SimpleLatexExpression()
        self.construct_MultipleLatexExpression()

    def test_parseTxtExpression(self):
        """ Test the separation of an expression into logical block """
        
        self.assertEqual(
            self.expected_logicalRoot,
            logical_parser.parse_txt_expression(self.multiple_logical_block)
        )
    def test_uniqueLatexElement(self):
        """ Test the construction of different latex single element """

        # Definition of the latex elements:
        # ---------------------------------
        latex_element0 = LatexElement("omega")
        latex_element1 = LatexElement("omega",superScript="2")
        latex_element2 = LatexElement("omega","BdG")
        latex_element3 = LatexElement("omega","BdG","2")

        # Assertion:
        # ----------
        self.assertEqual(latex_element0, latex_parser.latex_element_factory("omega"))
        self.assertEqual(latex_element1, latex_parser.latex_element_factory("omega^2"))
        self.assertEqual(latex_element2, latex_parser.latex_element_factory("omega_BdG"))
        self.assertEqual(latex_element3, latex_parser.latex_element_factory("omega_BdG^2"))
    def test_simpleLatexElement(self):
        """ Tests the construction of latex elements from a logical element"""

        root_expr = LatexExpression(LatexDelimitor())
        root_expr, _ = latex_parser.parse_logical_element(self.simplelogic_element,root_expr,_LEVEL0_OPERATORS)

        self.assertEqual(
            self.expected_simpleLatexExpression,
            root_expr
        )
    def test_multipleLatexExpression(self):
        """ Test the construction of a latex expression """

        self.assertEqual(
            self.expected_multipleLatexExpression,
            latex_parser.parse_logical_expression(self.multiple_logical_block2)
        )

if __name__ == "__main__":
    unittest.main()