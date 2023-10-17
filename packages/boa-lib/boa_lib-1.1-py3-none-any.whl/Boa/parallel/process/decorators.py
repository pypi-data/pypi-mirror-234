"""
This module implements useful multiprocessing decorators.
"""

from typing import Callable, Concatenate, Generic, NoReturn, ParamSpec, TypeVar, overload
from Viper.meta.decorators import Decorator

__all__ = ["background", "daemon"]





T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")

class BackgroundFunction(Decorator, Generic[P, R]):

    """
    This class is used to transform a regular function into a background process function, their code actually gets executed in a Worker process in the default_pool.
    """

    from .pool import default_pool, Pool
    
    def __init__(self, target : Callable[P, R], *, pool : Pool = default_pool) -> None:
        super().__init__(target)
        if not callable(target):
            raise TypeError(f"Expected callable, got '{type(target).__name__}'")
        self.__func = target
        self.__active = False
        self.__default_pool = pool
    
    del default_pool, Pool

    def __eq__(self, value: object) -> bool:
        return value is self or value is self.__func or (isinstance(value, type(self)) and value.__func == self.__func)
    
    def __repr__(self) -> str:
            address = hex(id(self.__func))[2:].upper()
            address = "0x" + ("0" * (16 - len(address))) + address
            return f"<background function {self.__qualname__} at {address}>"

    def __call__(self, *args : P.args, **kwargs : P.kwargs) -> R:
        """
        Implements self(*args, **kwargs). Calls the wrapped function in a background process.
        """
        if self.__active:
            return self.__func(*args, **kwargs)
        return self.__default_pool.apply(self, *args, **kwargs)





class BackgroundMethod(BackgroundFunction[Concatenate[T, P], R], Generic[T, P, R]):

    """
    Just a subclass of BackgroundFunction used for methods.
    """
    
    from types import MethodType as __MethodType
    from .pool import default_pool, Pool

    def __init__(self, target: Callable[Concatenate[T, P], R], *, pool : Pool = default_pool) -> None:
        super().__init__(target, pool=pool)

    del default_pool, Pool

    @overload
    def __get__(self, instance : T, cls : type[T] | None) -> Callable[P, R]:
        ...

    @overload
    def __get__(self, instance : None, cls : type) -> Callable[Concatenate[T, P], R]:
        ...

    def __get__(self, instance : T | None, cls : type[T] | None):
        """
        Implements method access.
        """
        if instance is None:
            return self

        else:
            return BackgroundMethod.__MethodType(self, instance)
        




@overload
def background(target : Callable[Concatenate[T, P], R]) -> BackgroundMethod[T, P, R]:
    ...

@overload
def background(target : Callable[P, R]) -> BackgroundFunction[P, R]:
    ...

def background(target):
    """
    Makes the function be called in a background process in the default pool.
    Note : avoid using this with NoReturn functions as this will forever block one of the pool workers.
    """
    return BackgroundMethod(target)


@overload
def daemon(target : Callable[Concatenate[T, P], NoReturn]) -> BackgroundMethod[T, P, NoReturn]:
    ...

@overload
def daemon(target : Callable[P, NoReturn]) -> BackgroundFunction[P, NoReturn]:
    ...

def daemon(target):
    """
    Makes the function be called in a background process.
    Note : This is meant to be used with NoReturn functions.
    """
    from .pool import Pool
    return BackgroundMethod(target, pool=Pool(1))





del R, P, T, Callable, Concatenate, Generic, NoReturn, ParamSpec, TypeVar, overload, Decorator