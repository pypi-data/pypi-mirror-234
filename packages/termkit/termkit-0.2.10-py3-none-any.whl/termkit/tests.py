"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from typing import Union

from termkit.core import Termkit


class TermkitRunner:
    captured_output: str
    exception: Union[Exception, SystemExit]
    exit_code: int
    app: Termkit

    def __init__(self, app: Termkit):
        self.app = app

    def run(self, *args):
        captured_output = io.StringIO()
        sys.argv = ["termkit-runner", *args]
        with redirect_stdout(captured_output), redirect_stderr(captured_output):
            try:
                self.app()
            except SystemExit as e:
                self.exit_code = e.code
                self.exception = e
            except Exception as e:
                self.exception = e
            finally:
                self.captured_output = captured_output.getvalue()
