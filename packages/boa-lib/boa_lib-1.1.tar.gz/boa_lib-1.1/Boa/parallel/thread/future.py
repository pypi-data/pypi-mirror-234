"""
This module declares the multithreading version of Futures.
"""

from typing import Callable, Generic, Iterable, TypeVar

from ..abc import Future as AbstractFuture

__all__ = ["Future"]





T = TypeVar("T")

set_type = set

class Future(AbstractFuture[T]):
    
    """
    The multithreading version of Futures. Use a Future to wait for a future object to come.
    """

    from threading import Event as __Event, RLock as __RLock
    from ..exceptions import (
        CancelledFuture as __CancelledFuture,
        TooFarFutureError as __TooFarFutureError,
        FutureSetError as __FutureSetError,
        FutureUnsetError as __FutureUnsetError
        )
    from ...parallel import logger as __logger
    
    __slots__ = {
        "__value" : "The currently set value of the Future (if any).",
        "__exception" : "The currently set exception of the Future (if any).",
        "__lock" : "A lock used by Future's methods to keep it in a coherent state.",
        "__waiting" : "The number of calls to wait() and result() waiting for the Future.",
        "__collapsed" : "An event indicating if the Future can be cleared once it has been set.",
        "__callbacks" : "A list of functions to call when the Future is set.",
        "__event" : "The event that handles the behavior of the Future."
    }

    def __init__(self) -> None:
        super().__init__()
        self.__value : "T"
        self.__exception : BaseException | None = None
        self.__lock = self.__RLock()
        self.__waiting : int = 0
        self.__collapsed = self.__Event()
        self.__collapsed.set()
        self.__callbacks : "list[Callable[[Future[T]], None]]" = []
        self.__event = self.__Event()

    def set(self, value : T) -> None:
        self.__set(value)

    def __set(self, value : T, propagation_state : set_type["Future[T]"] | None = None):
        if propagation_state is None:
            propagation_state = {self}
        self.__logger.debug(f"Setting {self} to {value}")
        to_do : "Iterable[Future[T]]" = (fut for fut in self.linked() if fut not in propagation_state)

        with self.__lock:
            if self.is_set:
                raise self.__FutureSetError(self, "Future is already set")
            self.__value = value
            if self.__waiting:
                self.__collapsed.clear()
            self.__event.set()

            excs_1 : list[BaseException] = []
            for cb in self.__callbacks:
                try:
                    cb(self)
                except BaseException as e:
                    excs_1.append(e)

            excs_2 : list[BaseException] = []
            for fut in to_do:
                try:
                    propagation_state.add(fut)
                    fut.__set(value, propagation_state)
                except BaseException as e:
                    excs_2.append(e)

            if excs_1:
                exc_1 = BaseExceptionGroup(f"{'An exception' if len(excs_1) == 1 else 'Some exceptions'} occured while calling Future callbacks", excs_1)
            else:
                exc_1 = None
            
            if excs_2:
                exc_2 = BaseExceptionGroup(f"{'An exception' if len(excs_2) == 1 else 'Some exceptions'} occured while propagating causality to linked Futures", excs_2)
            else:
                exc_2 = None
            if exc_1 and exc_2:
                raise BaseExceptionGroup("Exceptions occured both while calling Future callbacks and propagating causality to linked Futures", (exc_1, exc_2))
            elif exc_1:
                raise exc_1
            elif exc_2:
                raise exc_2
    
    @property
    def is_set(self) -> bool:
        return self.__event.is_set()
    
    @AbstractFuture.exception.getter
    def exception(self) -> BaseException | None:
        with self.__lock:
            if not self.is_set:
                raise self.__FutureUnsetError(self, "Future has not been set yet")
            return self.__exception
    
    @AbstractFuture.value.getter
    def value(self) -> T | None:
        with self.__lock:
            if not self.is_set:
                raise self.__FutureUnsetError(self, "Future has not been set yet")
            try:
                return self.__value
            except AttributeError:
                return None
    
    @AbstractFuture.cancelled.getter
    def cancelled(self) -> bool:
        with self.__lock:
            return self.is_set and isinstance(self.exception, self.__CancelledFuture)
    
    def set_exception(self, exc : BaseException) -> None:
        self.__set_exception(exc)
    
    def __set_exception(self, exc : BaseException, propagation_state : set_type["Future[T]"] | None = None):
        if not isinstance(exc, BaseException):
            raise TypeError("Expected BaseException, got " + repr(type(exc).__name__))
        if propagation_state is None:
            propagation_state = {self}
        if isinstance(exc, self.__CancelledFuture):
            self.__logger.info(f"Cancelling {self}")
        else:
            self.__logger.info(f"Raising {exc} from {self}")
        to_do : "Iterable[Future[T]]" = (fut for fut in self.linked() if fut not in propagation_state)
        
        with self.__lock:
            if self.is_set:
                raise self.__FutureSetError(self, "Future is already set")
            self.__exception = exc
            if self.__waiting:
                self.__collapsed.clear()
            self.__event.set()
            excs_1 : list[BaseException] = []
            for cb in self.__callbacks:
                try:
                    cb(self)
                except BaseException as e:
                    excs_1.append(e)

            excs_2 : list[BaseException] = []
            for fut in to_do:
                try:
                    propagation_state.add(fut)
                    fut.__set_exception(exc, propagation_state)
                except BaseException as e:
                    excs_2.append(e)

            if excs_1:
                exc_1 = BaseExceptionGroup(f"{'An exception' if len(excs_1) == 1 else 'Some exceptions'} occured while calling Future callbacks", excs_1)
            else:
                exc_1 = None
            
            if excs_2:
                exc_2 = BaseExceptionGroup(f"{'An exception' if len(excs_2) == 1 else 'Some exceptions'} occured while propagating causality to linked Futures", excs_2)
            else:
                exc_2 = None
            if exc_1 and exc_2:
                raise BaseExceptionGroup("Exceptions occured both while calling Future callbacks and propagating causality to linked Futures", (exc_1, exc_2))
            elif exc_1:
                raise exc_1
            elif exc_2:
                raise exc_2
        
    def add_callback(self, cb : Callable[["Future[T]"], None]):
        with self.__lock:
            self.__logger.debug(f"Adding {cb} to {self}'s callbacks")
            self.__callbacks.append(cb)
            if self.__event.is_set():
                cb(self)
    
    def remove_callback(self, cb : Callable[["Future[T]"], None]):
        with self.__lock:
            while cb in self.__callbacks:
                self.__callbacks.remove(cb)
    
    def clear(self) -> None:
        self.__clear()
    
    def __clear(self, propagation_state : set_type["Future[T]"] | None = None):
        if not self.__collapsed.is_set():
            self.__collapsed.wait()
        if propagation_state is None:
            propagation_state = {self}
        self.__logger.debug(f"Clearing {self}")
        to_do : "Iterable[Future[T]]" = (fut for fut in self.linked() if fut not in propagation_state)

        with self.__lock:
            if not self.__event.is_set():
                return
            self.__collapsed.wait()
            try:
                del self.__value
            except AttributeError:
                pass
            self.__exception = None
            self.__event.clear()

            for fut in to_do:
                propagation_state.add(fut)
                fut.__clear(propagation_state)
    
    def wait(self, timeout : float = float("inf")) -> bool:
        try:
            timeout = float(timeout)
        except:
            pass
        if not isinstance(timeout, float):
            raise TypeError("Expected float for timeout, got " + repr(type(timeout).__name__))
        if timeout < 0 or timeout == float("nan"):
            raise ValueError("Expected positive timeout, got " + repr(timeout))
        try:
            with self.__lock:
                self.__waiting += 1
            return self.__event.wait(timeout if timeout != float("inf") else None)
        finally:
            with self.__lock:
                self.__waiting -= 1
                if not self.__waiting:
                    self.__collapsed.set()
    
    def result(self, timeout : float = float("inf")) -> T:
        try:
            timeout = float(timeout)
        except:
            pass
        if not isinstance(timeout, float):
            raise TypeError("Expected float for timeout, got " + repr(type(timeout).__name__))
        if timeout < 0 or timeout == float("nan"):
            raise ValueError("Expected positive timeout, got " + repr(timeout))
        try:
            with self.__lock:
                self.__waiting += 1
            ok = self.wait(timeout)
            if not ok:
                raise self.__TooFarFutureError(self, "Future has not been resolved yet")
            if not self.__exception:
                return self.__value
            else:
                raise self.__exception from None
        finally:
            with self.__lock:
                self.__waiting -= 1
                if not self.__waiting:
                    self.__collapsed.set()





del T, Callable, Iterable, TypeVar, Generic, AbstractFuture, set_type