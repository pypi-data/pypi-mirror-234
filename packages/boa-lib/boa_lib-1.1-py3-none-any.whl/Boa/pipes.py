"""
This module contains a cross-platform inheritable version of pipes.
"""

from multiprocessing.shared_memory import SharedMemory
from threading import RLock, Thread, Event
from typing import ContextManager, TypeVar
from weakref import WeakSet

from Viper.abc.io import (STREAM_PACKET_SIZE, BytesIO, BytesIOBase,
                          BytesReader, BytesWriter)
from Viper.abc.utils import Budget

from .parallel.thread.decorators import exclusive

__all__ = ["pipe", "bridge"]





T1 = TypeVar("T1", bound=ContextManager)
T2 = TypeVar("T2", bound=ContextManager)

class _ContextTuple(tuple[T1, T2]):

    """
    Just a tuple subclass that can work with context managers (for its elements).
    Used by pipe() and bridge().
    """

    def __enter__(self):
        """
        Implements with self.
        """
        for e in self:
            if hasattr(e, "__enter__") and callable(e.__enter__):
                e.__enter__()
        return self
    
    def __exit__(self, exc_type, exc, traceback):
        """
        Implements with self.
        """
        for e in self:
            if hasattr(e, "__exit__") and callable(e.__exit__):
                e.__exit__(exc_type, exc, traceback)

del T1, T2

ACTIVE_WAIT_CYCLES = 1024
PASSIVE_CHECKER_INTERVAL = 1000000

class _PipeBase(BytesIOBase):

    """
    This is an abstract base class for pipes.

    Note that you don't need to close the pipes yourself, they are closed at destruction or at normal interpreter shutdown (undefined behavior on abrupt interpreter shutdown).
    """

    def seekable(self) -> bool:
        return False
    
    def seek(self, offset: int, whence: int = ...) -> int:
        """
        This method is here for compatibility. Pipes are not seekable.
        """
        raise OSError("Pipes are not seekable.")
    
    def fileno(self) -> int:
        """
        This method is here for compatibility. Pipes don't have an associated file descriptor.
        """
        raise OSError("Pipes don't have an associated file descriptor.")
        




class _CircularSharedArray(SharedMemory):

    """
    This class of memory array works as a circular buffer.
    """

    __SIZE_LENGTH = 8

    def __init__(self, name: str | None = None, create: bool = False, size: int = 0) -> None:
        super().__init__(name, create, size + self.__SIZE_LENGTH * 3 + 1)
        self.__read = memoryview(self.buf)[self.__SIZE_LENGTH : self.__SIZE_LENGTH * 2]
        self.__writen = memoryview(self.buf)[self.__SIZE_LENGTH * 2 : self.__SIZE_LENGTH * 3]
        self.__closed = memoryview(self.buf)[self.__SIZE_LENGTH * 3 : self.__SIZE_LENGTH * 3 + 1]
        if create:
            memoryview(self.buf)[0 : self.__SIZE_LENGTH] = size.to_bytes(self.__SIZE_LENGTH, "little")
            self.__read[:] = (0).to_bytes(self.__SIZE_LENGTH)
            self.__writen[:] = (0).to_bytes(self.__SIZE_LENGTH)
            self.__closed[0] = 0
        else:
            size = int.from_bytes(memoryview(self.buf)[0 : self.__SIZE_LENGTH], "little")
        self.__size = size
        self.__buffer = memoryview(self.buf)[self.__SIZE_LENGTH * 3 + 1 : self.__SIZE_LENGTH * 3 + 1 + self.size]

    @property
    def size(self) -> int:
        return self.__size
    
    @property
    def closed(self) -> bool:
        """
        Returns True if the closed flag is set.
        """
        return self.__closed.tobytes() != b"\0"
    
    def close(self):
        """
        Sets the closed flag to True.
        """
        self.__closed[0] = 1
    
    @property
    def __read_index(self) -> int:
        """
        The current reading index.
        """
        return int.from_bytes(self.__read, "little")
    
    @__read_index.setter
    def __read_index(self, val : int):
        self.__read[:] = val.to_bytes(self.__SIZE_LENGTH, "little")
    
    @property
    def __write_index(self) -> int:
        """
        The current writing index.
        """
        return int.from_bytes(self.__writen, "little")
    
    @__write_index.setter
    def __write_index(self, val : int):
        self.__writen[:] = val.to_bytes(self.__SIZE_LENGTH, "little") 
    
    @property
    def readable(self) -> int:
        """
        The amount of data that can immediately be read.
        """
        return self.__write_index - self.__read_index
    
    @property
    def writable(self) -> int:
        """
        The amount of data that can immediately be written.
        """
        return self.__read_index - self.__write_index + self.__size
    
    def read(self, n : int) -> bytes:
        """
        Reads the amount of bytes specified and moves reading index forward.
        Cannot read more than self.readable.
        """
        start, end, size = self.__read_index, self.__write_index, self.size
        end = min(end, start + n)
        if end == start:
            return b""
        if start % size < end % size:
            packet = self.__buffer[start % size : end % size].tobytes()
        else:
            packet = self.__buffer[start % size :].tobytes() + self.__buffer[: end % size].tobytes()
        self.__read_index = end
        return packet
    
    def readline(self, n : int) -> bytes:
        """
        Reads the amount of bytes specified or until a newline is encountered and moves reading index forward.
        Cannot read more than self.readable.
        """
        start, end, size = self.__read_index, self.__write_index, self.size
        end = min(end, start + n)
        if end == start:
            return b""
        if start % size < end % size:
            packet = self.__buffer[start % size : end % size].tobytes()
        else:
            packet = self.__buffer[start % size :].tobytes() + self.__buffer[: end % size].tobytes()
        if b"\n" in packet:
            packet = packet[: packet.index(b"\n") + 1]
        self.__read_index = start + len(packet)
        return packet
    
    def write(self, data : bytes | bytearray | memoryview) -> int:
        """
        Writes the given data and moves the writing index forward. Returns the amount of bytes written.
        Cannot write more than self.writable.
        """
        start, end, size = self.__write_index, self.__read_index, self.size
        end += size
        end = min(end, start + len(data))
        if end == start:
            return 0
        if start % size < end % size:
            self.__buffer[start % size : end % size] = data
        else:
            array1, array2 = self.__buffer[start % size :], self.__buffer[: end % size]
            packet = memoryview(data)
            array1[:], array2[:] = packet[: len(array1)], packet[len(array1) : len(array1) + len(array2)]
        self.__write_index = end
        return end - start
    
    @property
    def total_read(self) -> int:
        """
        The total amount of data that was read through this array.
        """
        return self.__read_index
    
    @property
    def total_written(self) -> int:
        """
        The total amount of data that was written through this pipe.
        """
        return self.__write_index

    def __del__(self):
        try:
            self.close()
        except:
            pass





module_ready = Event()
reader_thread_ready = Event()
writer_thread_ready = Event()

class PipeReader(_PipeBase, BytesReader):

    """
    This is the reading end of a pipe. Acts as a file-like object.
    To share it with another process, just use pickle.
    To work, it should be connected to a PipeWriter.
    Use pipe() to create both.
    """

    __waiting : WeakSet["PipeReader"] = WeakSet()
    from Viper.abc.io import IOClosedError as __IOClosedError

    def __init__(self, array : _CircularSharedArray) -> None:
        import atexit
        from Viper.abc.utils import Budget
        from Viper.abc.io import BytesReader
        BytesReader.__init__(self)
        self.__array = array
        self.__readable = Budget(array.readable)
        self.__readable.add_callback(self.__schedule_cursor_update)
        self.__dual = None
        atexit.register(self.close)
        self.__unregister = lambda : atexit.unregister(self.close)

    def __setstate__(self, array : _CircularSharedArray):
        import atexit
        from Viper.abc.utils import Budget
        from Viper.abc.io import BytesReader
        BytesReader.__init__(self)
        self.__dual = None
        self.__array = array
        self.__readable = Budget(array.readable)
        self.__readable.add_callback(self.__schedule_cursor_update)
        atexit.register(self.close)
        self.__unregister = lambda : atexit.unregister(self.close)

    def __getstate__(self):
        return self.__array
    
    @property
    def lock(self) -> RLock:
        return self.__readable.lock
    
    @property
    def readable(self):
        return self.__readable

    @property
    def dual(self) -> "PipeWriter | None":
        """
        The writing side of this pipe, if it exists in this process.
        """
        return self.__dual
    
    @dual.setter
    def dual(self, d : "PipeWriter"):
        """
        Sets the writing side of this pipe. Can only be done once.
        """
        if self.__dual is not None:
            raise RuntimeError("Dual already set")
        if not isinstance(d, PipeWriter):
            raise TypeError(f"Expected PipeWriter, got '{type(d).__name__}'")
        self.__dual = d
        if d.dual is None:
            d.dual = self
        
    def close(self):
        if not self.closed:
            self.__array.close()
            self.__readable.close()
            try:
                self.__unregister()
            except:
                pass

    @property
    def closed(self) -> bool:
        if self.__array.closed and not self.__readable.closed:
            self.__readable.close()
        return self.__array.closed

    def tell(self) -> int:
        with self.lock:
            return self.__array.total_read
        
    def __update_cursor(self) -> int:
        """
        Internal function used to update the size of the next packet to come.
        """
        try:
            diff = self.__array.readable - self.readable.value
            if diff >= 0:
                self.readable.increase(diff)
            else:
                self.readable.decrease(-diff)
        except RuntimeError:
            pass
        return self.readable.value
    
    def __check_closed(self) -> bool:
        """
        Internal function used to check if the pipe was closed via its array.
        """
        if self.__array.closed and not self.__readable.closed:
            self.__readable.close()
            try:
                self.__unregister()
            except:
                pass
            return True
        return self.closed

    def __schedule_cursor_update(self, bud : Budget):
        """
        Internal function used to schedule the update of the read marker when it reaches zero.
        """
        for i in range(ACTIVE_WAIT_CYCLES):
            if self.__update_cursor() or self.__check_closed():
                return
        while self in self.__waiting:
            pass
        self.__waiting.add(self)
    
    @staticmethod
    @exclusive
    def __background_checker():
        """
        Internal function used to check the status of all PipeReader instances that are passively waiting.
        """
        from typing import TypeVar, Iterator
        T = TypeVar("T")
        def secure_weak_ref_iterator(s : "WeakSet[T]") -> Iterator[T]:      # Yes, even making a copy inside a real set can still cause weakref exceptions!!!
            it = iter(s)
            while True:
                try:
                    yield next(it)
                except (RuntimeError, StopIteration):
                    break
        from time import sleep
        dt = PASSIVE_CHECKER_INTERVAL / (10 ** 9)
        module_ready.wait()
        reader_thread_ready.set()
        __waiting = PipeReader.__waiting
        while True:
            sleep(dt)
            for self in secure_weak_ref_iterator(__waiting):
                try:
                    if self.__update_cursor() or self.__check_closed():
                        __waiting.discard(self)
                except:
                    __waiting.discard(self)
                del self

    Thread(target = __background_checker, name = "PipeReader Passive Background Checker", daemon = True).start()
    
    def read(self, size : int | float = float("inf")) -> bytes:
        if not isinstance(size, int) and size != float("inf"):
            raise TypeError(f"Expected int or float('inf'), got {type(size).__name__}")
        if size < 0:
            raise ValueError(f"Expected positive integer, got {size}")        
        if self.closed and not self.readable:
            raise self.__IOClosedError("Pipe has been closed")
        
        if isinstance(size, float):
            buffer = bytearray()
        else:
            buffer = bytearray(size)
        done = 0
        with self.lock:
            while done < size and not (self.closed and not self.readable):
                with self.readable as readable:
                    if not readable:
                        break
                    packet = self.__array.read(min(readable, size - done))          # type: ignore because float("inf") won't be the min...
                    buffer[done : done + len(packet)] = packet
                    done += len(packet)
                    self.readable.decrease(len(packet))
            return memoryview(buffer)[:done].tobytes()
    
    def readinto(self, buffer: bytearray | memoryview) -> int:
        if not isinstance(buffer, (bytearray, memoryview)):
            raise TypeError(f"Expected writable buffer, got '{type(buffer).__name__}'")
        if len(buffer) == 0:
            return 0
        if self.closed and not self.readable:
            raise self.__IOClosedError("Pipe has been closed")

        done = 0
        with self.lock:
            while done < len(buffer) and not (self.closed and not self.readable):
                with self.readable as readable:
                    if not readable:
                        break
                    packet = self.__array.read(min(readable, len(buffer) - done))          # type: ignore because float("inf") won't be the min...
                    buffer[done : done + len(packet)] = packet
                    done += len(packet)
                    self.readable.decrease(len(packet))
            return done
    
    def readline(self, size : int | float = float("inf")) -> bytes:
        if not isinstance(size, int) and size != float("inf"):
            raise TypeError(f"Expected int or float('inf'), got {type(size).__name__}")
        if size < 0:
            raise ValueError(f"Expected positive integer, got {size}")
        if self.closed and not self.readable:
            raise self.__IOClosedError("Pipe has been closed")
        
        if isinstance(size, float):
            buffer = bytearray()
        else:
            buffer = bytearray(size)
        done = 0
        with self.lock:
            while done < size and not (self.closed and not self.readable):
                with self.readable as readable:
                    if not readable:
                        break
                    packet = self.__array.readline(min(readable, size - done))          # type: ignore because float("inf") won't be the min...
                    buffer[done : done + len(packet)] = packet
                    done += len(packet)
                    self.readable.decrease(len(packet))
                    if packet.endswith(b"\n"):
                        break
            return memoryview(buffer)[:done].tobytes()
    




class PipeWriter(_PipeBase, BytesWriter):

    """
    This is the writing end of a pipe. Acts as a file-like object.
    To share it with another process, just use pickle.
    To work, it should be connected to a PipeReader.
    Use pipe() to create both.
    """

    __waiting : WeakSet["PipeWriter"] = WeakSet()
    from Viper.abc.io import IOClosedError as __IOClosedError

    def __init__(self, array : _CircularSharedArray) -> None:
        import atexit
        from Viper.abc.utils import Budget
        from Viper.abc.io import BytesWriter
        BytesWriter.__init__(self)
        self.__array = array
        self.__writable = Budget(array.writable)
        self.__writable.add_callback(self.__schedule_cursor_update)
        self.__dual = None
        atexit.register(self.close)
        self.__unregister = lambda : atexit.unregister(self.close)

    def __setstate__(self, array : _CircularSharedArray):
        import atexit
        from Viper.abc.utils import Budget
        from Viper.abc.io import BytesWriter
        BytesWriter.__init__(self)
        self.__dual = None
        self.__array = array
        self.__writable = Budget(array.writable)
        self.__writable.add_callback(self.__schedule_cursor_update)
        atexit.register(self.close)
        self.__unregister = lambda : atexit.unregister(self.close)

    def __getstate__(self):
        return self.__array
    
    @property
    def lock(self) -> RLock:
        return self.__writable.lock
    
    @property
    def writable(self) -> Budget:
        return self.__writable

    @property
    def dual(self) -> "PipeReader | None":
        """
        The writing side of this pipe, if it exists in this process.
        """
        return self.__dual
    
    @dual.setter
    def dual(self, d : "PipeReader"):
        """
        Sets the writing side of this pipe. Can only be done once.
        """
        if self.__dual is not None:
            raise RuntimeError("Dual already set")
        if not isinstance(d, PipeReader):
            raise TypeError(f"Expected PipeReader, got '{type(d).__name__}'")
        self.__dual = d
        if d.dual is None:
            d.dual = self
    
    def close(self):
        if not self.closed:
            self.__array.close()
            self.__writable.close(erase = True)
            try:
                self.__unregister()
            except:
                pass

    @property
    def closed(self) -> bool:
        if self.__array.closed and not self.__writable.closed:
            self.__writable.close(erase = True)
        return self.__array.closed

    def tell(self) -> int:
        with self.lock:
            return self.__array.total_written
        
    def __update_cursor(self) -> int:
        """
        Internal function used to update the size of the next packet to send.
        """
        try:
            diff = self.__array.writable - self.writable.value
            if diff >= 0:
                self.writable.increase(diff)
            else:
                self.writable.decrease(-diff)
        except RuntimeError:
            pass
        return self.writable.value
    
    def __check_closed(self) -> bool:
        """
        Internal function used to check if the pipe was closed via its array.
        """
        if self.__array.closed and not self.__writable.closed:
            self.__writable.close()
            try:
                self.__unregister()
            except:
                pass
            return True
        return self.closed

    def __schedule_cursor_update(self, bud : Budget):
        """
        Internal function used to schedule the update of the write marker when it reaches zero.
        """
        for i in range(ACTIVE_WAIT_CYCLES):
            if self.__update_cursor() or self.__check_closed():
                return
        while self in self.__waiting:
            pass
        self.__waiting.add(self)
    
    @staticmethod
    @exclusive
    def __background_checker():
        """
        Internal function used to check the status of all PipeWriter instances that are passively waiting.
        """
        from typing import TypeVar, Iterator
        T = TypeVar("T")
        def secure_weak_ref_iterator(s : "WeakSet[T]") -> Iterator[T]:
            it = iter(s)
            while True:
                try:
                    yield next(it)
                except (RuntimeError, StopIteration):
                    break
        from time import sleep
        dt = PASSIVE_CHECKER_INTERVAL / (10 ** 9)
        module_ready.wait()
        writer_thread_ready.set()
        __waiting = PipeWriter.__waiting
        while True:
            sleep(dt)
            for self in secure_weak_ref_iterator(__waiting):
                try:
                    if self.__update_cursor() or self.__check_closed():
                        __waiting.discard(self)
                except:
                    __waiting.discard(self)
                del self

    Thread(target = __background_checker, name = "PipeWriter Passive Background Checker", daemon = True).start()
    
    def truncate(self, size: int | None = None):
        raise OSError("Pipes are not truncable.")
    
    def write(self, data: bytes | bytearray | memoryview) -> int:
        if not isinstance(data, bytes | bytearray | memoryview):
            raise TypeError(f"Expected readable buffer, got '{type(data).__name__}'")
        if self.closed:
            raise self.__IOClosedError("Pipe has been closed")
        
        done = 0
        data = memoryview(data)
        with self.lock:
            while done < len(data):
                with self.writable as writable:
                    if not writable:
                        break
                    n = self.__array.write(data[done : min(done + writable, len(data))])
                    done += n
                    self.writable.decrease(n)
            return done
        




class Duplex(BytesIO):

    """
    This is a bidirectional pipe. Acts as a file-like object.
    To share it with another process, just use pickle.
    To work, it should be connected to another Duplex.
    Use bridge() to create a pair.
    """

    def __init__(self, array1 : _CircularSharedArray, array2 : _CircularSharedArray) -> None:
        self.__reader = PipeReader(array1)
        self.__writer = PipeWriter(array2)
        self.__dual = None
    
    @property
    def readable(self):
        return self.reader.readable
    
    @property
    def writable(self):
        return self.writer.writable
    
    @property
    def read_lock(self):
        return self.reader.read_lock
    
    @property
    def write_lock(self):
        return self.writer.write_lock

    @property
    def reader(self) -> PipeReader:
        """
        Returns the reading end of this Duplex.
        """
        return self.__reader
    
    @property
    def writer(self) -> PipeWriter:
        """
        Returns the writing end of this Duplex.
        """
        return self.__writer
    
    def __getstate__(self):
        """
        Implements dumps(self).
        """
        return {
            "__reader" : self.reader,
            "__writer" : self.writer
        }
    
    def __setstate__(self, state):
        """
        Implements loads(self).
        """
        self.__reader = state["__reader"]
        self.__writer = state["__writer"]
        self.__dual = None
    
    @property
    def dual(self) -> "Duplex | None":
        """
        The writing side of this pipe, if it exists in this process.
        """
        return self.__dual
    
    @dual.setter
    def dual(self, d : "Duplex"):
        """
        Sets the writing side of this pipe. Can only be done once.
        """
        if self.__dual is not None:
            raise RuntimeError("Dual already set")
        if not isinstance(d, Duplex):
            raise TypeError(f"Expected Duplex, got '{type(d).__name__}'")
        self.__dual = d
        self.reader.dual = d.writer
        if d.dual is None:
            d.dual = self

    def __ensure_same_state(self):
        """
        Internal function that makes sure the reader and the writer are in the same state.
        """
        if self.reader.closed and not self.writer.closed:
            self.writer.close()
        if self.writer.closed and not self.reader.closed:
            self.reader.close()
    
    def fileno(self) -> int:
        raise OSError("Duplexes don't have a unique underlying stream")
    
    def isatty(self) -> bool:
        raise OSError("Duplexes don't have a unique underlying stream")
    
    def close(self):
        self.reader.close()
        self.writer.close()
    
    @property
    def closed(self) -> bool:
        with self.lock:
            self.__ensure_same_state()
            return self.reader.closed and self.writer.closed
    
    def tell(self) -> int:
        raise OSError("Duplexes don't have a unique underlying stream")

    def seekable(self) -> bool:
        return False
    
    def seek(self, offset: int, whence: int = ...) -> int:
        raise OSError("Duplexes don't have a unique underlying stream")
    
    def read(self, size : int | float = float("inf")) -> bytes:
        self.__ensure_same_state()
        return self.reader.read(size)
    
    def readinto(self, buffer: bytearray | memoryview) -> int:
        self.__ensure_same_state()
        return self.reader.readinto(buffer)
    
    def readline(self, size : int | float = float("inf")) -> bytes:
        self.__ensure_same_state()
        return self.reader.readline(size)
        
    def truncate(self, size: int | None = None):
        raise OSError("Duplexes don't have a unique underlying stream")
    
    def write(self, data: bytes | bytearray | memoryview) -> int:
        self.__ensure_same_state()
        return self.writer.write(data)

    




def pipe(*, bufsize : int = STREAM_PACKET_SIZE * 4) -> _ContextTuple[PipeReader, PipeWriter]:
    """
    Creates a pipe. Returns a (PipeReader, PipeWriter) pair to that pipe.
    
    Usage:
    >>> r, w = pipe()
    >>> w.write(b"Hey")
    3
    >>> r.read(3)
    b'Hey'
    >>> w.write(b"Hello")
    5
    >>> w.close()
    >>> r.read(10)
    b'Hello'
    >>> r.read(5)
    b''
    >>> r.read(5)
    Traceback (most recent call last):
        raise IOClosedError("Pipe has been closed")
    IOClosedError: Pipe has been closed

    Note that they can be pickled:

    >>> r, w = pipe()
    >>> from pickle import *
    >>> r = loads(dumps(r))     # You can send a pickle to a parent/child process
    >>> with w:     # w is closed at context exit
    ...     w.write(b"Hey")
    ... 
    >>> r.read(10)
    b'Hey'

    You can also directly use this function in a context manager:

    >>> with pipe() as (r, w):
    ...     w.write(b"Hey")
    ...     r.read(3)
    ... 
    3
    b'Hey'

    The keyword bufsize argument sets the size of the internal buffer used by the pipe.
    """
    if not isinstance(bufsize, int):
        raise TypeError(f"Expected int for bufsize, got '{type(bufsize).__name__}'")
    if bufsize <= 0:
        raise ValueError(f"Expected positive nonzero integer for bufsize, got {bufsize}")
    from os import urandom
    while True:         # In case we are unlucky enough to pick an existing name...
        try:
            array = _CircularSharedArray(f"Pipe-{urandom(64).hex()}", True, bufsize)
            break
        except:
            pass
    r = PipeReader(array)
    w = PipeWriter(array)
    r.dual = w
    return _ContextTuple((r, w))

def bridge(*, bufsize : int = STREAM_PACKET_SIZE * 4) -> _ContextTuple[Duplex, Duplex]:
    """
    Creates a pair of connected Duplexes. Use them as file objects.
    
    Usage:
    >>> d1, d2 = bridge()
    >>> d1.write(b"Hey")
    3
    >>> d2.read(3)
    b'Hey'
    >>> d2.write(b"Hello")
    5
    >>> d2.close()
    >>> d1.read(10)
    b'Hello'
    >>> d1.read(5)
    b''
    >>> d1.read(5)
    Traceback (most recent call last):
        raise IOClosedError("Pipe has been closed")
    IOClosedError: Pipe has been closed
    >>> d1.write(b"Are you still there?")
    Traceback (most recent call last):
        raise IOClosedError("Pipe has been closed")
    IOClosedError: Pipe has been closed

    Note that they can be pickled:

    >>> d1, d2 = bridge()
    >>> from pickle import *
    >>> d1 = loads(dumps(d1))       # You can send a pickle to a parent/child process
    >>> with d2:        # d2 is closed at context exit
    ...     d2.write(b"Hey")
    ... 
    >>> d1.read(10)
    b'Hey'
    
    You can also directly use this function in a context manager:

    >>> with bridge() as (d1, d2):
    ...     d1.write(b"Hey")
    ...     d2.read(3)
    ... 
    3
    b'Hey'

    The keyword bufsize argument sets the size of the two internal buffers used by the bridge.
    """
    if not isinstance(bufsize, int):
        raise TypeError(f"Expected int for bufsize, got '{type(bufsize).__name__}'")
    if bufsize <= 0:
        raise ValueError(f"Expected positive nonzero integer for bufsize, got {bufsize}")
    from os import urandom
    while True:         # In case we are unlucky enough to pick an existing name...
        try:
            array1 = _CircularSharedArray(f"Pipe-{urandom(64).hex()}", True, bufsize)
            break
        except:
            pass
    while True:         # In case we are unlucky enough to pick an existing name...
        try:
            array2 = _CircularSharedArray(f"Pipe-{urandom(64).hex()}", True, bufsize)
            break
        except:
            pass
    d1 = Duplex(array1, array2)
    d2 = Duplex(array2, array1)
    d1.dual = d2
    return _ContextTuple((d1, d2))





module_ready.set()
reader_thread_ready.wait()
writer_thread_ready.wait()

del SharedMemory, RLock, Thread, ContextManager, TypeVar, WeakSet, STREAM_PACKET_SIZE, BytesIO, BytesIOBase, BytesReader, BytesWriter, Budget, exclusive, Event, module_ready, reader_thread_ready, writer_thread_ready