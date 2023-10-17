"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

import argparse
import enum
import typing
from abc import abstractmethod
from typing import Optional

from termkit.groups import _TermkitGroup, get_parser_from_group


class Nargs(enum.Enum):
    ONE_OR_DEFAULT = "?"
    ZERO_OR_MANY = "*"
    ONE_OR_MANY = "+"

    def __get__(self, instance, owner):
        return self.value


class _TermkitArgument:
    _ignored_params = ["flags", "group"]

    @abstractmethod
    def _populate(self, parser: argparse.ArgumentParser, dest: str, help: str):
        ...

    @property
    def argparse_params(self):
        out = self.__dict__.copy()
        for item in self._ignored_params:
            if item in out.keys():
                del out[item]
        return out


class Positional(_TermkitArgument):
    def __init__(
        self,
        type: Optional[type] = str,
        metavar: Optional[str] = None,
        nargs: Optional[typing.Union[int, str]] = None,
        choices: Optional[typing.Container] = None,
    ):
        self.type = type
        self.metavar = metavar
        self.nargs = nargs
        self.choices = choices

    def _populate(self, parser: argparse.ArgumentParser, dest: str, help: str):
        parser.add_argument(dest, **self.argparse_params, help=help)


class Option(_TermkitArgument):
    def __init__(
        self,
        *flags: str,
        type: Optional[type] = str,
        metavar: Optional[str] = None,
        required: bool = False,
        default: Optional[typing.Any] = None,
        group: Optional[_TermkitGroup] = None,
        nargs: Optional[typing.Union[int, str]] = None,
        choices: Optional[typing.Container] = None,
    ):
        self.flags = flags
        self.type = type
        self.nargs = nargs
        self.metavar = metavar
        self.required = required
        self.default = default
        self.group = group
        self.choices = choices

    def _populate(self, parser: argparse.ArgumentParser, dest: str, help: str):
        parser = get_parser_from_group(parser, self.group)
        parser.add_argument(*sorted(self.flags, key=len), **self.argparse_params, dest=dest, help=help)


class Flag(_TermkitArgument):
    _ignored_params = ["flags", "type", "group"]

    def __init__(
        self,
        *flags: str,
        store: Optional[typing.Any] = True,
        group: Optional[_TermkitGroup] = None,
    ):
        self.flags = flags
        self.type = None
        self.group = group
        if store is True:
            self.action = "store_true"
        if store is False:
            self.action = "store_false"
        else:
            self.action = "store_const"
            self.const = store

    def _populate(self, parser: argparse.ArgumentParser, dest: str, help: str):
        parser = get_parser_from_group(parser, self.group)
        parser.add_argument(*sorted(self.flags, key=len), **self.argparse_params, dest=dest, help=help)


class CounterFlag(_TermkitArgument):
    _ignored_params = ["flags", "type", "group"]

    def __init__(
        self,
        *flags: str,
        store: Optional[typing.Any] = True,
        group: Optional[_TermkitGroup] = None,
    ):
        self.flags = flags
        self.type = None
        self.group = group

    def _populate(self, parser: argparse.ArgumentParser, dest: str, help: str):
        parser = get_parser_from_group(parser, self.group)
        parser.add_argument(
            *sorted(self.flags, key=len), **self.argparse_params, dest=dest, help=help, default=0, action="count"
        )
