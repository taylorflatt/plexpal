#!/usr/bin/env python3
import os
import src.helpers.errors

for module in os.listdir(os.path.dirname(__file__)):
    try:
        if module == "__init__.py" or module[-3:] != ".py":
            continue
        _temp = __import__(module[:-3], globals(), locals())
    except Exception:
        pass  #print(get_exception(trace=True))
