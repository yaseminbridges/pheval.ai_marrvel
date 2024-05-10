from dataclasses import dataclass
from pathlib import Path

from pheval.runners.runner import PhEvalRunner


@dataclass
class TemplatePhEvalRunner(PhEvalRunner):
    input_dir: Path
    testdata_dir: Path
    tmp_dir: Path
    output_dir: Path
    config_file: Path
    version: str

    def prepare(self):
        """
        Pre-process any data and inputs necessary to run the tool.
        """
        print("preparing")

    def run(self):
        """
        Run the tool to produce the raw output.
        """
        print("running with fake predictor")

    def post_process(self):
        """
        Post-process the raw output into PhEval standardised TSV output.
        """
        print("post processing results to PhEval standardised TSV output.")
