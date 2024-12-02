import subprocess
from pathlib import Path

from pheval_ai_marrvel.run.create_apptainer_commands import create_apptainer_commands
from pheval_ai_marrvel.run.create_docker_commands import run_docker
from pheval_ai_marrvel.run.prepare_next_flow_commands import create_nextflow_commands


def run_batch_file(testdata_dir: Path, tool_input_commands_dir: Path):
    """
    Run the batch file for the corpus.
    Args:
        testdata_dir (Path): Path to the test data directory.
        tool_input_commands_dir (Path): Path to the input commands directory.
    """
    batch_file = tool_input_commands_dir.joinpath(f"{testdata_dir.name}_commands.txt")
    subprocess.run(
        ["bash", str(batch_file)],
        shell=False,
    )


def run_commands(
    tool_input_commands_dir: Path,
    testdata_dir: Path,
    input_dir: Path,
    output_dir: Path,
    environment: str,
) -> None:
    """
    Run the apptainer commands.

    Args:
        tool_input_commands_dir (Path): Path to the tool input commands directory.
        testdata_dir (Path): Path to the test data directory.
        input_dir (Path): Path to the input directory.
        output_dir (Path): Path to the output directory.
    """
    if environment.lower() == "apptainer":
        create_apptainer_commands(tool_input_commands_dir, testdata_dir, input_dir, output_dir)
        run_batch_file(testdata_dir, tool_input_commands_dir)
    elif environment.lower() == "docker":
        run_docker(testdata_dir, input_dir, output_dir)
    elif environment.lower() == "nextflow":
        create_nextflow_commands(tool_input_commands_dir, testdata_dir, input_dir, output_dir)
        run_batch_file(testdata_dir, tool_input_commands_dir)
