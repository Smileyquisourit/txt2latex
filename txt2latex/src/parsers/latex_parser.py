# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Functions to parse a logical expression to a latex one
# ---------------------------------------------------------
# ./src/parsers/latex_parser.py

""" Ensemble de fonction permettant de parser une expression.

    Ce module contient des fonctions permettant de parser une expression logique
complexe et de créer l'expression Latex qui en résulte
"""

# Import statement:
# =================
import re
from typing import Union, Optional
from txt2latex.src.baseComponent import logicalComponent, latexComponent
from txt2latex.src.baseComponent.loadOperator import _LEVEL0_OPERATORS, _nullOperator


# Constant definition:
# ====================
latex_element_pattern = re.compile(r"(?P<mainContent>[a-zA-Z0-9]+)(_(?P<subScript>[a-zA-Z0-9_]*)|)(\^(?P<superScript>.*)|)")


# Functions definitions:
# ======================
def _findOperator(char:str,operators:list[latexComponent.LatexOperator]) -> Optional[latexComponent.LatexOperator]:
    """ Function to associate a caracter to an operator

    Iterate through the given list of operator and return the operator
    when one match. Return None if no match is found.

    Arguments:
    char : str
        The caracter to search in the operator.
    operators : list[LatexOperator]
        The list of operator to serach in.

    Return:
    LatexOperator | None
        The resulting match, or None if no match was found
    """
    for operator in operators:
        if char == operator:
            return operator
        
    return None
def latex_element_factory(element:str) -> latexComponent.LatexElement:
    """ Construct a LatexElement from a string

    The element to construct is expected to be in the form 'aa_bb^cc'

    Arguments:
    element : str
        The string from which the element is constructed.

    Return:
    latex_element : LatexElement
        The LatexElement resulting.

    Raise:
    TypeError : When the argument isn't of the correct type
    RuntimeError : When the string can't be parsed
    """

    # Type Check:
    # -----------
    if not isinstance(element,str):
        raise TypeError(f"The element to parse must be a string, instead I've received a '{type(element)}'")

    # Parse element:
    # --------------
    if match := latex_element_pattern.match(element):

        latex_element = latexComponent.LatexElement(**match.groupdict())

    else:
        raise RuntimeError(f"Impossible to parse the following element: '{element}'")
    return latex_element
def parse_logical_element(expr:logicalComponent.LogicalElement, 
                          latex_expr:latexComponent.LatexExpression,
                          operators:list[latexComponent.LatexOperator]) \
    -> tuple[latexComponent.LatexExpression,Optional[latexComponent.LatexOperator]]:
    """ Parse a logic element.

    Parse a logic element by separating the different latex element with the operator
    ('+','-','*','/',...) given in argument. It the construct the LatexElement and add
    it to the LatexExpression given in arguments.

    A logic element is in the form:
        'p^2 - omega_BdG^2 + 2*omega_BdG*p'
    In this exemple, the element be decomposed in:
    1. (,'p^2')          -> mainContent:'p',     superScript:'2',  subScript:None
    2. ('+','omega_BdG') -> mainContent:'omega', superScript:None, subScript:'BdG'
    3. ('+','2')         -> mainContent:'2',     superScript:None, subScript:None,
    4. ('*','omega_BdG)  -> mainContent:'omega', superScript:None, subScript:'BdG'
    5. ('*','p')         -> mainContent:'p',     superScript:None, subScript:None,

    In the case where the expression contains only one operator and no other elements,
    this function will return the LatexExpression unchanged and the LatexOperator found.
    In case where the expression ends with an operator, it means that the operator is for
    the child of the LogicalBlock parent to the LogicalElement given in arguments, so we
    return it.

    Arguments:
    expr : LogicalElement
        The logic element to parse.
    latex_expr : LatexExpression
        The LaTeX expression to which the found LaTeX elements should be added.
    operators : LatexOperators
        The LatexOperators used for parsing the differents elements of the expression.

    Return:
    latex_expr : LatexExpression
        The LaTeX expression with the newly added LaTeX elements.
    currentOperator : LatexOperator | None
        The latest operator found if it wasn't used, else None

    Raise:
    TypeError : When one of the argument isn't of the correct type
    """

    # Type Check:
    # -----------
    if not isinstance(expr,logicalComponent.LogicalElement):
        raise TypeError(f"The expression to parse must be a LogicalElement, instead I've received a '{type(expr)}'")
    if not isinstance(latex_expr,latexComponent.LatexExpression):
        raise TypeError(f"The latex expression to complete must be a LatexElement, instead I've received a '{type(expr)}'")
    
    # Initialisation:
    # ---------------
    buff = ""
    currentOperator = _nullOperator
    
    # Parse expression:
    # -----------------
    for char in expr.contents:

        # Ignore empty char
        if char == ' ':
            continue

        # If next element found
        if operator := _findOperator(char,operators):
            # The operator found correspond to the next expression !!

            # Ignore case where the expression start with an operator
            if buff == "":
                currentOperator = operator
                continue

            latex_expr.add_children(currentOperator,latex_element_factory(buff))
            currentOperator = operator
            buff = ""
        
        # If next element not found, buffering continu
        else:
            buff += char
    
    # End of the expression. If the buffer is still empty, in means that the
    # expression end with an operator.
    if buff != "":
        latex_expr.add_children(currentOperator,latex_element_factory(buff))
        currentOperator = None

    # Return results:
    # ---------------
    return latex_expr, currentOperator

def _parse_logical_expression(logic_expr:logicalComponent.LogicalBlock,
                              delimitor:latexComponent.LatexDelimitor) \
                            -> tuple[latexComponent.LatexExpression, latexComponent.LatexOperator]:
    """ Parse a logical expression.

    Parse a logical expression by scanning it from left to right, and parsing each of 
    children. If a children is also a LogicalBlock, it parse it recursively.

    Arguments:
    expr : logicalComponent.LogicalBlock
        The logical expression to parse.
    delimitor : LatexDelimitor
        The delimitor to use for new LatexExpression

    Return:
    latex_expr : latexComponent.LatexExpression
        The resulting LatexExpression.
    currOperator : latexComponent.LatexOperator
        The latest operator found if it wasn't used, else None

    Raise:
    TypeError : When one of the argument isn't of the correct type
    """

    # Type Check:
    # -----------
    if not isinstance(logic_expr,logicalComponent.LogicalBlock):
        raise TypeError(f"The logical expression to parse must be a LogicalBlock, instead I've received a '{type(logic_expr)}'")
    if not isinstance(delimitor,latexComponent.LatexDelimitor):
        raise TypeError(f"The delimitor to use must be a LatexDelimitor, instead I've received a '{type(delimitor)}'")
    
    # Constante definition:
    # ---------------------
    par_delimitor = latexComponent.LatexDelimitor("(",")")

    # Initialization:
    # ---------------
    latex_expr = latexComponent.LatexExpression(delimitor)
    
    # Start recursive process:
    # ------------------------
    currOperator = _nullOperator
    for child in logic_expr.children:

        if isinstance(child,logicalComponent.LogicalElement):
            latex_expr, nextOperator = parse_logical_element(child,latex_expr,_LEVEL0_OPERATORS)
            if not nextOperator:
                currOperator = _nullOperator
            else:
                currOperator = nextOperator
            
        else:
            expression, nextOperator = _parse_logical_expression(child,par_delimitor)
            if expression:
                latex_expr.add_children(currOperator,expression)
                currOperator = _nullOperator
            if nextOperator:
                currOperator = nextOperator
    
    return latex_expr, currOperator
def parse_logical_expression(expr:logicalComponent.LogicalBlock) -> latexComponent.LatexExpression:
    """ Wrapper parsing a logical expression.

    Allows parsing a logical expression using a recursive function. This function enables 
    the handling of variables that the recursive function returns, some of which are only 
    necessary for the recursive function itself.

    Arguments:
    expr : logicalComponent.LogicalBlock
        The logical element to parse

    Return:
    root_expression : LatexExpression
        The resulting latex expression

    Raise:
    TypeError : When one of the argument isn't of the correct type
    """

    # Type Check:
    # -----------
    if not isinstance(expr,logicalComponent.LogicalBlock):
        raise TypeError(f"The expression to parse must be a LogicalBlock, instead I've received a '{type(expr)}'")

    # Start process:
    # --------------
    null_delimitor = latexComponent.LatexDelimitor()
    root_expression, _ = _parse_logical_expression(expr,null_delimitor)

    return root_expression
