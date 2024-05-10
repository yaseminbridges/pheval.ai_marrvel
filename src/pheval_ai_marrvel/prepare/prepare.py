from pathlib import Path

from pheval_ai_marrvel.prepare.prepare_input import write_input_txt_files


def prepare_inputs(testdata_dir: Path) -> None:
    write_input_txt_files(testdata_dir)
