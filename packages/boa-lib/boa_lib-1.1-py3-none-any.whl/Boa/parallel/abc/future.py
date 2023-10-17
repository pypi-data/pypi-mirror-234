"""
This module sets up the abstract Future system.
Find its implementations in other Boa.parallel packages.
"""

from abc import ABCMeta, abstractmethod
from threading import RLock
from typing import Callable, Generic, Iterator, TypeVar
from weakref import WeakSet

__all__ = ["Future"]





T = TypeVar("T")

class Future(Generic[T], metaclass = ABCMeta):

    """
    A Future represents an eventual value. This value might get defined at some point but it can also be set to raise an exception.
    You can wait for it like an Event. Contrary to an Event, you cannot set it twice without clearing it (raises FutureSetError).
    To avoid waiting forever, it is good to raise an UnreachableFuture exception when you know a Future will never come.
    """

    from threading import RLock as __RLock
    from weakref import WeakSet as __WeakSet

    from ..exceptions import CancelledFuture as __CancelledFuture, FutureSetError as __FutureSetError
    from ...parallel import logger as __logger

    __slots__ = {
        "__name" : "The eventual name given to that Future.",
        "__linked" : "The set of Futures directly linked to this particular Future.",
        "__group" : "The set of Futures linked directly or not to this particular Future.",
        "__group_lock" : "A lock used to iterate over the group of causally equivalent Futures.",
        "__weakref__" : "A placeholder for weak references.",
        "__cancel_on_del" : "A boolean indicating if the Future should be cancelled first if not set upon deletion."
    }

    __linking_lock = __RLock()

    def __init__(self, *, name : str | None = None):
        if name is not None and not isinstance(name, str):
            raise TypeError(f"Expected str or None for name, got '{type(name).__name__}'")
        self.__name = name
        self.__linked : "WeakSet[Future[T]]" = Future.__WeakSet()
        self.__group : "WeakSet[Future[T]]" = Future.__WeakSet((self, ))
        self.__group_lock = self.__RLock()
        self.__cancel_on_del : bool = False
        self.__logger.debug("Initializing new Future")

    # def acquire(self, blocking : bool = True, timeout : float = float("inf")):

    
    @property
    def name(self) -> str | None:
        """
        The name given to this Future. This is intended for debugging purpuses.
        """
        return self.__name
    
    @name.setter
    def name(self, value : str | None):
        if value is not None and not isinstance(value, str):
            raise TypeError(f"Expected str or None for name, got '{type(value).__name__}'")
        self.__logger.debug(f"Changing name of {self} to '{value}'")
        self.__name = value

    @name.deleter
    def name(self):
        self.__logger.debug(f"Changing name of {self} to None")
        self.__name = None

    @property
    def cancel_on_del(self) -> bool:
        """
        If this value is True, the Future will be cancelled (if not already set) when its destructor is invoked.
        """
        return self.__cancel_on_del
    
    @cancel_on_del.setter
    def cancel_on_del(self, value : bool):
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got '{type(value).__name__}'")
        self.__cancel_on_del = value

    def __repr__(self) -> str:
        """
        Implements repr(self).
        """
        if self.name is not None:
            return f"<{type(self).__name__} '{self.name}': {('cancelled' if self.cancelled else 'errored' if self.exception is not None else 'set') if self.is_set else 'unset'}>"
        else:
            address = hex(id(self))[2:].upper()
            address = "0x" + "0" * (16 - len(address)) + address
            return f"<{type(self).__name__} at {address}: {('cancelled' if self.cancelled else 'errored' if self.exception is not None else 'set') if self.is_set else 'unset'}>"

    @abstractmethod
    def set(self, value : T) -> None:
        """
        Sets the value of the Future. The Future must not be already set.
        It may raise ExceptionGroups if errors occur while propagating causality.
        """
        raise NotImplementedError

    @abstractmethod
    def set_exception(self, exc : BaseException) -> None:
        """
        Makes the Future raise an exception. The Future must not be already set.
        It may raise ExceptionGroups if errors occur while propagating causality.
        """
        raise NotImplementedError
    
    @property
    @abstractmethod
    def is_set(self) -> bool:
        """
        Indicates if the Future has been set.
        """
        raise NotImplementedError
    
    @property
    @abstractmethod
    def value(self) -> T | None:
        """
        The current value of the Future.
        Raises FutureUnsetError if the Future is not set.
        Returns None if the Future had an exception.
        """
        raise NotImplementedError
        
    @value.setter
    def value(self, value : T):
        """
        Sets the Future to a value. Equivalent to self.set(value).
        """
        self.set(value)

    @value.deleter
    def value(self):
        """
        Resets the Future. Equivalent to self.clear().
        """
        self.clear()
    
    @property
    @abstractmethod
    def exception(self) -> BaseException | None:
        """
        The current exception raised by the Future.
        Raises FutureUnsetError if the Future is not set.
        Returns None if the Future did not have an exception.
        """
        raise NotImplementedError
        
    @exception.setter
    def exception(self, value : BaseException):
        """
        Sets the exception of the Future. Equivalent to self.set_exception(value).
        """
        if not isinstance(value, BaseException):
            raise TypeError(f"Expected BaseException, got '{type(value).__name__}'")
        self.set_exception(value)
    
    @exception.deleter
    def exception(self):
        """
        Resets the Future. Equivalent to self.clear().
        """
        self.clear()

    @property
    @abstractmethod
    def cancelled(self) -> bool:
        """
        Indicates if the Future has been cancelled.
        """
        raise NotImplementedError
    
    @cancelled.setter
    def cancelled(self, value : bool):
        """
        Sets the cancel state of the Future.
        Setting to True is equivalent to self.cancel().
        Setting to False is equivalent to self.clear().
        """
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got '{type(value).__name__}'")
        if value:
            self.cancel()
        else:
            self.clear()

    @abstractmethod
    def add_callback(self, cb : Callable[["Future[T]"], None]):
        """
        Adds a callback for the realization of the Future. It will be called with the Future object as argument each time it realizes or there is an exception.
        Note that adding a callback when the Future is already set will cause it to be called immediately.
        """
        raise NotImplementedError

    @abstractmethod
    def remove_callback(self, cb : Callable[["Future[T]"], None]):
        """
        Removes all instances of the given callback.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """
        Clears the Future. Removes the associated value and exception.
        """
        raise NotImplementedError

    @abstractmethod
    def wait(self, timeout : float = float("inf")) -> bool:
        """
        Waits for the realization of the Future. Returns a boolean indicating if the Future has been realized.
        If the timeout is given, waits at most for this timeout and returns.
        """
        raise NotImplementedError

    @abstractmethod
    def result(self, timeout : float = float("inf")) -> T:
        """
        Waits for the Future to be resolved and returns the associated value.
        Raises TooFarFutureError if the future has not been resolved before timeout has been reached.
        """
        raise NotImplementedError

    def link(self, cause_or_effect : "Future[T]"):
        """
        Links this Future to another. When the other Future realizes, this one will be realized in an identical way and vice-versa.
        Silently does nothing if they were linked.
        If cause_or_effect or self is not set, sets the other to the same result or exception.
        Raises FutureSetError if both Futures were set to different values/exceptions.
        """
        if not isinstance(cause_or_effect, type(self)):
            raise TypeError(f"Expected '{type(self).__name__}', got '{type(cause_or_effect).__name__}'")

        with self.__linking_lock, self.__group_lock, cause_or_effect.__group_lock:

            if cause_or_effect.is_set != self.is_set:
                if self.is_set:
                    try:
                        cause_or_effect.set(self.result())
                    except BaseException as e:
                        cause_or_effect.set_exception(e)
                else:
                    try:
                        self.set(cause_or_effect.result())
                    except BaseException as e:
                        self.set_exception(e)
            elif cause_or_effect.is_set and self.is_set:
                if cause_or_effect.exception != self.exception or cause_or_effect.value != self.value:
                    raise Future.__FutureSetError("Linking Futures set to different states.")
            
            self.__logger.debug(f"Linking {self} and {cause_or_effect}")

            self.__linked.add(cause_or_effect)
            cause_or_effect.__linked.add(self)

            if self.__group is cause_or_effect.__group:
                return

            g = self.__group | cause_or_effect.__group
            l = self.__group_lock

            for fut in g:
                fut.__group = g
                fut.__group_lock = l

            self.__logger.info(f"Merged a group of Futures : {list(g)}")

    def unlink(self, cause_or_effect : "Future[T]"):
        """
        Unlinks this Future from another.
        Silently does nothing if they were not linked.
        """
        if not isinstance(cause_or_effect, type(self)):
            raise TypeError(f"Expected '{type(self).__name__}', got '{type(cause_or_effect).__name__}'")
        
        def explore(fut : "Future[T]") -> "WeakSet[Future[T]]":
            """
            Internal function used to find all the Futures causally connected to a starting Future.
            """
            s = self.__WeakSet({fut})
            new = self.__WeakSet({fut})
            while new:
                new = self.__WeakSet().union(*[f.__linked for f in new]) - s
                s |= new
            return s

        with self.__linking_lock, self.__group_lock, cause_or_effect.__group_lock:

            if self.__group is not cause_or_effect.__group:
                return
            
            self.__logger.debug(f"Unlinking {self} and {cause_or_effect}")
            
            self.__linked.discard(cause_or_effect)
            cause_or_effect.__linked.discard(self)

            old_group = self.__group
            # old_group.add(self)     # Some weird stuff might happen at destruction...
            g1 = explore(self)
            if len(g1) != len(old_group):       # Then we just cut a group in two subgroups
                g2 = explore(cause_or_effect)
                new_lock = self.__RLock()
                
                if len(g1) > len(g2):           # Change the smallest group
                    for fut in g2:
                        fut.__group = g2
                        fut.__group_lock = new_lock
                    old_group -= g2
                    self.__logger.info(f"Splitting Future groups : {list(old_group)} and {list(g2)}")
                else:
                    for fut in g1:
                        fut.__group = g1
                        fut.__group_lock = new_lock
                    old_group -= g1
                    self.__logger.info(f"Splitting Future groups : {list(g1)} and {list(old_group)}")

    def linked(self) -> "Iterator[Future[T]]":
        """
        Iterates over all the linked Futures. While iterating, a lock is held, preventing iterating simultenously from another Future linked (directly or not) to this one.
        """

        def get_lock(fut : "Future") -> "RLock":
            """
            Just returns the private __group_lock.
            """
            return fut.__group_lock
        
        class LockedIter:

            """
            Internal classs used to keep a lock on a group while iterating of a Future's direct neighbors.
            """

            def __init__(self, fut : "Future[T]", s : "set[Future[T]]") -> None:
                while True:
                    lock = get_lock(fut)
                    lock.acquire()
                    if get_lock(fut) == lock:
                        break
                    lock.release()
                self.__lock = lock
                self.__iter = iter(s.copy())
            
            def __iter__(self):
                """
                Implements iter(self).
                """
                return self
            
            def __next__(self):
                """
                Implements next(self).
                """
                return next(self.__iter)
            
            def __del__(self):
                """
                Implements del self.
                """
                try:
                    self.__lock.release()
                except RuntimeError:
                    pass            # For some reasons, it was not always acquired...


        return LockedIter(self, set(self.__linked))
    
    def __del__(self):
        """
        Implements del self.
        """
        self.__logger.debug(f"Deleting {self}")
        if self.cancel_on_del:
            with self.__group_lock:
                if not self.is_set:
                    self.__logger.info(f"Cancelling {self} because of destruction")
                    self.cancel()
        with self.__group_lock:
            while self.__linked:
                try:
                    f = next(iter(self.__linked))
                    self.unlink(f)
                except StopIteration:
                    return
                except:
                    pass

    def cancel(self):
        """
        Cancels the execution of the task by raising CancelledFuture.
        """
        self.set_exception(self.__CancelledFuture(self, "Task cancelled"))





del ABCMeta, abstractmethod, RLock, Callable, Generic, Iterator, TypeVar, WeakSet