from pathlib import Path

from pheval_template.post_process.post_process_results_format import create_standardised_results


def post_process(raw_results_dir: Path, output_dir: Path) -> None:
    create_standardised_results(raw_results_dir=raw_results_dir,
                                output_dir=output_dir)
