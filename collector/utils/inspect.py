import pathlib
import sys


def get_running_module_path() -> pathlib.Path:
    """
    gives the running python module path
    ex.: if `python -m collector` was run, gives 'collector' directory path
    ex.: if `python collector.py` was run, gives 'collector.py' script path
    :return:
    """
    path = pathlib.Path(sys.modules['__main__'].__file__)
    if path.name == "__main__.py":
        path = path.parent
    return path
