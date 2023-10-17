"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT

The following imports are designed to provide convenient access to frequently used modules and functionality.
These imports help streamline the code and improve readability by reducing the need to prefix module names.
"""

from termkit.arguments import Positional  # noqa: F401
from termkit.arguments import Nargs, CounterFlag, Flag, Option  # noqa: F401
from termkit.core import Termkit  # noqa: F401
from termkit.groups import ArgumentGroup, MutuallyExclusiveGroup  # noqa: F401
from termkit.prompt import Prompt  # noqa: F401
