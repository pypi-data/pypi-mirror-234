import argparse
import typing


class _TermkitGroup:
    def __init__(self):
        self.reg = dict()

    def register(self, parser, argparse_group):
        self.reg[id(parser)] = argparse_group


class ArgumentGroup(_TermkitGroup):
    def __init__(self, name: str, description: typing.Optional[str] = None):
        super().__init__()
        self.name = name
        self.description = description


class MutuallyExclusiveGroup(_TermkitGroup):
    def __init__(self, required: bool = False, parent: ArgumentGroup = None):
        super().__init__()
        self.required = required
        self.parent = parent


def get_parser_from_group(parser: argparse.ArgumentParser, group: typing.Optional[_TermkitGroup]):
    if group is None:
        return parser

    if isinstance(group, ArgumentGroup):
        if group.reg.get(id(parser), None) is None:
            argparse_group = parser.add_argument_group(group.name, group.description)
            # Add new group before options
            parser._action_groups.insert(-2, parser._action_groups.pop(-1))
            group.register(parser, argparse_group)
        return group.reg.get(id(parser))

    if isinstance(group, MutuallyExclusiveGroup):
        if group.reg.get(id(parser), None) is None:
            if group.parent is not None:
                parent_group = get_parser_from_group(parser, group.parent)
                argparse_group = parent_group.add_mutually_exclusive_group(required=group.required)

                group.register(parser, argparse_group)
            else:
                argparse_group = parser.add_mutually_exclusive_group(required=group.required)
                group.register(parser, argparse_group)
        return group.reg.get(id(parser))
