# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Definition of Logical Component
# ---------------------------------------------------------
# ./src/baseComponent/logicalComponent.py

"""Set of functions and classes for representing an expression.

This module contains functions and classes that allow translating an
expression into a set of logical blocks.
These logical blocks are currently only determined based on the
formatting of Matlab symbolic expressions.
"""

from typing import Union, Optional

class LogicalElement():
    """Class representing a logical element.

    An instance of this class represents a simple logical element, i.e. without
    other groups (content enclosed in parentheses).
    """
    def __init__(self,expr:str) -> None:

        # Type checking:
        # --------------
        if not isinstance(expr,str):
            raise TypeError(f"The 'expr' argument must be a string, instead I've received a '{type(expr)}'")

        # Initialize instance:
        # --------------------
        if '(' in expr or ')' in expr:
            raise ValueError(f"Expression shall not contains the following caracters. '(' or ')'. I received {expr}")
        
        self.contents:str = expr
    
    def __eq__(self,other:'LogicalElement') -> bool:

        # Test Class:
        if not isinstance(other,LogicalElement):
            return False
        
        # Test contents:
        return self.contents == other.contents
    def __str__(self) -> str:
        return f"E'{self.contents}'"


class LogicalBlock():
    """Class representing a logical block.

    An instance of this class allows representing a logical block. A
    logical block has children, which can themselves be logical blocks
    or logical content (i.e. a group of characters that does not contain any
    other nested parentheses).
    
    An instance also allows storing metadata (a dictionary containing key-value pairs
    defined by the user) and the delimiter that surrounds the logical block (under development).
    """

    def __init__(self, **metadatas:dict) -> None:
        self.children:list[Union['LogicalBlock',LogicalElement]] = list()
        self._metadata:dict[any:any] = metadatas

    def __eq__(self, other:'LogicalBlock') -> bool:
        
        # Test class:
        if not isinstance(other,LogicalBlock):
            return False
        
        # Test len of children:
        if len(self.children) != len(other.children):
            return False
        
        # Test children:
        for child1,child2 in zip(self.children,other.children):
            if child1 != child2:
                return False
            
        return True
    def __str__(self) -> str:
        s = "Block( "
        for child in self.children:
            s += str(child)
        s += " )"
        return s

    def add_children(self,children:Union[LogicalElement,'LogicalBlock']) -> None:

        # Type check:
        # -----------
        if not isinstance(children, (LogicalElement,LogicalBlock)):
            raise TypeError(f"The argument 'children' must be a LatexContents or an other LogicalBlock, instead I've received '{type(children)}'")
        
        # Add children:
        # -------------
        self.children.append(children)

    def set_metadata(self, key:str, value:any) -> None:
        """ Set a metadata. """

        # Type checking:
        # --------------
        if not isinstance(key,str):
            raise TypeError(f"The 'key' argument must be a string, instead I've received '{type(key)}'")

        # Add metadata:
        # -------------
        self._metadata[key] = value
    def get_metadata(self, key:str, default:Optional[any]=None) -> any:
        """ Get a metadata """

        # Type checking:
        # --------------
        if not isinstance(key,str):
            raise TypeError(f"The argument 'key' must be a string, instead I've received '{type(key)}'")
        
        # Get metadata:
        # -------------
        return self._metadata.get(key,default=default)