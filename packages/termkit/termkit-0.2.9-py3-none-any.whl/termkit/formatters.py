import argparse


class TermkitDefaultFormatter(argparse.RawTextHelpFormatter):
    def __init__(self, prog: str):
        super().__init__(prog, width=120, max_help_position=40)

    def _format_action(self, action: argparse.Action) -> str:
        if isinstance(action, argparse._SubParsersAction):
            subactions = action._get_subactions()
            invocations = [self._format_action_invocation(a) for a in subactions]
            self._subcommand_max_length = max(len(i) for i in invocations)

        if isinstance(action, argparse._SubParsersAction._ChoicesPseudoAction):
            # format subcommand help line
            subcommand = self._format_action_invocation(action)  # type: str
            width = self._subcommand_max_length
            help_text = ""
            if action.help:
                help_text = self._expand_help(action)
            if len(help_text) > 0:
                return "  {} {} {}\n".format(subcommand, "." * (width + 4 - len(subcommand)), help_text)
            else:
                return f"  {subcommand}\n".format(subcommand, width=width)

        elif isinstance(action, argparse._SubParsersAction):
            # process subcommand help section
            msg = ""
            for subaction in action._get_subactions():
                msg += self._format_action(subaction)
            return msg
        else:
            return super(TermkitDefaultFormatter, self)._format_action(action)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            (metavar,) = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append("%s" % option_string)
                parts[-1] += " %s" % args_string
            return ", ".join(parts)
