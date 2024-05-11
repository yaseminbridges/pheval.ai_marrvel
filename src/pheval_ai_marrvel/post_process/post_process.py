from pathlib import Path

import click

from pheval_ai_marrvel.post_process.post_process_results_format import create_standardised_results


def post_process_results(raw_results_dir: Path, output_dir: Path) -> None:
    create_standardised_results(raw_results_dir, output_dir)


@click.command()
@click.option(
    "--raw_results_dir",
    "-r",
    type=Path,
)
@click.option(
    "--output_dir",
    "-r",
    type=Path,
)
def post_process(raw_results_dir: Path, output_dir: Path) -> None:
    post_process_results(raw_results_dir, output_dir)
