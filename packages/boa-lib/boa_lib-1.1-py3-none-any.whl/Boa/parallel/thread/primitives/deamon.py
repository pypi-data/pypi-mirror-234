"""
This module contains a separate class for daemonic threads.
"""

from collections.abc import Callable, Mapping
from threading import Thread
from typing import Any, ParamSpec

__all__ = ["DaemonThread"]





P = ParamSpec("P")

class DaemonThread(Thread):

    """
    Subclass of Thread that is always daemonic.
    """

    def __init__(self, group: None = None, target: Callable[P, Any] | None = None, name: str | None = None, args: tuple = (), kwargs: Mapping[str, Any] | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=True)
    
    def isDaemon(self) -> bool:
        return True
    
    def setDaemon(self, daemonic: bool) -> None:
        raise ValueError("Cannot change the daemon flag for DaemonThreads.")
    




del P, Callable, Mapping, Thread, Any, ParamSpec