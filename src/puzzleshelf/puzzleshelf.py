import functools
from typing import Any, Callable


class Run:
    solution: Any
    time: float


class PuzzleShelf:
    name: str
    __solvers: dict[int, Callable]
    __parsers: dict[int, Callable]

    def __init__(self, name: str):
        self.name = name
        self.__solvers = dict()
        self.__parsers = dict()

    def run(self, id: int, *, part: int | None = None):
        p = self.__parsers.get(id)
        args = p()

        s = self.__solvers.get(id)
        return s(*args)

    def solver(self, id: int):
        def decorator(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                return fn(*args, **kwargs)

            self.__solvers[id] = wrapper

        return decorator

    def parser(self, id: int, part: int | None = None):
        def decorator(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                val = fn(*args, **kwargs)
                if not isinstance(val, tuple):
                    return (val,)
                return val

            self.__parsers[id] = wrapper

        return decorator
