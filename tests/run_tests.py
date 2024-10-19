# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Script for starting test process
# ---------------------------------------------------------
# ./tests/run_tests.py

""" Script for starting test process

Each script in the tests directory that start with 'test_' contains
the definition of test class testing the code of a module. Each script
are considered as a test suite, and the present script contains function
for setting up the tests and running it.

As for the version 0.1.0, this is script is still in progress !!
"""

import unittest

def run_all():
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    runner = unittest.TextTestRunner()
    print("Starting test...\n")
    runner.run(suite)

#TODO
def run_specific_tests(test_suite_names):
    loader = unittest.TestLoader()
    suites_list = []
    for test_suite_name in test_suite_names:
        suite = loader.loadTestsFromName(test_suite_name)
        suites_list.append(suite)
    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()
    runner.run(big_suite)