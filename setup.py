# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Setup script for the CLI application
# ---------------------------------------------------------
# ./setup.py

from setuptools import setup, find_packages

# NOTE : for now, the py_utils package is cloned from the dev branch of the reop,
# and will be changed to the master one when it's ready

setup(
    name='txt2latex',
    version='0.1.1',
    description='CLI App for translating texte expression to a LaTeX expresion',
    author='DERAINS Thibaut',
    author_email='thibaut.derains@gmail.com',
    py_modules=['txt2latex'],
    install_requires=[
        'py_utils @ git+https://github.com/Smileyquisourit/py_utils.git@dev'
    ],
    packages=find_packages(),
    entry_points={ 'console_scripts': [
        'txt2latex = txt2latex.scripts.__main__:main',
        ]}
)
