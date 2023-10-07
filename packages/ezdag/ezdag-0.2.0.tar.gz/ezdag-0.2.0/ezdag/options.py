# Copyright (C) 2020 Patrick Godwin
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# <https://mozilla.org/MPL/2.0/>.
#
# SPDX-License-Identifier: MPL-2.0

from collections.abc import Iterable
from dataclasses import dataclass, field
import os
from typing import Callable, List, Optional, Union


_PROTECTED_CONDOR_VARS = {"input", "output", "rootdir"}


@dataclass
class Argument:
    """Defines a command-line argument (positional).

    This provides some extra functionality over defining command line
    argument explicitly, in addition to some extra parameters which
    sets how condor interprets how to handle them within the DAG
    and within submit descriptions.

    Parameters
    ----------
    name
        The option name. Since this is a positional argument, it is not
        used explicitly in the command, but is needed to define
        variable names within jobs.
    argument
        The positional argument value(s) used in a command.
    track
        Whether to track files defined here and used externally within
        jobs to determine parent-child relationships when nodes specify
        this option as an input or output. On by default.
    remap
        Whether to allow remapping of output files being transferred.
        If set, output files will be moved to their target directories
        after files are transferred back. This is done to avoid issues
        where the target directories are available on the submit node
        but not on the exectute node. On by default.
    suppress
        Whether to hide this option. Used externally within jobs to
        determine whether to define job arguments. This is typically used
        when you want to track file I/O used by a job but isn't directly
        specified in their commands. Off by default.
    suppress_with_remap
        Same as suppress but allowing transfer remaps to still occur.
        Used when you want to track file output which is not directly
        specified in their command but whose file locations changed
        compared to their inputs. Off by default.

    Examples
    --------
    >>> Argument("command", "run").vars()
    'run'

    >>> files = ["input_1.txt", "input_2.txt"]
    >>> Argument("input-files", files).vars()
    'input_1.txt input_2.txt'

    """

    name: str
    argument: Union[int, float, str, List]
    track: bool = True
    remap: bool = True
    suppress: bool = False
    suppress_with_remap: bool = False
    _args: List[str] = field(init=False)

    def __post_init__(self) -> None:
        # check against list of protected condor names/characters,
        # rename condor variables name to avoid issues
        self.condor_name = self.name.replace("-", "_")
        if self.condor_name in _PROTECTED_CONDOR_VARS:
            self.condor_name += "_"

        if isinstance(self.argument, str) or not isinstance(self.argument, Iterable):
            self.argument = [self.argument]
        self._args = [str(arg) for arg in self.argument]

        # set options that control other options
        if self.suppress:
            self.remap = False
        elif self.suppress_with_remap:
            self.suppress = True

    @property
    def _arg_basename(self) -> List[str]:
        return [os.path.basename(arg) for arg in self._args]

    def args(self) -> List[str]:
        return self._args

    def vars(self, basename: Union[bool, Callable[[str], bool]] = False) -> str:
        if callable(basename):
            # if basename is a function, determine whether the argument's
            # basename should be used based on calling basename(argument)
            args = []
            for arg in self._args:
                if basename(arg):
                    args.append(os.path.basename(arg))
                else:
                    args.append(arg)
            return " ".join(args)
        elif basename:
            return " ".join(self._arg_basename)
        else:
            return " ".join(self._args)

    def files(self, basename: bool = False) -> str:
        return ",".join(self._arg_basename) if basename else ",".join(self._args)

    def remaps(self) -> str:
        return ";".join(
            [
                f"{base}={arg}"
                for base, arg in zip(self._arg_basename, self._args)
                if base != arg
            ]
        )


@dataclass
class Option:
    """Defines a command-line option (long form).

    This provides some extra functionality over defining command line
    options explicitly, in addition to some extra parameters which
    sets how condor interprets how to handle them within the DAG
    and within submit descriptions.

    Parameters
    ----------
    name
        The option name to be used in a command.
    argument
        The argument value(s) used in a command.
    track
        Whether to track files defined here and used externally within
        jobs to determine parent-child relationships when nodes specify
        this option as an input or output. On by default.
    remap
        Whether to allow remapping of output files being transferred.
        If set, output files will be moved to their target directories
        after files are transferred back. This is done to avoid issues
        where the target directories are available on the submit node
        but not on the exectute node. On by default.
    suppress
        Whether to hide this option. Used externally within jobs to
        determine whether to define job arguments. This is typically used
        when you want to track file I/O used by a job but isn't directly
        specified in their commands. Off by default.
    suppress_with_remap
        Same as suppress but allowing transfer remaps to still occur.
        Used when you want to track file output which is not directly
        specified in their command but whose file locations changed
        compared to their inputs. Off by default.

    Examples
    --------
    >>> Option("verbose").vars()
    '--verbose'

    >>> Option("input-type", "file").vars()
    '--input-type file'

    >>> Option("ifos", ["H1", "L1", "V1"]).vars()
    '--ifos H1 --ifos L1 --ifos V1'

    """

    name: str
    argument: Optional[Union[int, float, str, List]] = None
    track: Optional[bool] = True
    remap: Optional[bool] = True
    suppress: Optional[bool] = False
    suppress_with_remap: Optional[bool] = False
    _args: List[str] = field(init=False)

    def __post_init__(self) -> None:
        # check against list of protected condor names/characters,
        # rename condor variables name to avoid issues
        self.condor_name = self.name.replace("-", "_")
        if self.condor_name in _PROTECTED_CONDOR_VARS:
            self.condor_name += "_"

        if self.argument is not None:
            if isinstance(self.argument, str) or not isinstance(
                self.argument, Iterable
            ):
                self.argument = [self.argument]
            self._args = [str(arg) for arg in self.argument]

        # set options that control other options
        if self.suppress:
            self.remap = False
        elif self.suppress_with_remap:
            self.suppress = True

    @property
    def _arg_basename(self) -> List[str]:
        return [os.path.basename(arg) for arg in self._args]

    def args(self) -> List[str]:
        return self._args

    def vars(self, basename: Union[bool, Callable[[str], bool]] = False) -> str:
        if self.argument is None:
            return f"--{self.name}"
        elif callable(basename):
            # if basename is a function, determine whether the argument's
            # basename should be used based on calling basename(argument)
            args = []
            for arg in self._args:
                if basename(arg):
                    args.append(f"--{self.name} {os.path.basename(arg)}")
                else:
                    args.append(f"--{self.name} {arg}")
            return " ".join(args)
        elif basename:
            return " ".join([f"--{self.name} {arg}" for arg in self._arg_basename])
        else:
            return " ".join([f"--{self.name} {arg}" for arg in self._args])

    def files(self, basename: bool = False) -> str:
        return ",".join(self._arg_basename) if basename else ",".join(self._args)

    def remaps(self) -> str:
        return ";".join(
            [
                f"{base}={arg}"
                for base, arg in zip(self._arg_basename, self._args)
                if base != arg
            ]
        )
