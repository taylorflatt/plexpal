#!/usr/bin/env python3
import sys, inspect

test_context = lambda: inspect.stack()[1][3]


def class_context(obj):
    return type(obj).__name__
