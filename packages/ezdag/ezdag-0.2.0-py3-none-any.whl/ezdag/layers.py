# Copyright (C) 2020 Patrick Godwin
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# <https://mozilla.org/MPL/2.0/>.
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
import itertools
import os
import shutil
from typing import Any, Dict, List, Optional, Tuple, Union
import warnings

import htcondor
from htcondor import dags

from .format import format_submit_description
from .options import Argument, Option


@dataclass
class Layer:
    """Defines a single layer (or set of related jobs) in an HTCondor DAG.

    Stores submit configuration for a set of nodes as well as
    providing functionality to determine the parent-child
    relationships between nodes.

    Parameters
    ----------
    executable
        The path of the executable to run.
    name
        The human-readable name of this node. Defaults to the basename
        of the executable if not given.
    universe
        The execution environment for a job. Defaults to 'vanilla'.
    retries
        The number of retries given for a job. Defaults to 3.
    transfer_files
        Whether to leverage Condor file transfer for moving around
        files. On by default.
    submit_description
        The submit descriptors representing this set of jobs.
    requirements
        The submit descriptors representing this set of jobs.
        Deprecated in favor for submit_description to avoid confusion,
        as 'requirements' refers to a specific submit descriptor.
        This option will be removed in a future release.
    nodes
        The nodes representing the layer. Nodes can be passed upon
        instantiation or added to the layer after the fact via
        Layer.append(node), Layer.extend(nodes), or Layer += node.

    """

    executable: str
    name: str = ""
    universe: str = "vanilla"
    log_dir: str = "logs"
    retries: int = 3
    transfer_files: bool = True
    requirements: dict = field(default_factory=dict)
    submit_description: Union[dict, htcondor.Submit] = field(default_factory=dict)
    nodes: list = field(default_factory=list)
    inputs: dict = field(init=False, default_factory=dict)
    outputs: dict = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name:
            self.name = os.path.basename(self.executable)
        if self.requirements:
            self.submit_description.update(self.requirements)
            warnings.warn(
                "requirements has been deprecated in favor of submit_description"
                "to avoid confusion and will be removed in a future release",
                DeprecationWarning,
            )
        self.extend(self.nodes)

    def config(
        self,
        formatter: Optional[dags.NodeNameFormatter] = None,
    ) -> Dict[str, Any]:
        """Generates a layer configuration.

        This configuration can be passed directly into an
        htcondor.dags.NodeLayer if desired.

        Parameters
        ----------
        formatter : htcondor.dags.NodeNameFormatter
            Defines how the node names are defined and formatted. Defaults to a
            hex-based formatter with 5 digits.

        """
        # check that nodes are valid
        self.validate()

        # update submit description with defaults + other layer configuration
        submit_description = self._update_submit_defaults(self.submit_description)

        if not formatter:
            formatter = HexFormatter()
        return {
            "name": self.name,
            "submit_description": submit_description,
            "vars": self._vars(formatter),
            "retries": self.retries,
        }

    def append(self, node: Node) -> None:
        """Append a node to this layer."""
        assert isinstance(node.inputs, list)
        assert isinstance(node.outputs, list)
        for input_ in node.inputs:
            self.inputs.setdefault(input_.name, []).append(input_.argument)
        for output in node.outputs:
            self.outputs.setdefault(output.name, []).append(output.argument)
        self.nodes.append(node)

    def extend(self, nodes: Iterable[Node]) -> None:
        """Append multiple nodes to this layer."""
        for node in nodes:
            self.append(node)

    def __iadd__(self, nodes) -> Layer:
        if isinstance(nodes, Iterable):
            self.extend(nodes)
        else:
            self.append(nodes)
        return self

    def validate(self) -> None:
        """Ensure all nodes in this layer are consistent with each other."""
        assert self.nodes, "at least one node must be connected to this layer"

        # check arg names across nodes are equal
        args = [arg.name for arg in self.nodes[0].arguments]
        for node in self.nodes[:-1]:
            assert args == [arg.name for arg in node.arguments]

        # check input/output names across nodes are equal
        inputs = [arg.name for arg in self.nodes[0].inputs]
        for node in self.nodes[:-1]:
            assert inputs == [arg.name for arg in node.inputs]
        outputs = [arg.name for arg in self.nodes[0].outputs]
        for node in self.nodes[:-1]:
            assert outputs == [arg.name for arg in node.outputs]

    @property
    def has_dependencies(self) -> bool:
        """Check if any of the nodes in this layer have dependencies."""
        return any([node.requires for node in self.nodes])

    def _arguments(self) -> str:
        args = [f"$({arg.condor_name})" for arg in self.nodes[0].arguments]
        io_args = []
        io_opts = []
        for arg in itertools.chain(self.nodes[0].inputs, self.nodes[0].outputs):
            if not arg.suppress:
                if isinstance(arg, Argument):
                    io_args.append(f"$({arg.condor_name})")
                else:
                    io_opts.append(f"$({arg.condor_name})")
        return " ".join(itertools.chain(args, io_opts, io_args))

    def _inputs(self) -> str:
        return ",".join([f"$(input_{arg.condor_name})" for arg in self.nodes[0].inputs])

    def _outputs(self) -> str:
        return ",".join(
            [f"$(output_{arg.condor_name})" for arg in self.nodes[0].outputs]
        )

    def _output_remaps(self) -> str:
        return ";".join(
            [f"$(output_{arg.condor_name}_remap)" for arg in self.nodes[0].outputs]
        )

    def _vars(self, formatter: dags.NodeNameFormatter) -> List[Dict[str, str]]:
        allvars = []
        for i, node in enumerate(self.nodes):
            nodevars = {"nodename": formatter.generate(self.name, i)}
            # add arguments which aren't suppressed
            if node.arguments:
                nodevars.update(
                    {
                        arg.condor_name: arg.vars()
                        for arg in node.arguments
                        if not arg.suppress
                    }
                )
            # then add arguments defined as 'inputs'. if file transfer is enabled,
            # also define the $(input_{arg}) variable containing the files
            if node.inputs:
                if self.transfer_files:
                    # adjust file location for input files if they are absolute paths.
                    # condor will transfer the file /path/to/file.txt to the job's
                    # current working directory, so arguments should point to file.txt
                    args = {}
                    for arg in node.inputs:
                        if not arg.suppress:
                            args[f"{arg.condor_name}"] = arg.vars(
                                basename=os.path.isabs
                            )
                    nodevars.update(args)
                    nodevars.update(
                        {f"input_{arg.condor_name}": arg.files() for arg in node.inputs}
                    )
                else:
                    nodevars.update(
                        {
                            f"{arg.condor_name}": arg.vars()
                            for arg in node.inputs
                            if not arg.suppress
                        }
                    )
            # finally, add arguments defined as 'outputs'. if file transfer is
            # enabled, also define the $(output_{arg}) variable containing the
            # files. if argument if not suppressed, some extra hoops are done
            # with remaps to ensure that files are also saved to the right
            # place. the main problem is that when jobs are submitted, the
            # directory structure is present in the submit node but not the
            # execute node, so when a job tries to create a file assuming the
            # directories are there, the job fails. this gets around the issue
            # by writing the files to the root directory then remaps them so
            # they get stored in the right place after the job completes and
            # files are transferred back
            if node.outputs:
                for arg in node.outputs:
                    if not arg.suppress:
                        basename = self.transfer_files and arg.remap
                        nodevars.update(
                            {f"{arg.condor_name}": arg.vars(basename=basename)}
                        )
                    if self.transfer_files:
                        if arg.remap:
                            nodevars.update(
                                {f"output_{arg.condor_name}": arg.files(basename=True)}
                            )
                            nodevars.update(
                                {f"output_{arg.condor_name}_remap": arg.remaps()}
                            )
                        else:
                            nodevars.update({f"output_{arg.condor_name}": arg.files()})
            allvars.append(nodevars)

        return allvars

    def _update_submit_defaults(
        self, submit_description: Union[dict, htcondor.Submit]
    ) -> htcondor.Submit:
        # resolve executable path
        if os.path.exists(self.executable):
            executable = self.executable
        elif found_exec := shutil.which(self.executable):
            executable = found_exec
        else:
            warnings.warn(
                f"executable {self.executable} not found for layer {self.name}, "
                "this may be a failure mode during job submission",
                stacklevel=4,
            )
            executable = self.executable

        # add base submit opts + additional submit descriptors
        universe = submit_description.get("universe", self.universe)
        submit: Dict[str, Any] = {
            "universe": universe,
            "executable": executable,
            "arguments": self._arguments(),
            **submit_description,
        }

        # file submit opts
        if self.transfer_files:
            inputs = self._inputs()
            outputs = self._outputs()
            output_remaps = self._output_remaps()

            if inputs or outputs:
                submit.setdefault("should_transfer_files", "YES")
                submit.setdefault("when_to_transfer_output", "ON_SUCCESS")
                submit.setdefault("success_exit_code", 0)
                submit["preserve_relative_paths"] = True
            if inputs:
                submit["transfer_input_files"] = inputs
            if outputs:
                submit["transfer_output_files"] = outputs
                submit["transfer_output_remaps"] = f'"{output_remaps}"'

        # log submit opts
        submit.setdefault(
            "output", f"{self.log_dir}/$(nodename)-$(cluster)-$(process).out"
        )
        submit.setdefault(
            "error", f"{self.log_dir}/$(nodename)-$(cluster)-$(process).err"
        )

        # extra boilerplate submit opts
        submit.setdefault("notification", "never")

        return htcondor.Submit(format_submit_description(submit))


@dataclass
class Node:
    """Defines a single node (or job) in an HTCondor DAG.

    Stores both the arguments used within a job as well
    as capturing any inputs and outputs the job uses/creates.

    Parameters
    ----------
    arguments
        The arguments the node uses which aren't I/O related.
    inputs
        The arguments the node takes as inputs.
    outputs
        The arguments the node takes as outputs.

    """

    arguments: Union[Argument, Option, list] = field(default_factory=list)
    inputs: Union[Argument, Option, list] = field(default_factory=list)
    outputs: Union[Argument, Option, list] = field(default_factory=list)

    def __post_init__(self) -> None:
        if isinstance(self.arguments, Argument) or isinstance(self.arguments, Option):
            self.arguments = [self.arguments]
        if isinstance(self.inputs, Argument) or isinstance(self.inputs, Option):
            self.inputs = [self.inputs]
        if isinstance(self.outputs, Argument) or isinstance(self.outputs, Option):
            self.outputs = [self.outputs]

    @property
    def requires(self) -> List[str]:
        """
        Returns
        -------
        list
            The inputs this node explicitly depends on to run.

        """
        assert isinstance(self.inputs, list)
        return list(
            itertools.chain(*[input_.args() for input_ in self.inputs if input_.track])
        )

    @property
    def provides(self) -> List[str]:
        """
        Returns
        -------
        list
            The outputs this node provides when it completes.

        """
        assert isinstance(self.outputs, list)
        return list(
            itertools.chain(*[output.args() for output in self.outputs if output.track])
        )


class HexFormatter(dags.SimpleFormatter):
    """A hex-based node formatter that produces names like LayerName:0000C."""

    def __init__(
        self, separator: str = ":", index_format: str = "{:05X}", offset: int = 0
    ) -> None:
        self.separator = separator
        self.index_format = index_format
        self.offset = offset

    def parse(self, node_name: str) -> Tuple[str, int]:
        layer, hex_index = node_name.split(self.separator)
        index = int(hex_index, 16)
        return layer, index - self.offset
