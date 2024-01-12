from pathlib import Path

from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import create_hgnc_dict

from pheval_template.run.fake_predictor import predict_case


def run_tool(phenopacket_dir: Path, output_dir: Path) -> None:
    hgnc_dict = create_hgnc_dict()
    gene_list = list(hgnc_dict.keys())
    for phenopacket_path in all_files(phenopacket_dir):
        predict_case(phenopacket_path=phenopacket_path, gene_list=gene_list, output_dir=output_dir)
