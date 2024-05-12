from pathlib import Path

from pheval_ai_marrvel.prepare.prepare_input import write_input_txt_files


def prepare_inputs(testdata_dir: Path) -> None:
    """
    Prepare input files for AI Marrvel prediction from phenopackets.

    Args:
        testdata_dir (Path): Path to the test data directory.
    """
    testdata_dir.joinpath("hpo_ids").mkdir(exist_ok=True)
    write_input_txt_files(testdata_dir)
