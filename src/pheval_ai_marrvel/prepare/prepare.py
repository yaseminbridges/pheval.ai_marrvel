from pathlib import Path

from pheval_ai_marrvel.prepare.prepare_input import write_input_txt_files


def prepare_inputs(testdata_dir: Path) -> None:
    testdata_dir.joinpath("hpo_ids").mkdir(exist_ok=True)
    write_input_txt_files(testdata_dir)
