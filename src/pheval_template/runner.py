from dataclasses import dataclass
from pathlib import Path

from pheval.runners.runner import PhEvalRunner

from pheval_template.post_process.post_process import post_process
from pheval_template.run.run import run


@dataclass
class TemplatePhEvalRunner(PhEvalRunner):
    input_dir: Path
    testdata_dir: Path
    tmp_dir: Path
    output_dir: Path
    config_file: Path
    version: str

    def prepare(self):
        """prepare method."""
        # Any preprocessing required to run the tool should be carried out here.
        # This could include, but is not limited to, writing a required tool config
        # and preparing the test data in a compatible format
        print("preparing")

    def run(self):
        """run method."""
        print("running with template pheval runner")
        run(self.testdata_dir, self.raw_results_dir)

    def post_process(self):
        """post_process method."""
        print("post processing")
        post_process(raw_results_dir=self.raw_results_dir, output_dir=self.output_dir)
