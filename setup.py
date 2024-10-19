# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Setup script for the CLI application
# ---------------------------------------------------------
# ./setup.py

from setuptools import setup, find_packages

setup(
    name='txt2latex',
    version='0.1.0',
    description='CLI App for translating texte expression to a LaTeX expresion',
    author='DERAINS Thibaut',
    author_email='thibaut.derains@gmail.com',
    py_modules=['txt2latex'],
    packages=find_packages(),
    install_requires=[],
    entry_points={ 'console_scripts': [
        'txt2latex = txt2latex.scripts.__main__:main',
        ]}
)
