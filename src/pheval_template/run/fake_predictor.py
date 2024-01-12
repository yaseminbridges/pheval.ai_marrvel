import json
import random
from pathlib import Path
from typing import List
from phenopackets import Phenopacket

from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


class FakePredictor:
    def __init__(self, phenopacket: Phenopacket, gene_list: List[str]):
        self.phenopacket = phenopacket
        self.gene_list = gene_list
        self.random_generator = random.Random(42)

    def _get_known_genes(self) -> List[str]:
        diagnosed_genes = PhenopacketUtil(self.phenopacket).diagnosed_genes()
        return [diagnosed_gene.gene_symbol for diagnosed_gene in diagnosed_genes]

    def _get_random_list_of_predicted_genes(self) -> List[str]:
        return self.random_generator.choices(self.gene_list, k=15)

    def _get_list_of_predictions(self) -> List[str]:
        return self._get_known_genes() + self._get_random_list_of_predicted_genes()

    def predict(self):
        predictions = self._get_list_of_predictions()
        predictions_with_scores = []
        for prediction in predictions:
            self.random_generator.seed()
            predictions_with_scores.append({'gene_symbol': prediction,
                                            'score': self.random_generator.uniform(0, 1)})
        return predictions_with_scores


def predict_case(phenopacket_path: Path, gene_list: List[str], output_dir: Path):
    phenopacket = phenopacket_reader(phenopacket_path)
    predictions = FakePredictor(phenopacket, gene_list).predict()
    with open(output_dir.joinpath(phenopacket_path.name), "w") as output_file:
        json.dump(predictions, output_file, indent=4)
    output_file.close()
