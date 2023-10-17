"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

import argparse
import inspect
import typing

__RESERVED_PREFIXES__ = ["_TERMKIT_"]


def filter_args(ns: argparse.Namespace, callback: typing.Callable) -> typing.Dict:
    out = ns.__dict__.copy()
    params = inspect.signature(callback).parameters.keys()
    for arg in ns.__dict__.keys():
        for reserved_prefix in __RESERVED_PREFIXES__:
            if reserved_prefix in arg or arg not in params:
                del out[arg]
    return out


def strip_doc(doc: str) -> str:
    out = []
    for line in doc.splitlines():
        if len(line) > 0 and line[0] == ":":
            break
        out.append(line)
    return "\n".join(out)


def get_param_help(doc: str, dest: str) -> str:
    if doc is None:
        return ""
    for line in doc.splitlines():
        pre = f":param {dest}:"
        if pre == line[: len(pre)]:
            return "\n  ".join(list(map(lambda o: o.strip(), line[len(pre) :].replace("\\n", "\n").splitlines())))
    return ""
