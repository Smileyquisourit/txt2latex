# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Definition of the LaTeX components
# ---------------------------------------------------------
# ./src/baseComponent/latexComponent.py

from typing import Union, Optional

class LatexElement(): 
    """A LaTeX element

    An instance of this class represents a LaTeX element, which represents
    a single character or a sequence of characters (without spaces).

    An element is composed of a main content (the character(s) represented),
    a subscript, and a superscript, both of which can be string or empty.
    """
    def __init__(self,mainContent:str,subScript:Optional[str]=None,superScript:Optional[str]=None) -> None:

        # Type checking:
        # --------------
        if not isinstance(mainContent,str):
            raise TypeError(f"The 'mainContent' argument must be a string, instead I've received a '{type(mainContent)}'")

        # Initialize instance:
        # --------------------
        self.mainContent:str = mainContent
        self.subScript:Optional[str] = subScript
        self.superScript:Optional[str] = superScript

    def __eq__(self, other:'LatexElement') -> bool:
        
        # Type Check:
        # -----------
        if not isinstance(other,LatexElement):
            return False
        
        if not self.mainContent == other.mainContent:
            return False
        if not self.subScript == other.subScript:
            return False
        if not self.superScript == other.superScript:
            return False
        
        return True
    def __repr__(self) -> str:
        return "E{" + f"{self.mainContent}_{"{"}{self.subScript}{"}"}^{"{"}{self.superScript}{"}"}" + "}"
    def __str__(self) -> str:
        f_expr = self.mainContent
        if self.subScript:
            f_expr += f"_{"{"}{self.subScript}{"}"}"
        if self.superScript:
            f_expr += f"^{"{"}{self.superScript}{"}"}"
        
        return f_expr

    def set_subScript(self,new_subScript:str) -> None:

        # Type Check:
        # -----------
        if not isinstance(new_subScript,str):
            raise TypeError(f"The 'new_subScript' argument must be a string, instead I've received a '{type(new_subScript)}'")
        
        # Set new subScript:
        # ------------------
        self.subScript = new_subScript
    def set_superScript(self,new_superScript:str) -> None:

        # Type Check:
        # -----------
        if not isinstance(new_superScript,str):
            raise TypeError(f"The 'new_superScript' argument must be a string, instead I've received a '{type(new_superScript)}'")
        
        # Set new subScript:
        # ------------------
        self.superScript = new_superScript


class LatexOperator(): 
    """A LaTeX operator

    An instance of this class represents a LaTeX operator, symbolizing
    a mathematical operator. It is composed of a symbol (character),
    must be able to be formatted with 2 LaTeX expressions or elements,
    as well as a priority (for formatting). It is also possible to specify
    a formatting function.
    """
    def __init__(self,operator:str,priority:int=0) -> None:
        
        # Type Check:
        # -----------
        if not isinstance(operator,str):
            raise TypeError(f"The 'operator' argument must be a str, instead I've received a '{type(operator)}'")
        if not isinstance(priority,int):
            raise TypeError(f"The 'priority' argument must be a int, instead I've received a '{type(priority)}'")
        
        # Initialize instance:
        # --------------------
        self.operator = operator
        self.priority = priority
        self._userDefinedFormattingFunc = None

    def __eq__(self,other:Union['LatexOperator',str]) -> bool:
        """ Check if an operator (txt) is this operator """
        
        # LatexOperator:
        # --------------
        if isinstance(other,LatexOperator):
            return (self.operator == other.operator) and (self.priority == other.priority)
        
        # string:
        # -------
        if isinstance(other,str):
            return self.operator == other
        
        # Unknown type:
        # -------------
        return False
    def __repr__(self) -> str:
        return f"{self.operator} (p{self.priority})"
    
    def formate(self,expr1,expr2):
        """ Format the two expression with the operator.

        This method use the formatting function given if by the user
        if there is one, else will use the default one.
        """
        
        # Stringify the 2 expressions:
        # ----------------------------
        f_expr1 = str(expr1)
        f_expr2 = str(expr2)

        # Formate the expression:
        # -----------------------
        if self._userDefinedFormattingFunc:
            return self._userDefinedFormattingFunc(f_expr1,f_expr2)
        
        return f"{expr1} {self.operator} {expr2}"
    def add_formatting(self,func):
        """ Add a formating function to the operator.

        The given formating expression will be called with 2 str,
        representing respectively the expression before the operator
        and the expression after the operator.
        """
        #TODO add tests on the function?
        self._userDefinedFormattingFunc = func


class LatexDelimitor(): 
    """A LaTeX delimiter

    An instance of this class represents a LaTeX delimiter, which is
    a pair of characters surrounding an expression.
    """
    def __init__(self,openingCaracter:str="",closingCaracter:str="") -> None:

        # Type checking:
        # --------------
        if not isinstance(openingCaracter,str):
            raise TypeError(f"The 'openingCaracter' argument must be a str, instead I've received a '{type(openingCaracter)}'")
        if not isinstance(closingCaracter,str):
            raise TypeError(f"The 'closingCaracter' argument must be a str, instead I've received a '{type(openingCaracter)}'")

        # Initialize instance:
        # --------------------
        self.openingCaracter = openingCaracter
        self.closingCaracter = closingCaracter
    def __eq__(self, other: 'LatexDelimitor') -> bool:
        
        # Type Check:
        # -----------
        if not isinstance(other,LatexDelimitor):
            return False
        
        # Check caracter:
        if self.openingCaracter != other.openingCaracter:
            return False
        if self.closingCaracter != other.closingCaracter:
            return False
        
        return True
    def __repr__(self) -> str:
        return "{" + self.openingCaracter + ";" + self.closingCaracter + "}"
    
    def format(self, expr: str) -> str:

        # Type Check:
        # -----------
        if not isinstance(expr,str):
            raise TypeError(f"Expression to formate must be a string, instead I've received a '{type(expr)}'")

        # Formatting:
        # -----------
        return f"{self.openingCaracter}{expr}{self.closingCaracter}"


class LatexExpression(): 
    """A LaTeX expression

    An instance of this class allows representing a LaTeX expression.
    A LaTeX expression is composed of children, which are ordered and separated
    by operators, and the expression is surrounded by a delimiter.
    
    A child is therefore a pair of operator and LaTeX expression or LaTeX element.
    The operator of the first group is treated differently, in the sense that
    only its character (which should be '+' or '-', a '*' or '/' operator would
    not make sense) is used to format the expression.
    """

    def __init__(self,delimitor:LatexDelimitor) -> None:

        # Type checking:
        # --------------
        if not isinstance(delimitor,LatexDelimitor):
            raise TypeError(f"The 'delimitor' argument must be a LatexDelimitor, instead I've received a '{type(delimitor)}'")

        # Initialize instance:
        # --------------------
        self.children:list[tuple[LatexOperator,Union[LatexElement,LatexExpression]]] = list()
        self.delimitor = delimitor
    def __eq__(self, other: 'LatexExpression') -> bool:
        
        # Type Check:
        # -----------
        if not isinstance(other,LatexExpression):
            return False
        
        # Test delimitor:
        # ---------------
        if self.delimitor != other.delimitor:
            return False
        
        # Test len of children:
        # ---------------------
        if len(self.children) != len(other.children):
            return False
        
        # Test Children:
        # --------------
        for child1,child2 in zip(self.children,other.children):
            if child1 != child2:
                return False
            
        return True
    def __len__(self) -> int:
        return len(self.children)
    
    def __repr__(self) -> str:
        return f"LatexExpression:[d{self.delimitor}]::({len(self.children)}){self.children}"
    def __str__(self) -> str:
        """ Format the LaTeX expression based on the priority of operators.

        The children of this instance are flattened into a single list, alternating operators and
        expressions or elements. The list is then traversed, formatting the operator with the highest
        priority with the two adjacent elements, resulting in a string. The process is repeated until
        there is only one element left in the list.

        In the case of two adjacent operator (separated by an element) of the same priority, the first
        in the list will be formated first, then the second.

        At the beginning of the process, the list should consist of operators alternated with a LaTeX
        expression or a LaTeX element. As the formatting progresses, certain elements are formatted 
        into strings, until there is only one string left, which is then formatted with the LaTeX delimiter
        of the instance and returned to the user.
        """

        if len(self.children) == 0:
            return ""

        # Flatten the children:
        # ---------------------
        max_operatorPriority = 0
        flattened_children = list()
        for operator,element in self.children.copy():
            max_operatorPriority = max(max_operatorPriority,operator.priority)
            flattened_children.append(operator)
            flattened_children.append(element)

        #if self.debug:
        #    stdout.write("\n\n### __STR__ ###\n\n")
        #    stdout.write(f"flattened children before parsing:{flattened_children}\n")

        # Formating process:
        # ------------------
        idx = 0
        while len(flattened_children) > 1:
            
            # Check if we are at the end of the list: 
            if idx >= len(flattened_children):
                idx = 0
                max_operatorPriority -= 1
                # TODO: add a check that their is still some operator in the list
            
            if isinstance(flattened_children[idx],LatexOperator) and flattened_children[idx].priority == max_operatorPriority:

                # -*- COMMENT -*-
                #   If the first operator to be detected is the first child of the flattened children,
                # we need to format it with an empty string. We also add one to the idx to avoid
                # inserting at the end of the list, because we're inserting the resulting expression
                # to idx-1 of the list.
                # if self.debug:
                #     stdout.write(f"[__str__] Operator found a idx {idx} !!\n")

                # Pop the 3 elements:
                expr2 = flattened_children.pop(idx+1)
                operator = flattened_children.pop(idx)
                if idx == 0:
                    expr1 = ""
                    idx += 1
                else:
                    expr1 = flattened_children.pop(idx-1)

                #if self.debug:
                #    stdout.write(f"[__str__]\tExpr1: {expr1}\n")
                #    stdout.write(f"[__str__]\tOperateur: {operator}\n")
                #    stdout.write(f"[__str__]\tExpr2: {expr2}\n\t---\n")
                #    stdout.write(f"[__str__]\tResulting flattened children: {flattened_children}\n")

                # format the 3 elements:
                f_expr = operator.formate(expr1,expr2)
                #if self.debug:
                #    stdout.write(f"[__str__]\tResulting expression: {f_expr}\n\t---\n")

                # Insert back in the list:
                flattened_children.insert(idx-1,f_expr)
                #if self.debug:
                #    stdout.write(f"[__str__]\tResulting flattening children: {flattened_children}\n")

                # Continue to avoid idx += 1
                continue

            # Pass to the next idx:
            idx += 1

        
        # -*- COMMENT -*-
        #   At the end of the parsing, we should have only the 2 following case:
        # 1) The last children is a str
        # 2) The last children is not a str

        #if self.debug:
        #    stdout.write(f"flattened children after parsing:{flattened_children}\n")
        #    stdout.write("\n### __STR__ ###\n")

        if isinstance(flattened_children[0],str):
            f_expr = flattened_children[0]
        else:
            print(f"The last children wasn't a string, it was a {type(flattened_children[0])}:\n{flattened_children[0]}")
            print("Trying to stringify...")
            f_expr = str(flattened_children[0])
        
        return self.delimitor.format(f_expr)

    def add_children(self, operator:LatexOperator,
                     children:Union['LatexExpression',LatexElement]) -> None:
        
        # Type Check: 
        # -----------
        if not isinstance(children,(LatexExpression,LatexElement)):
            raise TypeError(f"The 'children' argument must be a LatexElement or an other LatexExpression, instead I've received a '{type(children)}'")
        if not isinstance(operator,LatexOperator):
            raise TypeError(f"The 'operator' argument must be a LatexOperator, instead I've received a '{type(operator)}'")

        # Add children:
        # -------------
        self.children.append( (operator,children) )
