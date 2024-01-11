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
        """prepare method."""
        print("preparing")

    def run(self):
        """run method."""
        print("running with template pheval runner")

    def post_process(self):
        """post_process method."""
        print("post processing")
