import subprocess
from pathlib import Path

from pheval_ai_marrvel.run.create_apptainer_commands import create_apptainer_commands


def run_commands(
    tool_input_commands_dir: Path, testdata_dir: Path, input_dir: Path, output_dir
) -> None:
    create_apptainer_commands(tool_input_commands_dir, testdata_dir, input_dir, output_dir)
    batch_file = tool_input_commands_dir.joinpath("apptainer_commands.txt")
    subprocess.run(
        ["bash", str(batch_file)],
        shell=False,
    )
