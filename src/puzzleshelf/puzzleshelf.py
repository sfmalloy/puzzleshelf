import functools
from io import TextIOWrapper
from os import PathLike
from pathlib import Path
from string import Template
from typing import Any, Callable, Hashable


class Run:
    solution: Any
    time: float


class PuzzleShelf:
    name: str
    __solvers: dict[Hashable, Callable]
    __parsers: dict[Hashable, Callable[[str], Any]]

    __input_path: str
    __input_filename_pattern: Template

    def __init__(
        self,
        name: str,
        *,
        input_path: PathLike = Path('./inputs'),
        input_filename_pattern: Template = Template('day${id}.txt'),
    ):
        """
        PuzzleShelf base class.

        :param name: Name of the group of puzzles on this shelf.
        :type name: str

        :param input_path: Path to input files
        :type input_path: str

        :param input_filename_pattern: Pattern for input filenames.
        :type input_filename_pattern: Template
        """
        self.name = name
        self.__solvers = dict()
        self.__parsers = dict()

        self.__input_path = Path(input_path)
        self.__input_filename_pattern = input_filename_pattern

    @property
    def input_path(self) -> str:
        return self.__input_path

    @property
    def input_filename_pattern(self) -> Template:
        return self.__input_filename_pattern

    def run(self, id: Hashable, *, part: int | None = None):
        parser = self.__parsers.get(id)
        if parser:
            substitutions = {'id': id}
            if part:
                substitutions['part'] = part
            path = self.input_filename_pattern.safe_substitute(substitutions)
            filepath = self.__input_path / path
            args = parser(filepath)
        else:
            args = {}

        solver = self.__solvers.get(id)
        return solver(*args)

    def solver(self, id: int):
        def decorator(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                return fn(*args, **kwargs)

            self.__solvers[id] = wrapper

        return decorator

    def parser(self, id: int, part: int | None = None):
        def decorator(fn: Callable[[TextIOWrapper], Any]):
            @functools.wraps(fn)
            def wrapper(filepath: str):
                with open(filepath) as input_file:
                    val = fn(input_file)
                if not isinstance(val, tuple):
                    return (val,)
                return val

            self.__parsers[id] = wrapper

        return decorator
