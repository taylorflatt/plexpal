#!/usr/bin/env python3
import uuid
import json
from src.helpers.errors import get_exception


def assert_all(assertions, context):
    success_count = 0
    print("\n   [{0}...\n".format(context))
    for a in assertions:
        try:
            a[0](*a[1:])
            success_count += 1
            print(
                "   ...{0}({1})- SUCCESS".format(
                    a[0].__name__,
                    [x.__name__ if (hasattr(x,
                                            "__name__")) else x for x in a[1:]]
                )
            )
        except AssertionError as ae:
            print(
                "   ...{0}({1}) - FAIL\n    ]".format(
                    a[0].__name__,
                    [x.__name__ if (hasattr(x,
                                            "__name__")) else x for x in a[1:]]
                )
            )
            raise ae
        except:
            print(
                "   ...{0}({1}) - FAIL\n    ]".format(
                    a[0].__name__,
                    [x.__name__ if (hasattr(x,
                                            "__name__")) else x for x in a[1:]]
                )
            )
            raise AssertionError(get_exception(trace=True, text=True))
    print("\n   {0} {1}]".format(context, success_count))
    return success_count
