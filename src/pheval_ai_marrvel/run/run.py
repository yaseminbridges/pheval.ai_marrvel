import subprocess
from pathlib import Path

from pheval_ai_marrvel.run.create_apptainer_commands import create_apptainer_commands


def run_commands(
    tool_input_commands_dir: Path, testdata_dir: Path, input_dir: Path, output_dir: Path
) -> None:
    """
    Run the apptainer commands.

    Args:
        tool_input_commands_dir (Path): Path to the tool input commands directory.
        testdata_dir (Path): Path to the test data directory.
        input_dir (Path): Path to the input directory.
        output_dir (Path): Path to the output directory.
    """
    create_apptainer_commands(tool_input_commands_dir, testdata_dir, input_dir, output_dir)
    batch_file = tool_input_commands_dir.joinpath(f"{testdata_dir.name}_commands.txt")
    subprocess.run(
        ["bash", str(batch_file)],
        shell=False,
    )
