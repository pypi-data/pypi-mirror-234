import filecmp
from unittest import mock

import pytest

from .. import Argument, DAG, Option, Layer, Node


@mock.patch("shutil.which", side_effect=lambda x: f"/path/to/{x}")
def test_dag_generation(mock_which, shared_datadir, tmp_path):
    # create DAG
    dag = DAG()

    # define job requirements
    requirements = {
        "environment": {
            "OMP_NUM_THREADS": 1,
        },
        "getenv": [
            "HOME",
            "USER",
        ],
        "request_cpus": 1,
        "request_memory": 2000,
        "requirements": [
            "HAS_CVMFS_oasis_opensciencegrid_org=TRUE",
        ],
    }

    # create processing layer, add nodes
    process_layer = Layer("process_bins", submit_description=requirements)
    output_files = []
    nodes = []
    for i in range(3):
        output_file = f"output_{i}.txt"
        nodes.append(
            Node(
                arguments=[
                    Argument("job-index", i),
                    Option("verbose"),
                    Option("bins", [3 * j + i for j in range(3)]),
                ],
                inputs=Option("input", "data.txt"),
                outputs=Argument("output", output_file),
            )
        )
        output_files.append(output_file)
    process_layer += nodes

    # add layer to DAG
    dag.attach(process_layer)

    # create combine layer, add node
    with pytest.warns(DeprecationWarning):
        combine_layer = Layer("combine_bins", requirements=requirements)
    combine_layer += Node(
        arguments=Option("verbose"),
        inputs=Argument("input", output_files),
        outputs=Argument("output", "combined.txt"),
    )

    # add layer to DAG
    dag.attach(combine_layer)

    # write DAG to disk
    dag_filename = "my_dag.dag"
    dag_path = tmp_path / dag_filename
    dag.write_dag(dag_filename, tmp_path)

    # write shell script to disk
    script_filename = "my_dag.sh"
    dag.write_script(script_filename, tmp_path)

    # compare contents of generated files
    assert filecmp.cmp(
        dag_path, shared_datadir / dag_filename
    ), f"contents for {dag_filename} does not match expected output"
    for job in ("process_bins", "combine_bins"):
        sub_filename = f"{job}.sub"
        sub_path = tmp_path / sub_filename
        assert filecmp.cmp(
            sub_path, shared_datadir / sub_filename
        ), f"contents for {sub_filename} does not match expected output"
    assert filecmp.cmp(
        tmp_path / script_filename, shared_datadir / script_filename
    ), f"contents for {script_filename} does not match expected output"
