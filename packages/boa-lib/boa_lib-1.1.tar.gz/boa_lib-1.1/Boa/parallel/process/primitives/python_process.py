import sys
from os import fdopen, getpid

from Viper.pickle_utils import WhiteListUnpickler
from Viper.abc.io import IOClosedError

from ....pipes import _CircularSharedArray, Duplex, PipeReader, PipeWriter

r = int(sys.argv[1])
parent_pid = int(sys.argv[2])

try:
    if sys.platform == "win32":     # In the case of Windows, we receive a handle that only exists in the parent process. Duplicate it and create a file descriptor

        from msvcrt import open_osfhandle

        from _winapi import (DUPLICATE_SAME_ACCESS, PROCESS_DUP_HANDLE,
                            SYNCHRONIZE, DuplicateHandle, GetCurrentProcess,
                            OpenProcess)

        parent_process = OpenProcess(
            SYNCHRONIZE | PROCESS_DUP_HANDLE,
            False,
            parent_pid
        )

        pipe_handle = DuplicateHandle(
            parent_process,
            r,
            GetCurrentProcess(),
            0,
            False,
            DUPLICATE_SAME_ACCESS | SYNCHRONIZE
            )
        
        r = open_osfhandle(pipe_handle, 0)    

    unp = WhiteListUnpickler()
    unp.allow(Duplex, PipeReader, PipeWriter, _CircularSharedArray)

    with fdopen(r, "rb") as from_parent:
        
        data_size = int.from_bytes(from_parent.read(8), "little")
        unp << from_parent.read(data_size)
        child_pipe : Duplex = unp.load()

        child_pipe.write(b"\1")

    child_pipe.write(getpid().to_bytes(8, "little"))

    from .process import ParentProcess
    from .workers import PythonChild
    ParentProcess().is_python = True
    ParentProcess().pid = int.from_bytes(child_pipe.read(8), "little")

    try:

        while True:
            bflag = child_pipe.read(1)
            if not bflag:
                raise IOClosedError("Remote connection has been closed")
            flag = bflag[0]

            action = PythonChild._get_child_action(flag)
            if action:
                action(child_pipe)
    
    except IOClosedError:
        pass

except:
    raise
