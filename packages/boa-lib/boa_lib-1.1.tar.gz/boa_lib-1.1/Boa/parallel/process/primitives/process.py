"""
This module defines some Process subclasses that are building blocks of the parallel package.
"""

import sys
from abc import abstractmethod
from typing import Any, Callable, Iterable, Literal, NoReturn, ParamSpec, TypeVar
from threading import RLock

from Viper.meta.iterable import InstanceReferencingHierarchy

from ...thread.decorators import exclusive
from ...thread import Future
from ..environment import Environment

__all__ = ["Process"]





P = ParamSpec("P")
T = TypeVar("T")
R = TypeVar("R")
Y = TypeVar("Y")
S = TypeVar("S")





class Process(metaclass = InstanceReferencingHierarchy):

    """
    Just a process class to hold general information about a process.
    """

    __slots__ = {
        "__weakref__" : "The weakref slot to allow for the creation of weak references to Process objects.",
        "__exit_code" : "A Future integer value indicating the exit code of the process that is set when the process dies."
    }

    __expanded_keys = Environment.expanded_keys()



    class __ProcessCallback:

        """
        Small internal class to transform a Future callback into a process callback.
        """

        def __init__(self, cb : Callable[["Process"], None], process : "Process") -> None:
            self.__callback = cb
            self.__process = process

        def __eq__(self, value: object) -> bool:
            return isinstance(value, type(self)) and value.__callback == self.__callback
        
        def __hash__(self) -> int:
            return hash(self.__callback)
        
        def __call__(self, fut : Future[int]) -> Any:
            return self.__callback(self.__process)
        
    

    def __init__(self) -> None:
        """
        Sets up the death trigger for this process. Note that subclasses shoudl execute this initialization once the "pid" property becomes available.
        """
        from ...thread import Future
        self.__exit_code : Future[int] = Future()
        self.__register_child()
    
    def add_callback(self, cb : Callable[["Process"], None]):
        """
        Adds a callback function to call when the process exits.
        The callback should take a single argument : the Process object that just exited.
        """
        self.__exit_code.add_callback(self.__ProcessCallback(cb, self))

    def remove_callback(self, cb : Callable[["Process"], None]):
        """
        Removes a callback function that should have been called when the process exits.
        If the callback was not registered, silently does nothing.
        """
        self.__exit_code.remove_callback(self.__ProcessCallback(cb, self))

    @property
    def exit_code(self) -> int | None:
        """
        The process exit code. None if the process has not exited yet.
        """
        if self.__exit_code.is_set:
            return self.__exit_code.result()
        return None

    @property
    @abstractmethod
    def pid(self) -> int | None:
        """
        The process identifier. It is None if the process has not been started yet or has exited.
        """
        raise NotImplementedError(f"You need to implement the 'pid' property of the '{type(self).__name__}' class.")
    
    @property
    @abstractmethod
    def environment(self) -> Environment:
        """
        The process environment object.
        """
        raise NotImplementedError(f"You need to implement the 'environment' property of the '{type(self).__name__}' class.")
    
    @environment.setter
    @abstractmethod
    def environment(self, env : Environment):
        """
        Sets the environment of the process.
        """
        raise NotImplementedError(f"You need to implement the 'environment' property of the '{type(self).__name__}' class.")

    def __getattribute__(self, name: str) -> Any:
        """
        Implements getattr(self, name). For a Process, if the attribute is not found, it will also lookup in its environment.
        """
        if name in Process.__expanded_keys:
            return getattr(self.environment, name)
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Implements setattr(self, name, value). For a Process, if the attribute is not found, it will also lookup in its environment.
        """
        if name in Process.__expanded_keys:
            return setattr(self.environment, name, value)
        super().__setattr__(name, value)
    
    def __dir__(self) -> Iterable[str]:
        """
        Implements dir(self). Returns the Process's attributes and its environment's attributes.
        """
        return list(super().__dir__()) + Process.__expanded_keys
        
    def __eq__(self, value: object) -> bool:
        """
        Implements self == value.
        """
        return isinstance(value, Process) and (value.pid == self.pid != None or value is self)
    
    def __hash__(self) -> int:
        """
        Implements hash(self).
        """
        return hash(self.pid)
    
    def __repr__(self) -> str:
        """
        Implements str(self).
        """
        if pid := self.pid:
            return f"{type(self).__name__} #{pid}"
        return f"{type(self).__name__} at {hex(id(self))}"
    
    def terminate(self):
        """
        Terminates the process (by sending SIGTERM).
        """
        if (pid := self.pid) is None:
            raise RuntimeError("Cannot terminate a process that has not been started yet or has already exited.")
        from os import kill
        from signal import SIGTERM
        kill(pid, SIGTERM)
    
    def join(self, timeout : float = float("inf")) -> bool:
        """
        Waits for the process to finish or for the timeout (in seconds) to pass.
        Returns True if the process has finished its execution, False if the timeout was reached.
        """
        if isinstance(timeout, (float | int | bool)):
            timeout = float(timeout)
        if not isinstance(timeout, float):
            raise TypeError(f"Expected float for timeout, got '{type(timeout).__name__}'")
        if timeout < 0:
            raise ValueError(f"Expected positive timeout, got '{timeout}'")
        return self.__exit_code.wait()
        
    @property
    def alive(self) -> bool:
        """
        True if the process is still running.
        """
        return not self.__exit_code.is_set

    @alive.setter
    def alive(self, value : Literal[False]):
        """
        Setting this to False will call self.terminate().
        """
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got '{type(value).__name__}'")
        if value != False:
            raise ValueError("Cannot make the process alive, only False is allowed")
        if self.alive:
            self.terminate()
    
    if sys.platform == "win32":

        def kill(self):
            """
            Kills the process (same as terminate).
            """
            Process.terminate(self)

        import _winapi
        from threading import Event
        __child_future_lock = RLock()
        __child_future_event = Event()
        __child_future_queue : list[tuple[Future[int], int]] = []
        del _winapi, Event

        def __register_child(self):
            """
            Internal function that registers this process to be watched by the child watcher.
            """
            from _winapi import OpenProcess, SYNCHRONIZE
            PROCESS_QUERY_INFORMATION = 0x400       # Let's hope it doesn't change...If only _winapi was more complete!
            pid = self.pid
            if pid is None:
                raise RuntimeError("Process intialization sequence failed. Use help(Process.__init__).")
            handle = OpenProcess(SYNCHRONIZE | PROCESS_QUERY_INFORMATION, False, pid)
            with Process.__child_future_lock:
                Process.__child_future_queue.append((self.__exit_code, handle))
                Process.__child_future_event.set()

        @staticmethod
        @exclusive
        def __child_watcher():
            """
            Internal function used to watch all existing children processes until they die.
            """
            from _winapi import WaitForMultipleObjects, GetExitCodeProcess, CloseHandle, WAIT_TIMEOUT, WAIT_ABANDONED_0, WAIT_OBJECT_0
            from ...thread import Future, DaemonThread
            from threading import Lock, current_thread
            MAX_HANDLES_PER_CALL = 63

            signal_fut : Future[int] = Future()
            signal_lock = Lock()
            registered_waiters : dict[int, "Future[int]"] = {}
            maps : dict[DaemonThread, list[int]] = {}
            map_lock = Lock()

            # Because WaitForMultipleObjects supports at most 63 handles, we need to create sub-threads to watch for packs of handles, and then set a Future when one of them is signaled by a handle.

            def waiter(handles : list[int]):
                while handles:
                    signaled = WaitForMultipleObjects(handles, False, 50)
                    if signaled != WAIT_TIMEOUT:
                        signal_lock.acquire()
                        signaled = handles.pop(signaled)
                        signal_fut.set(signaled)
                        with map_lock:
                            if not handles:
                                maps.pop(current_thread())

            def add_to_watch(handle : int):
                with map_lock:
                    for dt, handles in maps.items():
                        if len(handles) < MAX_HANDLES_PER_CALL:
                            handles.append(handle)
                            return
                    handles = [handle]
                    dt = DaemonThread(target=waiter, args=(handles,), name = f"Process Death Sub-Watcher #{len(maps)}")
                    maps[dt] = handles
                    dt.start()

            ok = False
            while not ok:       # We are doing this to wait until the module has been loaded.
                try:
                    Process
                    ok = True
                except NameError:
                    pass

            signaled = WAIT_TIMEOUT
            while True:
                if not registered_waiters:
                    Process.__child_future_event.wait()
                    signaled = WAIT_TIMEOUT
                else:
                    signaled_set = signal_fut.wait(0.05)
                    if signaled_set:
                        signaled = signal_fut.result()
                        signal_fut.clear()
                        signal_lock.release()
                if signaled in registered_waiters:
                    fut = registered_waiters.pop(signaled)
                    exit_code = GetExitCodeProcess(signaled)
                    fut.set(exit_code)
                    CloseHandle(signaled)
                with Process.__child_future_lock:
                    for fut, handle in Process.__child_future_queue:
                        registered_waiters[handle] = fut
                        add_to_watch(handle)
                    Process.__child_future_queue.clear()
                    Process.__child_future_event.clear()

    else:
            
        def kill(self):
            """
            Kills the process (by sending SIGKILL).
            """
            if (pid := self.pid) is None:
                raise RuntimeError("Cannot terminate a process that has not been started yet or has already exited.")
            from os import kill
            from signal import SIGKILL
            kill(pid, SIGKILL)

        __child_future_lock = RLock()
        __child_future_queue : list[tuple[Future[int], int]] = []

        def __register_child(self):
            """
            Internal function that registers this process to be watched by the child watcher.
            """
            pid = self.pid
            if pid is None:
                raise RuntimeError("Process intialization sequence failed. Use help(Process.__init__).")
            with Process.__child_future_lock:
                Process.__child_future_queue.append((self.__exit_code, pid))

        @staticmethod
        @exclusive
        def __child_watcher():
            """
            Internal function used to watch all existing children processes until they die.
            """
            from os import wait
            from time import sleep
            ok = False
            while not ok:       # We are doing this to wait until the module has been loaded.
                try:
                    Process
                    ok = True
                except NameError:
                    pass
            registered_waiters : dict[int, "Future[int]"] = {}
            while True:
                try:
                    pid, exit_code = wait()
                except ChildProcessError:
                    pid = 0
                    exit_code = 0
                with Process.__child_future_lock:
                    for fut, waiting_pid in Process.__child_future_queue:
                        registered_waiters[waiting_pid] = fut
                    Process.__child_future_queue.clear()
                if pid == 0:
                    for waiting_pid, fut in registered_waiters.items():
                        fut.set(exit_code)
                    registered_waiters.clear()
                    sleep(0.05)
                elif pid in registered_waiters:
                    registered_waiters.pop(pid).set(exit_code)
        
    
    from ...thread import DaemonThread
    DaemonThread(target = __child_watcher, name = "Process Death Watcher").start()
    del DaemonThread
        




class LocalProcess(Process):

    """
    This class is made to represent the current interpreter's process.
    """

    @exclusive
    def __new__(cls):
        for p in cls:
            return p
        return super().__new__(cls)
    
    def __init__(self) -> None:
        pass    # We do not want to wait for this process...

    @property
    def exit_code(self):
        raise RuntimeError("Cannot request the exit code of the local process")
    
    @property
    def pid(self) -> int:
        from os import getpid
        return getpid()
    
    @property
    def environment(self) -> Environment:
        from ..environment import local_env
        return local_env
    
    @environment.setter
    def environment(self, env : Environment):
        from .. import environment
        if not isinstance(env, environment.Environment):
            raise TypeError(f"Expected Environment, got '{type(env).__name__}'")
        environment.local_env.copy_from(env.export())
    
    def join(self, timeout: float = float("inf")) -> Literal[False] | NoReturn:
        from time import sleep
        if timeout < float("inf"):
            sleep(timeout)
            return False
        else:
            while True:
                sleep(3600)     # Yes, this is arbitrary

    @Process.alive.getter
    def alive(self) -> bool:
        """
        Returns True, since this is called from the *still alive* process.
        """
        return True

    def _self_destruct(self, p : Process):
        """
        Internal function used to terminate the current process when the parent process dies and the local daemon flag is set to True.
        """
        def watch_env(env : "Environment"):
            if env.daemon:
                raise SystemExit(0)
        
        self.environment.add_callback(watch_env)
        watch_env(self.environment)     # Call it once now





class ParentProcess(Process):

    """
    This class is made to represent the parent process of the current interpreter's process.
    """

    @exclusive
    def __new__(cls):
        for p in cls:
            return p
        return super().__new__(cls)
    
    def __init__(self) -> None:
        from os import getppid
        self.__base_pid = getppid()
        self.__pid = None
        self.__is_python = None
    
    @property
    def is_python(self) -> bool:
        """
        This property indicates if the parent process is a Python process.
        In such a case :
        - It might not be the actual parent (on some platforms, another process might be in between the current process and the this object in the process tree).
        - Communication is possible with this process, which might cause changes in the environment.
        """
        return self.__is_python or False
    
    @is_python.setter
    def is_python(self, value : bool):
        if self.__is_python is not None:
            raise AttributeError(f"property 'is_python' of '{type(self).__name__}' object has no setter")
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got '{type(value).__name__}'")
        self.__is_python = value

    @property
    def pid(self) -> int | None:
        if self.__pid is not None:
            if self.__pid < 0:
                return None
            return self.__pid
        return self.__base_pid
    
    @pid.setter
    def pid(self, value : int):
        if self.__pid is not None:
            raise AttributeError(f"property 'pid' of '{type(self).__name__}' object has no setter")
        if not isinstance(value, int):
            raise TypeError(f"Expected int, got '{type(value).__name__}'")
        self.__pid = value
        super().__init__()
        self.add_callback(lambda p : delattr(self, "pid"))
        self.add_callback(LocalProcess()._self_destruct)
        del LocalProcess._self_destruct
    
    @pid.deleter
    def pid(self):
        self.__pid = -1

    @property
    def environment(self) -> Environment:
        raise AttributeError("Cannot get the environment of the parent process. The current process inherits it by default.")
    
p, l = ParentProcess(), LocalProcess()      # Create the unique instances now.
del p, l





del sys, abstractmethod, Any, Callable, Iterable, NoReturn, ParamSpec, TypeVar, RLock, InstanceReferencingHierarchy, exclusive, Future, Environment, P, T, R, Y, S