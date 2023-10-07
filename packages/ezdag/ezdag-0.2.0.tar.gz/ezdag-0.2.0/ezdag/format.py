# Copyright (C) 2023 Cardiff University
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# <https://mozilla.org/MPL/2.0/>.
#
# SPDX-License-Identifier: MPL-2.0

"""HTCondor submit command formatting utilities.
"""

from __future__ import annotations

from typing import (Any, Callable, Iterable)


def _separated_factory(delimiter: str) -> Callable:
    """Factory function to define a delimiter-joiner function.
    """
    def _joiner(value: Iterable[Any]) -> str:
        return delimiter.join(map(str, value))
    return _joiner


_comma_separated = _separated_factory(", ")
_space_separated = _separated_factory(" ")
_semicolon_separated = _separated_factory("; ")


def _format_argument(arg: str) -> str:
    """Format a single command argument for inclusion in the condor_submit
    ``arguments`` command.

    According to the condor_submit _New Syntax_ description.
    """
    return "'{}'".format(
        arg.replace('"', '""').replace("'", "''"),
    )


def _format_arguments(value: Iterable[str]) -> str:
    """Format an iterable of command arguments for inclusion in the condor_submit
    ``arguments`` command.

    According to the condor_submit _New Syntax_ description.
    """
    return "\"{}\"".format(" ".join(map(_format_argument, value)))


def _format_environment(value: dict[str, Any]) -> str:
    """Format a `dict` of environment settings for the condor_submit
    ``environment`` command.
    """
    return "\"{}\"".format(" ".join(
        f"{key}='{value}'" for key, value in value.items()
    ))


def _format_classad_item(value: Any) -> str:
    """Format a single classad expression item.
    """
    return f"({value})"


def _format_classad_boolean_expression(
    value: Iterable[Any],
    operator: str = "&&",
) -> str:
    """Format an iterable of requirements expressions as a ClassAd Boolean
    Expression for the condor_submit ``requirements`` command, or similar,
    using the relevant operator.
    """
    return " {operator} ".join(map(_format_classad_item, value))


def _semicolon_separated_pairs(value: dict[str, Any]) -> str:
    """Format a dict as a semicolon-separated list of key, value pairs
    for the condor_submit ``transfer_output_remaps`` command, or similar.
    """
    def _format_item(key):
        val = value[key]
        if val is None:
            return key
        return f"{key}={val}"

    return "\"{}\"".format("; ".join(map(_format_item, value)))


DICT_FORMATTERS: dict[str, Callable] = {
    "environment": _format_environment,
    "transfer_output_remaps": _semicolon_separated_pairs,
    "transfer_plugins": _semicolon_separated_pairs,
}
LIST_FORMATTERS: dict[str, Callable] = {
    "arguments": _format_arguments,
    "getenv": _comma_separated,
    "requirements": _format_classad_boolean_expression,
    "transfer_checkpoint_files": _comma_separated,
    "transfer_input_files": _comma_separated,
    "transfer_output_files": _comma_separated,
}


def _format_condor_command_value(
    command: str,
    value: Any,
) -> str:
    """Format a condor submit command value.
    """
    if isinstance(value, dict) and command.lower() in DICT_FORMATTERS:
        return DICT_FORMATTERS[command.lower()](value)
    if isinstance(value, (list, tuple)) and command.lower() in LIST_FORMATTERS:
        return LIST_FORMATTERS[command.lower()](value)

    # special cases for dynamically-named commands
    if isinstance(value, (list, tuple)) and (
        "_oauth_permissions" in command
        or "_oauth_resource" in command
    ):
        return _space_separated(value)

    return str(value)


def format_submit_description(desc: dict[str, Any]) -> dict[str, str]:
    """Format a dictionary of submit description options.

    This method converts 'arbitrary' Pythonic input types for the values of
    condor submit description options into a string for inclusion in a
    condor submit file.
    """
    out = {}
    for key, value in desc.items():
        out[key] = _format_condor_command_value(key, value)
    return out
