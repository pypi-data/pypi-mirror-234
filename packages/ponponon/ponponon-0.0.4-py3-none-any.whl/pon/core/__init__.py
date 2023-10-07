import sys
import inspect
from typing import List


def get_class_names(module_name: str) -> List[str]:
    __import__(module_name)
    module = sys.modules[module_name]

    return [
        class_name
        for class_name, class_object in
        inspect.getmembers(module, inspect.isclass)
    ]
