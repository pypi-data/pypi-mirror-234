"""
This module defines some environment objects to be used in the the parallel module.
"""

from typing import Any, Callable, Iterable, SupportsIndex, SupportsBytes, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .primitives import Process

__all__ = ["local_env"]





class EnvDict(TypedDict):

    authkey : bytes
    daemon : bool




class Environment:

    """
    Just a class to hold some data specific to this process.
    """

    __slots__ = {
        "__authkey" : "The authentication key that the process (and its children) can use to communicate.",
        "__daemon" : "A boolean indicating if this process is a daemon process.",
        "__processes" : "The processes that this environment is affected to.",
        "__callbacks" : "A list of functions to call when the environment changes."
    }

    class SecureString(bytes):

        """
        Just a subclass of bytes that forbids pickling.
        """

        def __reduce__(self) -> str | tuple[Any, ...]:
            from Viper.pickle_utils import ForbiddenPickleError
            raise ForbiddenPickleError("Cannot pickle a SecureString")

    def __init__(self) -> None:
        from os import urandom
        from typing import TYPE_CHECKING, Callable
        if TYPE_CHECKING:
            from .primitives.process import Process
        from weakref import WeakSet
        self.__authkey = urandom(64)
        self.__processes : WeakSet[Process] = WeakSet()
        self.__daemon : bool = False
        self.__callbacks : list[Callable[["Environment"], None]] = []

    def __signal_change(self):
        """
        Internal function called when a variable changes which signals the change.
        """
        self.__update_processes()

    def __call_callbacks(self):
        """
        Internal function that call all callbacks waiting for a change in the environment.
        """
        exceptions : list[BaseException] = []
        for cb in self.__callbacks:
            try:
                cb(self)
            except BaseException as e:
                exceptions.append(e)
        if exceptions:
            if len(exceptions) == 1:
                raise RuntimeError("Got an exception while calling Environment change callbacks") from exceptions[0]
            else:
                raise RuntimeError("Got multiple exceptions while calling Environment change callbacks") from BaseExceptionGroup("The callback exceptions are the floowing:", exceptions)

    def __update_processes(self):
        """
        Internal function used to force an environment update in process that this environment object represent.
        """
        for p in set(self.__processes):
            p.environment = self

    def __getstate__(self) -> object:
        from Viper.pickle_utils import ForbiddenPickleError
        raise ForbiddenPickleError("Cannot pickle environment object")

    @staticmethod
    def expanded_keys() -> list[str]:
        """
        Returns the list of names that process objects will be able to access directly.
        """
        return ["authkey", "daemon"]

    def register(self, p : "Process"):
        """
        Registers the environment to a new process.
        """
        self.__processes.add(p)

    def unregister(self, p : "Process"):
        """
        Unregisters the environment from a process.
        """
        self.__processes.discard(p)

    def add_callback(self, cb : Callable[["Environment"], None]):
        """
        Adds a callback to be performed when a variable is changed.
        It will be called with the updated Environment object. 
        """
        if not callable(cb):
            raise TypeError(f"Expected callable, got '{type(cb).__name__}'")
        self.__callbacks.append(cb)

    def remove_callback(self, cb : Callable[["Environment"], None]):
        """
        Removes a callback that should have been performed when a variable is changed.
        Silently does nothing if it was not registered.
        """
        if not callable(cb):
            raise TypeError(f"Expected callable, got '{type(cb).__name__}'")
        while cb in self.__callbacks:
            self.__callbacks.remove(cb)

    def update(self):
        """
        Updates the environment in registered processes.
        """
        for p in self.__processes:
            p.environment = self

    def copy_from(self, other : EnvDict):
        """
        Copies the content of another environment into this one.
        """
        if not isinstance(other, dict):
            raise TypeError(f"Expected Environment, got '{type(other).__name__}'")
        
        self.__authkey = other["authkey"]
        self.__daemon = other["daemon"]

        self.__call_callbacks()

    def export(self) -> EnvDict:
        """
        Exports the evironment into a dictionnary.
        """
        return {
            "authkey" : self.__authkey,
            "daemon" : self.__daemon
        }

    @property
    def authkey(self) -> SecureString:
        """
        The authentication key that this process will use for authentication with its children.
        """
        return self.SecureString(self.__authkey)
    
    @authkey.setter
    def authkey(self, key : Iterable[SupportsIndex] | SupportsIndex | SupportsBytes | bytes | bytearray | memoryview):
        """
        Changes the authentication key of this process.
        Take not that if you do so, and if the parent process is a Python process, it won't be able to recognize this process anymore.
        """
        try:
            new = bytes(key)
            if new != self.__authkey:
                self.__authkey = new
                self.__signal_change()
        except TypeError as e:
            raise e from None
    
    @property
    def daemon(self) -> bool:
        """
        A bool value that indicates if this process exits if its parent dies.
        """
        return self.__daemon
    
    @daemon.setter
    def daemon(self, value : bool):
        """
        Sets the daemon flag of this process.
        If the parent is already dead, setting this to True will cause the process to exit immediately.
        """
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got '{type(value).__name__}'")
        if value != self.__daemon:
            self.__daemon = value
            self.__signal_change()

local_env = Environment()





del Any, Callable, Iterable, SupportsIndex, SupportsBytes, TypedDict, TYPE_CHECKING