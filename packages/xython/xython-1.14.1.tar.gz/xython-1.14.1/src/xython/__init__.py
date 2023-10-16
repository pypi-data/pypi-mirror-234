# __init__.py
# Copyright (C) 2023 (sjpkorea@yahoo.com) and contributors
#

import inspect
import os
import sys

__version__ = '1.14.1'
real_path = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
sys.path.append(real_path)

try:
    import xython

except ImportError as e:
    print(e," Please re-check.")
    exit(1)

__all__ = [name for name, obj in locals().items()
    if not (name.startswith('_') or inspect.ismodule(obj))]