"""
This module introduces nephilim threads, which will act like deamons threads, but are aware of the interpreter shutdown.
"""

from collections.abc import Callable, Mapping
from threading import Lock
from typing import Any, ParamSpec
from .deamon import DaemonThread
from atexit import register

__all__ = ["NephilimThread"]





P = ParamSpec("P")

class NephilimThread(DaemonThread):

    """
    NephilimThreads are in between normal Threads and DeamonThreads : they will not prevent interpreter shutdown, but when it happens, they will still be able to execute some actions.
    
    About the apocalypse mechanism:
    
    - It happens at interpreter shutdown (At the time all atexit refistered functions are called).
    - Any started Nephilim will see its fall_callback executed in a DeamonThread that will be awaited.
    - This also takes into account the Nephilims that are started during the apocalypse (even by a fall_calback).
    - Note that even normal Threads started during the apocalypse will not survive it (like DeamonThreads).
    - Once the apocalypse is over (all fall_callbacks have returned and there are no more alive Nephilims), all remaining threads will die and the interpreter shuts down.

    Note that this only works when the interpreter shuts down properly and atexit functions are called (not when it receives SIGKILL for example).
    """

    __starting_lock = Lock()

    def __init__(self, group: None = None, target: Callable[P, Any] | None = None, fall_callback : Callable[["NephilimThread"], None] | None = None, name: str | None = None, args: tuple = (), kwargs: Mapping[str, Any] | None = None) -> None:
        super().__init__(group, target, name, args, kwargs)
        if fall_callback is not None and not callable(fall_callback):
            raise TypeError(f"Expected callable or None for fall__callback, got '{type(fall_callback).__name__}'")
        self.__callback = fall_callback

    def start(self) -> None:
        with self.__starting_lock:      # This lock ensures that no Nephilim can be started when the finilization function is about to return (at which point the lock will never be released).
            return super().start()

    @property
    def fall_callback(self) -> Callable[["NephilimThread"], None] | None:
        """
        The possible callback function that will be called and awaited when the interpreter will shutdown.
        It will be called with the thread itself as argument.
        """
        return self.__callback
    
    @fall_callback.setter
    def fall_callback(self, callback : Callable[["NephilimThread"], None]):
        if not callable(callback):
            raise TypeError(f"Expected callable for callback, got '{type(callback).__name__}'")
        self.__callback = callback
    
    @fall_callback.deleter
    def fall_callback(self):
        self.__callback = None

    @register
    @staticmethod
    def __init_apocalypse():
        """
        Internal function used to warn all remaining NephilimThreads that the interpreter will shutdown.
        It should start all their callbacks in DeamonThreads and wait for them to finish.
        Note that if a NephilimThread is started while the apocalypse is happening, their callback will be (almost) imediately called.
        """
        from threading import enumerate
        from .deamon import DaemonThread
        from time import sleep

        callbacks : list[DaemonThread] = []
        finalized : set[NephilimThread] = set()

        def get_remaining_nephilims() -> list[NephilimThread]:
            """
            Returns the list of NephilimThreads that have yet to be finalized.
            """
            return list(t for t in enumerate() if isinstance(t, NephilimThread) and t.is_alive() and t not in finalized)

        NephilimThread.__starting_lock.acquire()
        remaining = get_remaining_nephilims()
        while remaining or callbacks:
            NephilimThread.__starting_lock.release()
            for nephilim in remaining:
                d = DaemonThread(target = nephilim.fall_callback, args = (nephilim, ), name = f"Callback of Nephilim with TID #{nephilim.ident}")
                d.start()
                callbacks.append(d)
                finalized.add(nephilim)
            
            for cb in callbacks.copy():
                if not cb.is_alive():
                    callbacks.remove(cb)
            
            NephilimThread.__starting_lock.acquire()
            remaining = get_remaining_nephilims()
            if not remaining:
                sleep(0.001)

    del __init_apocalypse





del P, Callable, Mapping, Any, ParamSpec, DaemonThread, register, Lock