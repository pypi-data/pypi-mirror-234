# PYTHON_ARGCOMPLETE_OK
"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import abc
import argparse
import inspect
import os
import sys
import typing

from termkit.parser import ArgumentHandler, TermkitParser
from termkit.utils import filter_args, strip_doc

try:
    import argcomplete

    __ARGCOMPLETE__ = True
except ImportError:
    __ARGCOMPLETE__ = False


class _TermkitComponent:
    name: str
    help: str

    @property
    def single_line_help(self):
        return self.help.split("\n")[0]

    @abc.abstractmethod
    def _populate(self, parser: argparse.ArgumentParser):
        ...


class _Command(_TermkitComponent):
    def __init__(self, callback: typing.Callable, name: str = None):
        self.callback = callback
        if name is None:
            name = callback.__name__
        self.name = name

        self.help = inspect.getdoc(callback)
        if self.help is None:
            self.help = ""

        self.help = strip_doc(self.help)

    def _populate(self, parser: argparse.ArgumentParser):
        argument_handler = ArgumentHandler(parser, self.callback)
        for param_name in argument_handler.parameters.keys():
            argument_handler.parse(param_name)


class Termkit(_TermkitComponent):
    def __init__(
        self,
        name: str = os.path.basename(sys.argv[0]),
        description: typing.Optional[str] = None,
        callbacks: typing.Optional[typing.List[typing.Callable]] = None,
        childs: typing.Optional[typing.Dict] = None,
    ):
        self._childs = []
        self._callbacks = []
        self._parser = TermkitParser(prog=name, description=description)
        self._populated = False

        self.name = name
        self.help = description if description is not None else ""
        self.ctx = dict()

        if callbacks is not None and isinstance(callbacks, typing.Iterable):
            for callback in callbacks:
                self.add_callback(callback)

        if childs is not None and isinstance(childs, typing.Dict):
            for child_name, callback_or_app in childs.items():
                self.add(callback_or_app, child_name)

    @property
    def _child_names(self):
        return [c.name for c in self._childs]

    def add(self, app_or_command: typing.Union[Termkit, typing.Callable], name: typing.Optional[str] = None):
        if isinstance(app_or_command, Termkit):
            child = app_or_command
            self.ctx.update({child.name: child.ctx})
        elif inspect.isfunction(app_or_command):
            child = _Command(app_or_command, name)
        else:
            raise TypeError(f"Cannot add object of type '{type(app_or_command)}' to Termkit application.")

        if name is not None:
            child.name = name

        if child.name in self._child_names:
            raise ValueError(f"Name '{child.name}' already taken in '{self.name}' application.")

        self._childs.append(child)

    def command(self, name: str = None):
        def decorator(func: typing.Callable):
            self.add(func, name)
            return func

        return decorator

    def add_callback(self, func: typing.Callable):
        if inspect.isfunction(func):
            self._callbacks.append(_Command(func, func.__name__ + "_CALLBACK"))
        else:
            raise ValueError(f"Cannot add '{func}' as callback, function is required.")

    def callback(self):
        def decorator(func: typing.Callable):
            self.add_callback(func)
            return func

        return decorator

    def _populate(self, parser: argparse.ArgumentParser):
        if not self._populated:
            if len(self._callbacks) > 0:
                parser.add_argument(
                    "_TERMKIT_CALLBACKS", action="store_const", const=self._callbacks, help=argparse.SUPPRESS
                )
                for callback in self._callbacks:
                    callback._populate(parser)

            if len(self._childs) > 0:
                sub_parser = parser.add_subparsers(title="Commands", metavar="COMMAND")
                for child in self._childs:
                    command_parser = sub_parser.add_parser(
                        name=child.name, help=child.single_line_help, description=child.help
                    )
                    if isinstance(child, _Command):
                        command_parser.add_argument(
                            "_TERMKIT_COMMAND",
                            action="store_const",
                            const=child.callback,
                            help=argparse.SUPPRESS,
                        )
                    if isinstance(child, Termkit):
                        child._callbacks = self._callbacks + child._callbacks

                    child._populate(command_parser)

        self._populated = True

    def __call__(self, *args, **kwargs):
        self._populate(self._parser)
        if __ARGCOMPLETE__:
            argcomplete.autocomplete(self._parser)
        arguments = self._parser.parse_args()
        if hasattr(arguments, "_TERMKIT_CALLBACKS"):
            for callback in arguments._TERMKIT_CALLBACKS:
                callback.callback(**filter_args(arguments, callback.callback))

        if hasattr(arguments, "_TERMKIT_COMMAND"):
            arguments._TERMKIT_COMMAND(**filter_args(arguments, arguments._TERMKIT_COMMAND))

        sys.exit(0)
