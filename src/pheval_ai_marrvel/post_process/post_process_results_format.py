from pathlib import Path
from typing import List

import polars as pl
from pheval.post_processing.post_processing import (
    PhEvalGeneResult,
    PhEvalVariantResult,
    calculate_end_pos,
    generate_pheval_result,
)
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_hgnc_dict


def read_raw_result(raw_result_path: Path) -> pl.DataFrame:
    """
    Read the raw result file.

    Args:
        raw_result_path(Path): Path to the raw result file.

    Returns:
        List[dict]: Contents of the raw result file.
    """
    raw_result = pl.read_csv(raw_result_path)
    raw_result = raw_result.rename({"Unnamed: 0": "variant"})
    return raw_result.select(pl.col(["variant", "predict", "geneSymbol"]))


class ConvertToPhEvalResult:
    """Class to convert the raw result file to PhEvalGeneResult and PhEvalVariantResult."""

    def __init__(self, raw_result: pl.DataFrame, gene_identifier_updater: GeneIdentifierUpdater):
        """
        Initialise the ConvertToPhEvalResult class.

        Args:
            raw_result (pl.DataFrame): Contents of the raw result file.

        """
        self.raw_result = raw_result
        self.gene_identifier_updater = gene_identifier_updater

    @staticmethod
    def _obtain_score(result_entry: dict) -> float:
        """
        Obtain the score from the result entry.

        Args:
            result_entry (dict): Contents of the result entry.

        Returns:
            float: The score.
        """
        return result_entry["predict"]

    @staticmethod
    def _obtain_gene_symbol(result_entry: dict) -> str:
        """
        Obtain the gene symbol from the result entry.

        Args:
            result_entry (dict): Contents of the result entry.

        Returns:
            str: The gene symbol.
        """
        return result_entry["geneSymbol"]

    def obtain_gene_identifier(self, result_entry: dict) -> str:
        """
        Obtain the gene identifier from the result entry.

        Args:
            result_entry (dict): Contents of the result entry.

        Returns:
            str: The gene identifier.
        """
        return self.gene_identifier_updater.find_identifier(self._obtain_gene_symbol(result_entry))

    @staticmethod
    def obtain_chrom(variant_str: str) -> str:
        return variant_str.split("-")[0]

    @staticmethod
    def obtain_pos(variant_str: str) -> int:
        return int(variant_str.split("-")[1])

    @staticmethod
    def obtain_ref(variant_str: str) -> str:
        return variant_str.split("-")[2]

    @staticmethod
    def obtain_alt(variant_str: str) -> str:
        return variant_str.split("-")[3]

    def extract_pheval_gene_requirements(self) -> List[PhEvalGeneResult]:
        """
        Extract the data required to produce PhEval gene output.

        Returns:
            List[PhEvalGeneResult]: List of PhEvalGeneResult objects.
        """
        pheval_result = []
        for result_entry in self.raw_result.rows(named=True):
            pheval_result.append(
                PhEvalGeneResult(
                    gene_symbol=self._obtain_gene_symbol(result_entry),
                    gene_identifier=self.obtain_gene_identifier(result_entry),
                    score=self._obtain_score(result_entry),
                )
            )
        return pheval_result

    def extract_pheval_variant_requirements(self) -> List[PhEvalVariantResult]:
        """
        Extract the data required to produce PhEval variant output.

        Returns:
            List[PhEvalVariantResult]: List of PhEvalVariantResult objects.
        """
        pheval_result = []
        for result_entry in self.raw_result.rows(named=True):
            pheval_result.append(
                PhEvalVariantResult(
                    chromosome=self.obtain_chrom(result_entry["variant"]),
                    start=self.obtain_pos(result_entry["variant"]),
                    end=calculate_end_pos(
                        self.obtain_pos(result_entry["variant"]),
                        self.obtain_ref(result_entry["variant"]),
                    ),
                    ref=self.obtain_ref(result_entry["variant"]),
                    alt=self.obtain_alt(result_entry["variant"]),
                )
            )
        return pheval_result


def create_standardised_results(raw_results_dir: Path, output_dir: Path) -> None:
    """
    Create PhEval gene tsv output from raw results.

    Args:
        raw_results_dir (Path): Path to the raw results directory.
        output_dir (Path): Path to the output directory.
    """
    gene_identifier_updator = GeneIdentifierUpdater(
        gene_identifier="ensembl_id", hgnc_data=create_hgnc_dict()
    )
    raw_results = [file for file in all_files(raw_results_dir) if "_integrated.csv" in file.name]
    for raw_result_path in raw_results:
        raw_result = read_raw_result(raw_result_path)
        converter = ConvertToPhEvalResult(raw_result, gene_identifier_updator)
        pheval_gene_result = converter.extract_pheval_gene_requirements()
        generate_pheval_result(
            pheval_result=pheval_gene_result,
            sort_order_str="DESCENDING",
            output_dir=output_dir,
            tool_result_path=Path(str(raw_result_path).replace("_integrated", "")),
        )
        pheval_variant_result = converter.extract_pheval_variant_requirements()
        generate_pheval_result(
            pheval_result=pheval_variant_result,
            sort_order_str="DESCENDING",
            output_dir=output_dir,
            tool_result_path=Path(str(raw_result_path).replace("_integrated", "")),
        )
