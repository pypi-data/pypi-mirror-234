import argparse
import sys

import requests

class DebugAction(argparse.Action):
    """This action turns on the DEBUG flags so we get coverage of the debug code."""
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        """This is called if the --debug-mode option is passed to pytest."""
        if option_string in self.option_strings:
            # do something to turn on debug mode
            pass


def pytest_addoption(parser):
    parser.addoption(
        "--performance", action="store_true", help="run performance tests"
    )
    parser.addoption(
        "--debug-mode", action=DebugAction, help="turn on DEBUG mode while testing"
    )

def pytest_sessionfinish(session, exitstatus):
    """Hook called after whole test run finished, right before returning
    the exit status to the system."""

    DESTDIR = "docs/"  # physical

    if sys.implementation.name == "pypy":
        py = "pypy"
    else:
        py = "py"
    if exitstatus == 0:
        status = "passing"
        color = "success"
    else:
        status = "failed"
        color = "critical"
    name = f"{py}{sys.version_info.major}{sys.version_info.minor}"

    badge = requests.get(
        f"https://img.shields.io/badge/{name}-{status}-{color}"
    ).text

    filename = f"_images/badge-{name}.svg"
    with open(f"{DESTDIR}{filename}", "w") as dest:
        dest.write(badge)
        print(f"{filename}")
