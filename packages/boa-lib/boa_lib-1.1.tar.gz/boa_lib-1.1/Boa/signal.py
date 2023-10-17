"""
This module is used for creating multiple signal handlers from any threads.

Use add_handler(sig : Signals, handler : HandlerType) and remove_handler(sig : Signals, handler : HandlerType) to register/unregister signal handlers.
This is done using the Enum Signals which is compatible with bitwise operations:
>>> add_handler(Signals.SIGINT | Signals.SIGBREAK, handler)

You can also manage handlers from the Signals:
>>> Signals.SIGINT.add_handler(handler)

Note that this is build over the signal module. Using signal.signal() after loading this module will cause the corresponding handlers to be missed.
Also not that handlers will be called in the order in which they were added.
"""

import signal
from threading import RLock
from types import FrameType
from typing import Callable
from enum import IntFlag

__all__ = ["add_handler", "remove_handler", "Signals", "UncatchableSignals"]





from threading import current_thread, main_thread
if current_thread() != main_thread():
    raise RuntimeError("The Boa.signal module should be loaded by the main thread")
del current_thread, main_thread

HandlerType = Callable[["SignalManager.Signals"], None]

class SignalManager:

    """
    This class is just here to setup all the advanced signal handling system.
    """

    # This part of the code will place the code used to set the multiplexing signal handlers.

    __signal_names : dict[int, str] = {}
    __signal_enum : dict[int, "Signals"] = {}
    __state_lock = RLock()

    for sig in signal.Signals:

        for name, value in vars(signal).items():
            if value == sig:
                __signal_names[value] = name
            del name, value

        del sig

    @staticmethod
    def __advanced_handler(sig_num : "Signals"):
        """
        This is the base handler that will call all the user-registered handlers. 
        """
        with SignalManager.__state_lock:
            if sig_num not in SignalManager.__registered_handlers:
                raise RuntimeError(f"Unknown signal : {sig_num}")
            exceptions : list[BaseException] = []
            for h in SignalManager.__registered_handlers[sig_num].copy():
                try:
                    h(sig_num)
                except BaseException as e:
                    exceptions.append(e)
            if exceptions:
                if len(exceptions) == 1:
                    raise RuntimeError(f"Got an exception in the signal handler for signal {sig_num.name}") from exceptions[0]
                else:
                    raise RuntimeError(f"Got some exceptions in the signal handler for signal {sig_num.name}") from BaseExceptionGroup("Here are the different exceptions that occured in each signal handler:", exceptions)

    # Setting up specialized handlers for each existing signal

    __uncatchable_signals : list[int] = []

    for sig_num, sig_name in __signal_names.copy().items():

        handler_name = f"{sig_name}_handler"
        handler_doc = f"Handles the signal {sig_name} by calling all the registered handlers."
        try:
            handler_doc += f"\nThe description of this signal is: {signal.strsignal(sig_num)}"
        except:
            pass

        try:
            last_handler = signal.getsignal(sig_num)
            if not callable(last_handler):
                last_handler = None
        except:
            last_handler = None
        
        if last_handler:

            @staticmethod
            def __handler_1(sig : int, frame : FrameType | None, old_handler = last_handler):
                try:
                    old_handler(sig, frame)
                finally:
                    SignalManager.__advanced_handler(SignalManager.__signal_enum[sig])
            
            __handler_1.__name__ = handler_name
            __handler_1.__qualname__ = handler_name
            __handler_1.__doc__ = handler_doc

            try:
                signal.signal(sig_num, __handler_1)
            except ValueError:
                __signal_names.pop(sig_num)
            except OSError:
                __uncatchable_signals.append(sig_num)

            del __handler_1
        
        else:

            @staticmethod
            def __handler_2(sig : int, frame : FrameType | None):
                SignalManager.__advanced_handler(SignalManager.__signal_enum[sig])
            
            __handler_2.__name__ = handler_name
            __handler_2.__qualname__ = handler_name
            __handler_2.__doc__ = handler_doc

            try:
                signal.signal(sig_num, __handler_2)
            except ValueError:
                __signal_names.pop(sig_num)
            except OSError:
                __uncatchable_signals.append(sig_num)

            del __handler_2

        del handler_doc, handler_name, last_handler, sig_name, sig_num

    class DescribedFlag:

        name : str

        @property
        def doc(self) -> str | None:
            """
            Returns the description of the signal if it has one.
            """
            import signal
            val = None
            for name, s in vars(signal).items():
                if name == self.name:
                    val = int(s)
                    break
            if val is None:
                return None
            try:
                return signal.strsignal(val)
            except:
                return None

    class HandlerFlag(DescribedFlag):

        def add_handler(self, handler : HandlerType):
            """
            Registers a handler to be called when this signal is received. It can be registered multiple times.
            This function will block if a signal is being processed (until processing finishes) and is not called from the main thread.
            Note that when calling this function from a signal handler, the new handler won't be called with the ongoing signal.
            """
            SignalManager.add_handler(self, handler) # type: ignore because the correct type comes later

        def remove_handler(self, handler : HandlerType):
            """
            Unregisters all occurences of this handler for this signal. If it was not registered, silently does nothing.
            This function will block if a signal is being processed (until processing finishes) and is not called from the main thread.
            Note that when calling this function from a signal handler, the new handler will still be called with the ongoing signal.
            """
            SignalManager.remove_handler(self, handler) # type: ignore because the correct type comes later
    
    uncatchable_names = []
    for sig_num in __uncatchable_signals:
        uncatchable_names.append(__signal_names[sig_num])
        del sig_num
    UncatchableSignals = IntFlag("UncatchableSignals", uncatchable_names)
    del uncatchable_names
    for sig_num in __uncatchable_signals:
        __signal_names.pop(sig_num)
        del sig_num
    del __uncatchable_signals
    Signals = IntFlag("Signals", list(__signal_names.values()), type = HandlerFlag)
    del HandlerFlag
    for sig_fl in Signals:
        for sig_num, sig_name in __signal_names.items():
            if sig_name == sig_fl.name:
                __signal_enum[sig_num] = sig_fl
            del sig_num, sig_name
        del sig_fl 
    del __signal_names

    __registered_handlers : dict[Signals, list[HandlerType]] = {sig : [] for sig in Signals}        # Registered handlers per signal

    # Now we can add the special methods to manage handlers.

    @staticmethod
    def add_handler(signal : Signals, handler : HandlerType):
        """
        Registers a handler to be called when given signal is received. It can be registered multiple times.
        This function will block if a signal is being processed (until processing finishes) and is not called from the main thread.
        Note that when calling this function from a signal handler, the new handler won't be called with the ongoing signal.
        """
        if not isinstance(signal, SignalManager.Signals) or not callable(handler):
            raise TypeError(f"Expected Signal and callable, got '{type(signal).__name__}' and '{type(handler).__name__}'")
        with SignalManager.__state_lock:
            for sig in SignalManager.Signals:
                if sig & signal:
                    SignalManager.__registered_handlers[sig].append(handler)

    @staticmethod
    def remove_handler(signal : Signals, handler : HandlerType):
        """
        Unregisters all occurences of this handler for the given signal. If it was not registered, silently does nothing.
        This function will block if a signal is being processed (until processing finishes) and is not called from the main thread.
        Note that when calling this function from a signal handler, the new handler will still be called with the ongoing signal.
        """
        if not isinstance(signal, SignalManager.Signals) or not callable(handler):
            raise TypeError(f"Expected Signal and callable, got '{type(signal).__name__}' and '{type(handler).__name__}'")
        with SignalManager.__state_lock:
            for sig in SignalManager.Signals:
                if sig & signal:
                    while handler in SignalManager.__registered_handlers[sig]:
                        SignalManager.__registered_handlers[sig].remove(handler)





add_handler = SignalManager.add_handler
remove_handler = SignalManager.remove_handler
Signals = SignalManager.Signals
UncatchableSignals = SignalManager.UncatchableSignals





del signal, FrameType, RLock, IntFlag, Callable