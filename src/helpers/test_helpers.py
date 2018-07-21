#!/usr/bin/env python3
import uuid


def assert_all(assertions, context):
    success_count = 0
    for a in assertions:
        if not a[0](*a[1:]):
            success_count += 1
            print(
                "...{0} - {1}({2})- success".format(
                    context,
                    a[0].__name__,
                    [x.__name__ if not (type(x) == str or type(x) == uuid.UUID) else x for x in a[1:]]
                )
            )
        else:
            print(
                "...{0} - {1}({2}) - failed".format(
                    context,
                    a[0].__name__,
                    [x.__name__ if not (type(x) == str or type(x) == uuid.UUID) else x for x in a[1:]]
                )
            )
    return success_count
