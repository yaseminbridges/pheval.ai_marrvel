from dataclasses import dataclass
from pathlib import Path
from typing import List

from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


@dataclass
class NextFlowParameters:
    """
    Parameters for running AI MARRVEL with next flow.
    Attributes:
        executable (Path): Path to the executable.
        ref_dir (Path): Path to the reference directory.
        input_vcf (Path): Path to the input vcf file.
        input_hpo (Path): Path to the input hpo file.
        output_dir (Path): Path to the output directory.
        sample_id (str): Sample ID.
        reference_version (str): Genome reference version.
    """

    executable: Path
    ref_dir: Path
    input_vcf: Path
    input_hpo: Path
    output_dir: Path
    sample_id: str
    reference_version: str


def get_next_flow_parameters(
    phenopacket_path: Path, testdata_dir: Path, input_dir: Path, output_dir: Path
):
    """
    Get next flow parameters for a sample.
    Args:
        phenopacket_path (Path): Path to the phenopacket file.
        testdata_dir (Path): Path to the test data directory.
        input_dir (Path): Path to the input directory.
        output_dir (Path): Path to the output directory.
    """
    phenopacket = phenopacket_reader(phenopacket_path)
    vcf_file_data = PhenopacketUtil(phenopacket).vcf_file_data(
        phenopacket_path, testdata_dir.joinpath("vcf")
    )
    genome_assembly = vcf_file_data.file_attributes["genomeAssembly"].lower()
    if genome_assembly == "grch37":
        genome_assembly = "hg19"
    elif genome_assembly == "grch38":
        genome_assembly = "hg38"
    return NextFlowParameters(
        executable=input_dir.joinpath("AI_MARRVEL/main.nf"),
        ref_dir=input_dir,
        input_vcf=vcf_file_data.uri,
        input_hpo=testdata_dir.joinpath(f"hpo_ids/{phenopacket_path.stem}.txt"),
        output_dir=output_dir,
        sample_id=phenopacket.subject.id,
        reference_version=genome_assembly,
    )


def create_next_flow_command(next_flow_parameters: NextFlowParameters) -> str:
    return (
        f"nextflow run {next_flow_parameters.executable} "
        f"--ref_dir {next_flow_parameters.ref_dir} "
        f"--input_vcf {next_flow_parameters.input_vcf} "
        f"--input_hpo {next_flow_parameters.input_hpo} "
        f"--outdir {next_flow_parameters.output_dir} "
        f"--run_id {next_flow_parameters.sample_id} "
        f"--ref_ver {next_flow_parameters.reference_version}"
    )


def write_commands(commands: List[str], tool_input_commands_dir: Path, testdata_dir: Path) -> None:
    """
    Write commands to a txt file.

    Args:
        commands (List[str]): The commands to write.
        tool_input_commands_dir (Path): The tool input commands directory.
        testdata_dir (Path): The testdata directory.
    """
    joined_commands_str = "\n".join(commands)
    with open(
        f"{tool_input_commands_dir.joinpath(f'{testdata_dir.name}_commands.txt')}", "w"
    ) as commands_file:
        commands_file.write(joined_commands_str)
    commands_file.close()


def create_nextflow_commands(
    tool_input_commands_dir: Path, testdata_dir: Path, input_dir: Path, output_dir: Path
) -> None:
    """
    Create nextflow commands for running AI-MARRVEL with a corpus.

    Args:
        tool_input_commands_dir (Path): The tool input commands directory.
        testdata_dir (Path): The testdata directory.
        input_dir (Path): The input directory.
        output_dir (Path): The output directory.
    """
    all_commands = []
    for phenopacket_path in all_files(testdata_dir.joinpath("phenopackets")):
        next_flow_arguments = get_next_flow_parameters(
            phenopacket_path, testdata_dir, input_dir, output_dir
        )
        all_commands.append(create_next_flow_command(next_flow_arguments))
    write_commands(all_commands, tool_input_commands_dir, testdata_dir)
