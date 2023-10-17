"""
This module adds some useful tools for synchronization accros a multithreaded system.
"""

from types import TracebackType
from typing import Any, Callable, Concatenate, Generic, ParamSpec, TypeVar, overload
from threading import Thread

__all__ = ["PLock", "ExclusionGroup"]





class PLock:

    """
    An Passable Recursive Lock class with a few more functionnalities which allow to transfer the lock to another thread with priority.
    """

    from threading import Lock as __Lock, Thread as __Thread, current_thread as __current_thread
    __current_thread = staticmethod(__current_thread)
    from time import time_ns as __time_ns

    __slots__ = {
        "__lock" : "The base lock used to acquire the RLock",
        "__level" : "The recursion level of the RLock",
        "__owner_thread" : "The thread that currently holds the lock",
        "__pass_lock" : "The lock used to synchronize the passing of the lock to the priority thread",
        "__next_thread" : "A thread that should acquire the lock next with highest priority"
    }

    def __init__(self) -> None:
        self.__lock = self.__Lock()
        self.__level : int = 0
        self.__owner_thread : "Thread | None" = None
        self.__pass_lock = self.__Lock()
        self.__next_thread : "Thread | None" = None
    
    def __repr__(self):
        """
        Implements repr(self).
        """
        s = f"<{type(self).__name__} object at {hex(id(self))}"
        if (t := self.__owner_thread) != None:
            s += f" owned by {t}>"
        else:
            s += " unlocked>"
        return s

    def __enter__(self):
        """
        Implements with self.
        """
        self.acquire()
    
    def __exit__(self, exc_type : type[BaseException], exc : BaseException, traceback : TracebackType):
        """
        Implements with self.
        """
        self.release()
    
    def acquire(self, blocking : bool = True, timeout : float = float("inf")) -> bool:
        """
        Acquires the lock.
        blocking specify if the operation should block until the lock has been acquired or until the optional timeout has been reached.
        Returns True if the lock is held on return, False otherwise.
        """
        if not isinstance(blocking, bool):
            raise TypeError(f"Expected bool, got '{type(blocking).__name__}'")
        try:
            timeout = float(timeout)
        except:
            pass
        if not isinstance(timeout, float):
            raise TypeError(f"Expected float for timeout, got '{type(timeout).__name__}'")
        if timeout < 0:
            raise ValueError(f"Expected positive value for timeout, got {timeout}")
        if self.__owner_thread == self.__current_thread():
            self.__level += 1
            return True
        if timeout == 0:
            blocking = False
        if timeout == float("inf"):
            timeout = -1
        timeout_0 = timeout
        t0 = self.__time_ns()
        while True:
            if not self.__lock.acquire(blocking, timeout):
                return False
            
            timeout = max(timeout_0 - (self.__time_ns() - t0) / 1000000000, -1)
            if timeout < 0 and timeout != -1:
                return False

            next_thread = self.__next_thread
            if next_thread != None and not next_thread.is_alive():  # The prioritized thread has died. Forget about priority.
                next_thread, self.__next_thread = None, None
                self.__pass_lock.release()

            if self.__pass_lock.acquire(False) or next_thread == self.__current_thread():
                if next_thread != None:      # The calling thread received the lock by priority
                    self.__next_thread = None
                self.__pass_lock.release()
                self.__owner_thread = self.__current_thread()
                self.__level = 1
                return True
            
            else:
                self.__lock.release()

            timeout = max(timeout_0 - (self.__time_ns() - t0) / 1000000000, -1)
            if timeout < 0 and timeout != -1:
                return False

    def release(self):
        """
        Lowers the ownership level by one. If it reaches zero, releases the lock so other threads can try acquiering it.
        """
        if self.__owner_thread != self.__current_thread():
            raise RuntimeError("Trying to release un-acquired lock")
        self.__level -= 1
        if self.__level == 0:
            self.__owner_thread = None
            self.__lock.release()

    @property
    def acquired(self) -> bool:
        """
        Returns True if the lock is currently owned by the calling thread.
        """
        return self.__owner_thread == self.__current_thread()

    def pass_on(self, next_thread : Thread):
        """
        Ensures that the next thread to acquire the lock is the one given as argument.
        Make sure that this thread will try to acquire it afterwards, to avoid causing a deadlock.
        """
        if not isinstance(next_thread, self.__Thread):
            raise TypeError(f"Expected Thread, got '{type(next_thread).__name__}'")
        if not self.acquired:
            raise RuntimeError("Cannot pass the lock without acquiering it first")
        self.__pass_lock.acquire()
        self.__next_thread = next_thread





P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")

class ExclusionGroup:

    """
    This class is used to create a mutual exclusion group.
    It is like using a RLock but that can be used as a decorator to make a function (or many) mutually exclusive in regards to anyone using this same function.
    """

    from weakref import ref as __ref
    from threading import RLock as __RLock



    class UnboundInstanceExclusiveMethod(Generic[T, P, R]):

        """
        Subclass (not really) of methods that ensure exclusivity of calls for each instance
        (i.e. you cannot call the same self-exclusive method bound to the same instance from different threads at the same time, one will block until the other returns).
        """
        
        from types import MethodType as __MethodType

        def __init__(self, unbound_method : Callable[Concatenate[T, P], R], group : "ExclusionGroup") -> None:
            self.__func = unbound_method
            self.__group = group
            self.__name__ = unbound_method.__name__

        def __call__(self, instance : T, *args: P.args, **kwargs: P.kwargs) -> R:
            self.__group.acquire(instance = instance)
            try:
                return self.__func(instance, *args, **kwargs)
            finally:
                self.__group.release(instance = instance)
            
        def __repr__(self) -> str:
            address = hex(id(self.__func))[2:].upper()
            address = "0x" + ("0" * (16 - len(address))) + address
            group_address = hex(id(self.__group))[2:].upper()
            group_address = "0x" + ("0" * (16 - len(group_address))) + group_address
            return f"<self-exclusive function {self.__name__} at {address} for group at {group_address}>"

        def __set_name__(self, owner : type[T], name : str):
            self.__name__ = f"{owner.__name__}.{name}"
        
        @overload
        def __get__(self, instance : T, cls : type[T] | None) -> Callable[P, R]:
            ...

        @overload
        def __get__(self, instance : None, cls : type[T]) -> Callable[Concatenate[T, P], R]:
            ...

        def __get__(self, instance : T | None, cls : type[T] | None):
            """
            Implements method access.
            """
            if instance is None:
                
                return self

            else:
                if cls is None:
                    cls = type(instance)
                
                return self.__MethodType(self, instance)
            


    class ExclusiveFunction(Generic[T, P, R]):

        """
        Subclass (not really) of functions that ensure exclusivity of calls.
        (i.e. you cannot call the same exclusive function from different threads at the same time, one will block until the other returns).
        """
        
        from types import MethodType as __MethodType

        def __init__(self, func : Callable[P, R], group : "ExclusionGroup") -> None:
            self.__func = func
            self.__group = group
            self.__name__ = func.__name__

        def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
            self.__group.acquire()
            try:
                return self.__func(*args, **kwargs)
            finally:
                self.__group.release()
            
        def __repr__(self) -> str:
            address = hex(id(self.__func))[2:].upper()
            address = "0x" + ("0" * (16 - len(address))) + address
            group_address = hex(id(self.__group))[2:].upper()
            group_address = "0x" + ("0" * (16 - len(group_address))) + group_address
            return f"<exclusive function {self.__name__} at {address} for group at {group_address}>"

        def __set_name__(self, owner : type[T], name : str):
            self.__name__ = f"{owner.__name__}.{name}"
        
        @overload
        def __get__(self, instance : T, cls : type[T] | None) -> Callable[P, R]:
            ...

        @overload
        def __get__(self, instance : None, cls : type[T]) -> Callable[Concatenate[T, P], R]:
            ...

        def __get__(self, instance : T | None, cls : type[T] | None):
            """
            Implements method access.
            """
            if instance is None:
                
                return self

            else:
                if cls is None:
                    cls = type(instance)
                
                return self.__MethodType(self, instance)



    def __init__(self) -> None:
        self.__instance_dict : "dict[int, ExclusionGroup.__ref[Any]]" = {}
        self.__lock_dict : "dict[int, ExclusionGroup.__RLock]" = {}
        self.__main_lock = ExclusionGroup.__RLock()
        self.__inner_lock = self.__RLock()

    def per_instance(self, unbound_method : Callable[Concatenate[T, P], R]) -> Callable[Concatenate[T, P], R]:
        """
        Decorates a method to be self-exclusive (cannot be called simultaneously on the same instance in different threads).
        """
        from functools import update_wrapper
        if not callable(unbound_method):
            raise TypeError(f"Expected callable, got '{type(unbound_method).__name__}'")
        wrapper = ExclusionGroup.UnboundInstanceExclusiveMethod(unbound_method, self)
        update_wrapper(wrapper, unbound_method)
        return wrapper
    
    def __call__(self, func : Callable[P, R]) -> Callable[P, R]:
        """
        Implements self(func).
        Decorates a function to be exclusive (cannot be called simultaneously in different threads).
        """
        from functools import update_wrapper
        if not callable(func):
            raise TypeError(f"Expected callable, got '{type(func).__name__}'")
        wrapper = ExclusionGroup.ExclusiveFunction(func, self)
        update_wrapper(wrapper, func)
        return wrapper

    def acquire(self, blocking : bool = True, timeout : float = -1, *, instance : T | None = None):
        """
        Acquires the exclusion group. Works exactly like RLock.acquire().
        """
        if instance is None:
            return self.__main_lock.acquire(blocking, timeout)
        with self.__inner_lock:
            n = id(instance)
            if n not in self.__instance_dict or self.__instance_dict[n]() is not instance:
                self.__instance_dict[n] = self.__ref(instance, lambda r : self.__instance_dict.pop(n) and self.__lock_dict.pop(n))
                self.__lock_dict[n] = self.__RLock()
            lock = self.__lock_dict[n]
        return lock.acquire(blocking, timeout)
    
    def release(self, *, instance : T | None = None):
        """
        Releases the exclusion group. Works exactly like RLock.release().
        """
        if instance is None:
            return self.__main_lock.release()
        with self.__inner_lock:
            n = id(instance)
            if n not in self.__instance_dict or self.__instance_dict[n]() is not instance:
                raise RuntimeError("cannot release un-acquired lock")
            lock = self.__lock_dict[n]
        lock.release()





del Any, Callable, Concatenate, Generic, ParamSpec, TypeVar, Thread, TracebackType, P, R, T