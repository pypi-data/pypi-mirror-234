"""
This package contains all the multiprocessing related part of parallel.
"""

from .environment import Environment
from .primitives.process import LocalProcess

from .pool import *
from .primitives import *
from .decorators import *





def current_process() -> LocalProcess:
    """
    Returns the local process object.
    """
    from .primitives.process import LocalProcess
    return LocalProcess()

def current_environment() -> Environment:
    """
    Returns the current process's environement.
    """
    return current_process().environment

del Environment, LocalProcess