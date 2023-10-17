# Boa
A library of advanced system tools for Python.

Boa adds upgraded versions of system tools. For example, this includes advanced pipes, parallelism, etc.
It is designed to have a simple Pythonic interface.

To list all of the available packages, simply Python's interactive prompt and explore:

```
>>> from Boa import *
>>> help(parallel)
Help on package Boa.parallel in Boa:

NAME
    Boa.parallel - This package contains some useful tools when working with multithreading or multiprocessing.

PACKAGE CONTENTS
    abc (package)
    exceptions
    process (package)
    thread (package)
...
```

Some practical examples of the content of Boa include:
- Futures to manage eventual objects to come:

```
>>> from Boa.parallel.thread import Future
>>> from threading import Thread
>>> f = Future()
>>> def show_future():
...         while True:
...                 print(f"Future got set to {f.result()}.")
...                 f.clear()
... 
>>> Thread(target = show_future).start()
>>> f.set("Hello")
Future got set to Hello.
>>> f.set(True)
Future got set to True.
>>> f.set_exception(ValueError("Time to stop"))
Exception in thread Thread-1 (show_future):
Traceback (most recent call last):
  File "C:\Program Files\Python311\Lib\threading.py", line 1038, in _bootstrap_inner
     self.run()
  File "C:\Program Files\Python311\Lib\threading.py", line 975, in run
    self._target(*self._args, **self._kwargs)
  File "<stdin>", line 3, in show_future
  File "C:\Users\Vince\OneDrive\Documents\Python\Boa\Boa\parallel\thread\future.py", line 248, in result
    raise self.__exception from None
ValueError: Time to stop
```
Futures are particularly useful in multithreaded environement for synchronization, especially with their special methods to cancel Futures, link them together, etc.

- Many parallelism decorators:
```
>>> from Boa.parallel.thread import exclusive
>>> from time import sleep
>>> @exclusive
... def run():
...         print("Entering...")
...         sleep(5)
...         print("Exiting.")
... 
>>> from threading import Thread
>>> for i in range(5):
...         Thread(target = run).start()
... 
Entering...
>>> Exiting.
Entering...
Exiting.
Entering...
Exiting.
Entering...
Exiting.
Entering...
Exiting.
```

This decorator and others allow you to ensure exclusion with precise rules accros a multithreaded program.

- Better signal handling:
```
>>> from Boa.signal import *
>>> Signals.
Signals.SIGABRT           Signals.SIGILL            Signals.SIGTERM           Signals.bit_length(       Signals.from_bytes(       Signals.numerator
Signals.SIGBREAK          Signals.SIGINT            Signals.as_integer_ratio( Signals.conjugate(        Signals.imag              Signals.real
Signals.SIGFPE            Signals.SIGSEGV           Signals.bit_count(        Signals.denominator       Signals.mro()             Signals.to_bytes(
>>> Signals.SIGINT.add_handler(lambda s : print(f"Received signal {s.name}"))
>>> Received signal SIGINT

KeyboardInterrupt
```

- And many other useful random features!

Note that this library is extensively documented. Use Python's help system (for example the help function while in an interactive interpreter) to learn how to use all the modules and classes.