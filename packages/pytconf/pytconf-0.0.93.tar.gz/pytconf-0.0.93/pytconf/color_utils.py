import os
from termcolor import colored, cprint


def print_highlight(text):
    cprint(text=text, color="white", attrs=["bold"])


def print_warn(text):
    cprint(text=text, color="red", attrs=["bold"])


def print_error(text):
    cprint(text=text, color="red", attrs=["bold"])


def print_title(text):
    cprint(text=text, color="green", attrs=[])


def color_hi(text):
    return colored(text=text, color="white", attrs=["bold"])


def color_warn(text):
    return colored(text=text, color="red", attrs=["bold"])


def color_ok(text):
    return colored(text=text, color="green", attrs=["bold"])


def identity(text):
    return text


color = "PYTCONF_DISABLE_COLORS" not in os.environ


if not color:
    print_highlight = print  # noqa: F811
    print_warn = print  # noqa: F811
    print_error = print  # noqa: F811
    print_title = print  # noqa: F811
    color_hi = identity  # noqa: F811
    color_warm = identity  # noqa: F811
    color_ok = identity  # noqa: F811
