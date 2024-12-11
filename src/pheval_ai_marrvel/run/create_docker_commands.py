from dataclasses import dataclass
from pathlib import Path
from typing import List

import docker
from docker import DockerClient
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader

from pheval_ai_marrvel.constants import DATA_DEPENDENCIES, HPO_TXT, OUTPUT_DIR, VCF_FILE


@dataclass
class AIMARRVELVolumes:
    """
    Volumes to mount to run AI MARRVEL

    Attributes:
        vcf_path (str): Path to VCF file
        data_dependencies (str): Path to data dependencies
        hpo_txt (str): Path to hpo txt file
        output_dir (str): Path to output directory
    """

    vcf_path: str
    data_dependencies: str
    hpo_txt: str
    output_dir: str


@dataclass
class SampleData:
    """
    Sample data.
    Attributes:
        sample_id (str): Sample ID
        genome_assembly (str): Genome assembly
        vcf_name (Path): VCF file name
    """

    sample_id: str
    genome_assembly: str
    vcf_name: Path


def get_sample_data(phenopacket_path: Path, vcf_dir: Path) -> SampleData:
    """
    Get sample data.

    Args:
        phenopacket_path (Path): Path to phenopacket file
        vcf_dir (Path): Path to VCF directory

    Returns:
        SampleData:The sample data
    """
    phenopacket_util = PhenopacketUtil(phenopacket_reader(phenopacket_path))
    vcf_data = phenopacket_util.vcf_file_data(phenopacket_path, vcf_dir)
    genome_assembly = vcf_data.file_attributes["genomeAssembly"].lower()
    if genome_assembly == "grch37":
        genome_assembly = "hg19"
    elif genome_assembly == "grch38":
        genome_assembly = "hg38"
    return SampleData(
        sample_id=phenopacket_path.stem,
        genome_assembly=genome_assembly,
        vcf_name=vcf_data.uri,
    )


def create_volumes(
    vcf_path: Path, data_dependencies: Path, hpo_txt: Path, output_dir: Path
) -> AIMARRVELVolumes:
    """
    Create volumes to mount AI MARRVEL.
    Args:
        vcf_path (Path): Path to VCF file
        data_dependencies (Path): Path to data dependencies
        hpo_txt (Path): Path to hpo txt file
        output_dir (Path): Path to output directory
    Returns:
        AIMARRVELVolumes:The volumes to mount AI MARRVEL
    """
    return AIMARRVELVolumes(
        vcf_path=f"{str(vcf_path)}:{VCF_FILE}",
        data_dependencies=f"{str(data_dependencies)}:{DATA_DEPENDENCIES}",
        hpo_txt=f"{str(hpo_txt)}:{HPO_TXT}",
        output_dir=f"{str(output_dir)}:{OUTPUT_DIR}",
    )


def create_docker_command(sample_data: SampleData) -> List[str]:
    """
    Create docker command to run AI MARRVEL.
    Args:
        sample_data (SampleData): The sample data
    Returns:
        List[str]: The docker command to run AI MARRVEL
    """
    return ["/run/proc.sh", sample_data.sample_id, sample_data.genome_assembly, "30G"]


def run_docker_sample(
    phenopacket_path: Path,
    vcf_dir: Path,
    data_dependencies: Path,
    hpo_txt: Path,
    output_dir: Path,
    client: DockerClient,
) -> None:
    """
    Run docker command for a sample.
    Args:
        phenopacket_path (Path): Path to phenopacket file
        vcf_dir (Path): Path to VCF directory
        data_dependencies (str): Path to data dependencies
        hpo_txt (str): Path to hpo txt file
        output_dir (str): Path to output directory
        client (DockerClient): Docker client
    """
    sample_data = get_sample_data(phenopacket_path, vcf_dir)
    docker_mounts = create_volumes(sample_data.vcf_name, data_dependencies, hpo_txt, output_dir)
    vol = [
        docker_mounts.vcf_path,
        docker_mounts.hpo_txt,
        docker_mounts.data_dependencies,
        docker_mounts.output_dir,
    ]
    docker_command = create_docker_command(sample_data)
    container = client.containers.run(
        "chaozhongliu/aim-lite",
        " ".join(docker_command),
        volumes=[x for x in vol if x is not None],
        detach=True,
    )
    for line in container.logs(stream=True):
        print(line.strip())


def run_docker(testdata_dir: Path, input_dir: Path, output_dir: Path) -> None:
    """
    Run AI MARRVEL with docker on a corpus.
    Args:
        testdata_dir (Path): Path to test data directory
        input_dir (Path): Path to input directory
        output_dir (Path): Path to output directory
    """
    client = docker.from_env()
    for phenopacket_path in all_files(testdata_dir.joinpath("phenopackets")):
        run_docker_sample(
            phenopacket_path,
            testdata_dir.joinpath("vcf"),
            input_dir,
            output_dir,
            testdata_dir.joinpath(f"hpo_ids/{phenopacket_path.stem}.txt"),
            client,
        )
