"""
This module defines the exception classes for the parallel package.
"""

__all__ = ["FutureError", "UnreachableFuture", "CancelledFuture", "TooFarFutureError", "FutureSetError", "FutureUnsetError"]





class FutureError(Exception):

    """
    Common base class for all Future-related exceptions.
    """

    def __init__(self, *args: object) -> None:
        try:
            from .abc import Future
            argv = list(args)
            self.__future = None
            for i, o in enumerate(argv):
                if isinstance(o, Future):
                    self.__future = o
                    argv.pop(i)
                    break
        except:
            argv = args
        super().__init__(*argv)
    
    @property
    def future(self):
        """
        The Future that caused this exception.
        """
        return self.__future





class UnreachableFuture(FutureError):

    """
    This class of exception is thrown when a Future is known to be unreachable (i.e. when it will never be set).
    """
    




class CancelledFuture(UnreachableFuture):

    """
    Subclass of UnreachableFuture that is raised by Futures when the Future.cancel() method is called.
    """





class TooFarFutureError(UnreachableFuture):

    """
    Subclass of UnreachableFuture that is raised by Futures when Future.wait() or Future.result() hit their timeout.
    """





class FutureSetError(FutureError):

    """
    This exception is raised when trying to set an already-set Future.
    """





class FutureUnsetError(FutureError):

    """
    This exception is raised when accessing attributes only set Futures have.
    """