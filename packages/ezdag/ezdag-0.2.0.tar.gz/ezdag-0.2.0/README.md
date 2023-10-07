<h1 align="center">ezdag</h1>

<p align="center">High-level HTCondor DAG generation library</p>

<p align="center">
  <a href="https://git.ligo.org/patrick.godwin/ezdag/-/pipelines/latest">
    <img alt="ci" src="https://git.ligo.org/patrick.godwin/ezdag/badges/main/pipeline.svg" />
  </a>
  <a href="https://git.ligo.org/patrick.godwin/ezdag/-/pipelines/latest">
    <img alt="ci" src="https://git.ligo.org/patrick.godwin/ezdag/badges/main/coverage.svg" />
  </a>
  <a href="https://docs.ligo.org/patrick.godwin/ezdag/">
    <img alt="documentation" src="https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat" />
  </a>
  <a href="https://pypi.org/project/ezdag/">
    <img alt="pypi version" src="https://img.shields.io/pypi/v/ezdag.svg" />
  </a>
  <a href="https://anaconda.org/conda-forge/ezdag">
    <img alt="conda version" src="https://img.shields.io/conda/vn/conda-forge/ezdag.svg" />
  </a>
</p>

---

## Installation

With `pip`:

```
pip install ezdag
```

With `conda`:

```
conda install -c conda-forge ezdag
```

## Features

This library provides a high-level API on top of `htcondor.dags`. Specifically, it adds two features:

1. Programmatic way of generating command line arguments
2. Track job dependencies automatically through file inputs and outputs

With (1), this allows you to define job arguments and tracked files on a per-job level for a given layer,
and these get automatically formatted into the right submit description when the DAG is generated.

By tracking job dependencies from (2) based on file input/outputs from specific jobs, all the parent/child
relationships get determined automatically without specifying them explicitly. This is similar in spirit
to Makefiles, where node connections are based purely on what data the job needs and provides.

An example of both these features can be seen in the quickstart below.

## Quickstart

The example below creates a simple DAG with two layers; a layer with 3 jobs which all produce output, and
a second layer with a single job, combining output from the other jobs:

```python
from ezdag import Argument, DAG, Option, Layer, Node

# create DAG
dag = DAG()

# define job options
# this can be a dictionary or an htcondor.Submit object
options = {
    "environment": {
        "OMP_NUM_THREADS": 1,
    },
    "requirements": [
        "HAS_CVMFS_oasis_opensciencegrid_org=TRUE",
    ],
    "request_cpus": 1,
    "request_memory": 2000
}

# create processing layer, add nodes
process_layer = Layer("process_bins", submit_description=options)
output_files = []
for i in range(3):
    output_file = f"output_{i}.txt"
    process_layer += Node(
        arguments = [
            Argument("job-index", i),                       # {i}
            Option("verbose"),                              # --verbose
            Option("bins", [3 * j + i for j in range(3)]),  # --bins {i} --bins {3 + i} --bins {6 + i}
        ],
        inputs = Option("input", "data.txt"),               # --input data.txt
        outputs = Argument("output", output_file)           # output_{i}.txt
    )
    output_files.append(output_file)

# add layer to DAG
dag.attach(process_layer)

# create combine layer, add node
combine_layer = Layer("combine_bins", submit_description=options)
combine_layer += Node(
    arguments = Option("verbose"),                          # --verbose
    inputs = Argument("input", output_files),               # output_0.txt output_1.txt output_2.txt
    outputs = Argument("output", "combined.txt")            # combined.txt
)

# add layer to DAG
dag.attach(combine_layer)

# write DAG to disk
dag.write_dag("my_dag.dag")
```

This generates 3 files, a DAG file (`my_dag.dag`) as well as submit files for each of the layers (2 total):

`my_dag.dag`:

```
# BEGIN META
# END META
# BEGIN NODES AND EDGES
JOB process_bins:00000 process_bins.sub
VARS process_bins:00000 nodename="process_bins:00000" job_index="0" verbose="--verbose" bins="--bins 0 --bins 3 --bins 6" input_="--input data.txt" input_input_="data.txt" output_="output_0.txt" output_output_="output_0.txt" output_output__remap=""
RETRY process_bins:00000 3
JOB process_bins:00001 process_bins.sub
VARS process_bins:00001 nodename="process_bins:00001" job_index="1" verbose="--verbose" bins="--bins 1 --bins 4 --bins 7" input_="--input data.txt" input_input_="data.txt" output_="output_1.txt" output_output_="output_1.txt" output_output__remap=""
RETRY process_bins:00001 3
JOB process_bins:00002 process_bins.sub
VARS process_bins:00002 nodename="process_bins:00002" job_index="2" verbose="--verbose" bins="--bins 2 --bins 5 --bins 8" input_="--input data.txt" input_input_="data.txt" output_="output_2.txt" output_output_="output_2.txt" output_output__remap=""
RETRY process_bins:00002 3
PARENT process_bins:00000 CHILD combine_bins:00000
PARENT process_bins:00001 CHILD combine_bins:00000
PARENT process_bins:00002 CHILD combine_bins:00000
JOB combine_bins:00000 combine_bins.sub
VARS combine_bins:00000 nodename="combine_bins:00000" verbose="--verbose" input_="output_0.txt output_1.txt output_2.txt" input_input_="output_0.txt,output_1.txt,output_2.txt" output_="combined.txt" output_output_="combined.txt" output_output__remap=""
RETRY combine_bins:00000 3
# END NODES AND EDGES
```

`process_bins.sub`:

```
universe = vanilla
executable = /path/to/process_bins
arguments = $(job_index) $(verbose) $(bins) $(input_) $(output_)
request_cpus = 1
request_memory = 2000
should_transfer_files = YES
when_to_transfer_output = ON_SUCCESS
success_exit_code = 0
preserve_relative_paths = True
transfer_input_files = $(input_input_)
transfer_output_files = $(output_output_)
transfer_output_remaps = "$(output_output__remap)"
output = logs/$(nodename)-$(cluster)-$(process).out
error = logs/$(nodename)-$(cluster)-$(process).err
notification = never

queue
```

`combine_bins.sub`:

```
universe = vanilla
executable = /path/to/combine_bins
arguments = $(verbose) $(input_) $(output_)
request_cpus = 1
request_memory = 2000
should_transfer_files = YES
when_to_transfer_output = ON_SUCCESS
success_exit_code = 0
preserve_relative_paths = True
transfer_input_files = $(input_input_)
transfer_output_files = $(output_output_)
transfer_output_remaps = "$(output_output__remap)"
output = logs/$(nodename)-$(cluster)-$(process).out
error = logs/$(nodename)-$(cluster)-$(process).err
notification = never

queue
```
