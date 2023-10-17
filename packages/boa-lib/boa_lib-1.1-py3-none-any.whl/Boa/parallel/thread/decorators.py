"""
This module implements useful multithreading decorators.
"""

from typing import Callable, Concatenate, ParamSpec, TypeVar

__all__ = ["exclusive", "critical", "self_exclusive", "self_critical"]





T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")

def exclusive(f : Callable[P, R]) -> Callable[P, R]:
    """
    Transforms a function into a thread exclusive/critical function:
    At most one thread can execute its code at the same time while others will wait.

    Implemented using threading.RLock (so recursion is allowed).
    """
    from .synchronization import ExclusionGroup
    return ExclusionGroup()(f)
    
critical = exclusive

def self_exclusive(f : Callable[Concatenate[T, P], R]) -> Callable[Concatenate[T, P], R]:
    """
    Transforms a method into a thread exclusive/critical method for each instance:
    At most one thread can execute its code at the same time on the same instance while others will wait.

    Implemented using threading.RLock (so recursion is allowed).
    """
    from .synchronization import ExclusionGroup
    return ExclusionGroup().per_instance(f)

self_critical = self_exclusive





del T, R, P, Callable, Concatenate, ParamSpec, TypeVar