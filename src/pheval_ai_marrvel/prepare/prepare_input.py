from pathlib import Path

from phenopackets import Phenopacket
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


def obtain_observed_hpo_ids(phenopacket: Phenopacket) -> str:
    observed_phenotypes = PhenopacketUtil(phenopacket).observed_phenotypic_features()
    observed_hpo_ids = "/n".join(observed_phenotypes)
    return observed_hpo_ids


def write_txt_input(observed_hpo_ids: str, output_file_name: Path) -> None:
    with open(output_file_name, "w") as f:
        f.write(observed_hpo_ids)
    f.close()


def write_observed_hpo_ids(phenopacket_path: Path, testdata_dir: Path) -> None:
    phenopacket = phenopacket_reader(phenopacket_path)
    observed_hpo_ids = obtain_observed_hpo_ids(phenopacket)
    write_txt_input(
        observed_hpo_ids, Path(testdata_dir).joinpath(f"hpo_ids/{phenopacket_path.stem}.txt")
    )


def write_input_txt_files(testdata_dir: Path) -> None:
    for phenopacket_path in all_files(Path(testdata_dir).joinpath("phenopackets")):
        write_observed_hpo_ids(phenopacket_path, testdata_dir)
