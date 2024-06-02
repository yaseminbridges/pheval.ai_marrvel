from pydantic import BaseModel, Field


class AIMARRVELConfigurations(BaseModel):
    """
    Class for defining the AI MARRVEL configurations in tool_specific_configurations field,
    within the input_dir config.yaml
    Args:
        environment (str): Environment to run AI MARRVEL, i.e., docker/apptainer
    """

    environment: str = Field(...)
