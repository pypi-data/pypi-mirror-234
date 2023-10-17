"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

import argparse
import inspect
import typing

from termkit.arguments import _TermkitArgument
from termkit.formatters import TermkitDefaultFormatter
from termkit.utils import get_param_help

__BUILTIN_TYPES__ = [str, int, float, complex, bool]


class TermkitParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, add_help=False)

        self._optionals.title = "Options"
        self._positionals.title = "Positionals"

        self.add_argument(
            "-h", "--help", action="help", default=argparse.SUPPRESS, help="Show this help message and exit"
        )

        if kwargs.get("formatter_class", None) is None:
            self.formatter_class = TermkitDefaultFormatter


class ArgumentHandler:
    def __init__(self, parser: argparse.ArgumentParser, func: typing.Callable):
        self.parser = parser
        self._func = func
        self.parameters = inspect.signature(func).parameters

    def parse(self, param_name: str):
        param = self.parameters.get(param_name)
        param_type = self._get_parameter_type(param_name)
        param_help = get_param_help(inspect.getdoc(self._func), param_name)

        # f(param (= ...))
        if param.annotation is inspect.Parameter.empty:
            # f(param)
            if param.default is inspect.Parameter.empty:
                self._populate_implicit_positional(param_name, param_type, help=param_help)
            # f(param = <default>)
            else:
                if type(param.default) in __BUILTIN_TYPES__:
                    self._populate_implicit_option(param_name, param_type, help=param_help)

        # f(param : <annotation> (= <default>))
        else:
            # f(param : <annotation>)
            if param.default is inspect.Parameter.empty:
                if param.annotation in __BUILTIN_TYPES__:
                    self._populate_implicit_positional(param_name, param_type, help=param_help)

                elif typing.get_origin(param.annotation) is typing.Annotated:
                    _type, option = typing.get_args(param.annotation)
                    if isinstance(option, _TermkitArgument):
                        option._populate(self.parser, dest=param_name, help=param_help)

            # f(param : <annotation> = <default>)
            else:
                if param.annotation in __BUILTIN_TYPES__:
                    self._populate_implicit_option(param_name, param_type, help=param_help)

    def _populate_implicit_positional(self, param_name: str, param_type: type, help: str):
        self.parser.add_argument(param_name, type=param_type, help=help)

    def _populate_implicit_option(self, param_name: str, param_type: type, help: str):
        param = self.parameters.get(param_name)
        self.parser.add_argument(f"--{param_name}", type=param_type, default=param.default, help=help)

    def _get_parameter_type(self, param_name: str):
        param = self.parameters.get(param_name)

        # f(param (= ...))
        if param.annotation is inspect.Parameter.empty:
            # f(param)
            if param.default is inspect.Parameter.empty:
                return str
            # f(param = <default>)
            else:
                if type(param.default) in __BUILTIN_TYPES__:
                    return type(param.default)
                elif isinstance(param.default, _TermkitArgument):
                    return param.default.type

        # f(param : <annotation> (= ...))
        else:
            # f(param : <annotation>)
            if param.default is inspect.Parameter.empty:
                if param.annotation in __BUILTIN_TYPES__:
                    return param.annotation
                elif isinstance(param.annotation, _TermkitArgument):
                    raise SyntaxError("Termkit argument cannot be set from annotation")

            # f(param : <annotation> = <default>)
            else:
                if param.annotation in __BUILTIN_TYPES__:
                    return param.annotation
                elif isinstance(param.annotation, _TermkitArgument):
                    raise SyntaxError("Termkit argument cannot be set from annotation")
