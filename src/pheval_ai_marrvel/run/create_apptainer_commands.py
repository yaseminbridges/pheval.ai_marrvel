from dataclasses import dataclass
from pathlib import Path
from typing import List

from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


@dataclass
class ApptainerArguments:
    sample_id: str
    vcf_path: Path
    vcf_assembly: str
    hpo_txt_file_path: Path
    data_dependencies: Path
    output_directory: Path


def get_apptainer_arguments(
    phenopacket_path: Path, testdata_dir: Path, input_dir: Path, output_dir: Path
) -> ApptainerArguments:
    phenopacket = phenopacket_reader(phenopacket_path)
    vcf_file_data = PhenopacketUtil(phenopacket).vcf_file_data(
        phenopacket_path, testdata_dir.joinpath("vcf")
    )
    return ApptainerArguments(
        sample_id=phenopacket.subject.id,
        vcf_path=vcf_file_data.uri,
        vcf_assembly=vcf_file_data.file_attributes["genomeAssembly"],
        hpo_txt_file_path=testdata_dir.joinpath(f"hpo_ids/{phenopacket_path.stem}.txt"),
        data_dependencies=input_dir,
        output_directory=output_dir,
    )


def create_apptainer_command(apptainer_arguments: ApptainerArguments) -> str:
    return (
        f"apptainer run --mount type=bind,source={apptainer_arguments.vcf_path},destination=/input/vcf.gz"
        f" --mount type=bind,source={apptainer_arguments.hpo_txt_file_path},destination=/input/hpo.txt"
        f" --mount type=bind,source={apptainer_arguments.data_dependencies},destination=/run/data_dependencies"
        f" --mount type=bind,source={apptainer_arguments.output_directory},destination=/out"
        f" docker://chaozhongliu/aim-lite /run/proc.sh {apptainer_arguments.sample_id}"
        f" {apptainer_arguments.vcf_assembly} 32"
    )


def write_commands(commands: List[str], tool_input_commands_dir: Path, testdata_dir: Path) -> None:
    joined_commands_str = "\n".join(commands)
    with open(
        f"{tool_input_commands_dir.joinpath(f'{testdata_dir.name}_commands.txt')}", "w"
    ) as commands_file:
        commands_file.write(joined_commands_str)
    commands_file.close()


def create_apptainer_commands(
    tool_input_commands_dir: Path, testdata_dir: Path, input_dir: Path, output_dir: Path
) -> None:
    all_commands = []
    for phenopacket_path in all_files(testdata_dir.joinpath("phenopackets")):
        apptainer_arguments = get_apptainer_arguments(
            phenopacket_path, testdata_dir, input_dir, output_dir
        )
        all_commands.append(create_apptainer_command(apptainer_arguments))
    write_commands(all_commands, tool_input_commands_dir, testdata_dir)
