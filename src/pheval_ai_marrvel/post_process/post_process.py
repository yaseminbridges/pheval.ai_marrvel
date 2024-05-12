from pathlib import Path

import click

from pheval_ai_marrvel.post_process.post_process_results_format import create_standardised_results


def post_process_results(raw_results_dir: Path, output_dir: Path) -> None:
    """
    Post-process AI-MARRVEL raw results and create standardised PhEval TSV results.

    Args:
        raw_results_dir (Path): Path to the raw results directory.
        output_dir (Path): Path to the output directory.
    """
    create_standardised_results(raw_results_dir, output_dir)


@click.command()
@click.option(
    "--raw-results-dir",
    "-r",
    type=Path,
)
@click.option(
    "--output-dir",
    "-o",
    type=Path,
)
def post_process(raw_results_dir: Path, output_dir: Path) -> None:
    """
    Post-process AI-MARRVEL raw results and create standardised PhEval TSV results.

    Args:
        raw_results_dir (Path): Path to the raw results directory.
        output_dir (Path): Path to the output directory.
    """
    post_process_results(raw_results_dir, output_dir)
