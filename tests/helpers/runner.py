#!/usr/bin/env python3
import unittest


def run_tests(tests=list()):
    loader = unittest.TestLoader()
    test_runner = unittest.TextTestRunner()
    for test in tests:
        test_runner.run(loader.loadTestsFromTestCase(test))
