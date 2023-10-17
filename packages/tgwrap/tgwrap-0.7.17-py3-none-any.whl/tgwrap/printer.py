"""
Simple class for printing console messages
"""
import sys
import shutil
import click

class Printer():
    """ A simple class for printing nice messages """
    def __init__(
        self,
        verbose: bool,
        ):

        self._print_verbose = verbose

    @property
    def print_verbose(self):
        return self._print_verbose

    def line(self):
        width = 80
        try:
            width, _ = shutil.get_terminal_size() 
        except OSError as e:
            pass
        click.secho("-" * width, file=sys.stderr)

    def header(self, msg, print_line_before=False, print_line_after=False):
        msg = msg.strip() if isinstance(msg, str) else msg
        self.line() if print_line_before else None
        click.secho('\n' + msg, bold=True, file=sys.stderr)
        self.line() if print_line_after else None

    def verbose(self, msg, print_line_before=False, print_line_after=False):
        if self._print_verbose:
            msg = msg.strip() if isinstance(msg, str) else msg
            self.line() if print_line_before else None
            print(msg, flush=True, file=sys.stderr)
            self.line() if print_line_after else None

    def normal(self, msg, print_line_before=False, print_line_after=False):
        msg = msg.strip() if isinstance(msg, str) else msg
        self.line() if print_line_before else None
        print(msg, flush=True, file=sys.stderr)
        self.line() if print_line_after else None

    def bold(self, msg, print_line_before=False, print_line_after=False):
        msg = msg.strip() if isinstance(msg, str) else msg
        self.line() if print_line_before else None
        click.secho('\n' + msg, bold=True, file=sys.stderr)
        self.line() if print_line_after else None

    def warning(self, msg, print_line_before=False, print_line_after=False):
        msg = msg.strip() if isinstance(msg, str) else msg
        self.line() if print_line_before else None
        click.secho(msg, fg="yellow", bold=True, file=sys.stderr)
        self.line() if print_line_after else None

    def error(self, msg, print_line_before=False, print_line_after=False):
        msg = msg.strip() if isinstance(msg, str) else msg
        self.line() if print_line_before else None
        click.secho(msg, fg="red", bold=True, file=sys.stderr)
        self.line() if print_line_after else None

    def success(self, msg, print_line_before=False, print_line_after=False):
        msg = msg.strip() if isinstance(msg, str) else msg
        self.line() if print_line_before else None
        click.secho(msg, fg="green", bold=True, file=sys.stderr)
        self.line() if print_line_after else None

