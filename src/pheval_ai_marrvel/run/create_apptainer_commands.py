from dataclasses import dataclass
from pathlib import Path
from typing import List

from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


@dataclass
class ApptainerArguments:
    """
    Arguments required for running AI-MARRVEL apptainer commands.

    Attributes:
        sample_id (str): The sample ID.
        vcf_path (Path): The VCF file path.
        vcf_assembly (str): The VCF assembly.
        hpo_txt_file_path (Path): The hpo txt file path.
        data_dependencies (Path): The data_dependencies path.
        output_directory (Path): The output directory path.
    """

    sample_id: str
    vcf_path: Path
    vcf_assembly: str
    hpo_txt_file_path: Path
    data_dependencies: Path
    output_directory: Path


def get_apptainer_arguments(
    phenopacket_path: Path, testdata_dir: Path, input_dir: Path, output_dir: Path
) -> ApptainerArguments:
    """
    Get apptainer arguments for running AI-MARRVEL apptainer commands for a phenopacket.

    Args:
        phenopacket_path (Path): The phenopacket path.
        testdata_dir (Path): The testdata directory.
        input_dir (Path): The input directory.
        output_dir (Path): The output directory.

    Returns:
        ApptainerArgument: The arguments for running AI-MARRVEL apptainer commands.
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
    return ApptainerArguments(
        sample_id=phenopacket_path.stem,
        vcf_path=vcf_file_data.uri,
        vcf_assembly=genome_assembly,
        hpo_txt_file_path=testdata_dir.joinpath(f"hpo_ids/{phenopacket_path.stem}.txt"),
        data_dependencies=input_dir,
        output_directory=output_dir,
    )


def create_apptainer_command(apptainer_arguments: ApptainerArguments) -> str:
    """
    Create an apptainer command for running AI-MARRVEL for a sample.

    Args:
        apptainer_arguments(ApptainerArguments): Arguments for running AI-MARRVEL with apptainer.

    Returns:
        str: The string apptainer command.
    """
    return (
        f"apptainer run --mount type=bind,source={apptainer_arguments.vcf_path},destination=/input/vcf.gz"
        f" --mount type=bind,source={apptainer_arguments.hpo_txt_file_path},destination=/input/hpo.txt"
        f" --mount type=bind,source={apptainer_arguments.data_dependencies},destination=/run/data_dependencies"
        f" --mount type=bind,source={apptainer_arguments.output_directory},destination=/out"
        f" docker://chaozhongliu/aim-lite /run/proc.sh {apptainer_arguments.sample_id}"
        f" {apptainer_arguments.vcf_assembly} 32"
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


def create_apptainer_commands(
    tool_input_commands_dir: Path, testdata_dir: Path, input_dir: Path, output_dir: Path
) -> None:
    """
    Create apptainer commands for running AI-MARRVEL apptainer with a corpus.

    Args:
        tool_input_commands_dir (Path): The tool input commands directory.
        testdata_dir (Path): The testdata directory.
        input_dir (Path): The input directory.
        output_dir (Path): The output directory.
    """
    all_commands = []
    for phenopacket_path in all_files(testdata_dir.joinpath("phenopackets")):
        apptainer_arguments = get_apptainer_arguments(
            phenopacket_path, testdata_dir, input_dir, output_dir
        )
        all_commands.append(create_apptainer_command(apptainer_arguments))
    write_commands(all_commands, tool_input_commands_dir, testdata_dir)
