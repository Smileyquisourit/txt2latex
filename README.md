 # txt2latex

This is a Python library for parsing mathematical expressions and converting them to LaTeX format. The library provides classes for representing mathematical expressions and LaTeX elements, as well as a parser for converting mathematical expressions to LaTeX.
This library was primarily developed to translate symbolic expressions obtained from symbolic expression with MATLAB, but it can be adapted to translate other expressions as well.


## Features

- **Translate a simple text expression to a latex expression**
- **Translate multiple text expression to a latex expression in an array** (under development)


## Table of Contents

- [txt2latex](#txt2latex)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Use it directly in the command windows:](#use-it-directly-in-the-command-windows)
    - [Use it in a script:](#use-it-in-a-script)
  - [Code organization](#code-organization)
  - [Contributing](#contributing)



## Installation

To install the library, clone the repository and install it:

```bash
git clone https://github.com/yourusername/latex-expression-parser.git
cd latex-expression-parser
pip install .
```

If you want to install it and still be able to change the source code without
re-installing it after each modification, change the last command to the following:
```bash
pip install -e .
```

## Usage

Their is multiple ways to use this librairy, depending on the use case. You can either:

### Use it directly in the command windows:
You can use it directly in the command windows:
```bash
txt2latex translate --help
```
Or as a python module:
```bash
python -m txt2latex --help
```

### Use it in a script:
You can import it in a python script and use it's functionality
```python
expression = r"a + (p^2 + 2*omega*(b - c))*(p^3 - (a*p^2)*(c - d) - a)"

from txt2latex import parsers
logic_expr = parsers.parse_txt_expression(expression)
latex_expr = parsers.parse_logical_expression(logic_expr)
print(latex_expr)
```


## Code organization

The application is a module in itself, but contains different submodule and sub-directory. These main components are:
- `scripts/`: A sub-directory containing the scripts used for the principals functionality of the module. It contains the following scripts:
  - `translate.py`: translate an expression
  - `tests.py`: execute the tests
  - `operator.py`: handles the operators used for the translation (under developpment)
- `src/`: A sub-directory containing the source code of the application. It contain the following submodule:
  - `baseComponents`: containing the class definitions of the main class used by the application
  - `parsers`: containing the function used for parsing expressions (under development)
  - `configParser`: containing a helper class representing a config file (under development)
  - `logueur`: containg a helper class for logging message to the console (under development)


## Contributing
Contributions are welcome! If you find a bug or have a feature request, please open an issue on the GitHub repository. If you would like to contribute code, please fork the repository and submit a pull request.