"""Provide utilities for dealing with functions."""
from typing import Any, List
import inspect


def get_callback_param(command: Any) -> List[str]:
    """Return a list of parameter names in the callback function of a command
    :param command: a function to get the parameters for
    """
    callback = command.callback
    sig = inspect.signature(callback)
    return list(sig.parameters.keys())


def get_callback_defaults(command: Any) -> dict:
    """Return a dictionary of callback defaults."""
    callback = command.callback
    sig = inspect.signature(callback)
    return {
        name: param.default if param.default != param.empty else None
        for name, param in sig.parameters.items()
    }
