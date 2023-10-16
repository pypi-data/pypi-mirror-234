"""common util"""

__version__ = '0.0.1'

import importlib
import os


def load(package):
    module_dir = os.getcwd() + "/" + package.replace(".", "/")
    for module_file in os.listdir(os.path.abspath(module_dir)):
        if module_file[-3:] == ".py" and module_file != "__init__.py":
            module_name = package + "." + module_file[:-3]
            importlib.import_module(module_name)
