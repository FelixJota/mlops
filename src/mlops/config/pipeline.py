from typing import Union, Dict, Any, Optional
import re
from abc import ABC
from azure.ai.ml import Input, Output
from azure.ai.ml.constants import AssetTypes, InputOutputModes
from pydantic import BaseModel, model_validator


class YAMLPipelineSyntax:
    DOT = "."
    PARENT = "parent"
    INPUTS = "inputs"
    OUTPUTS = "outputs"
    JOBS = "jobs"

    def join_elements(elements: list[str], DOT: str = DOT) -> str:
        """
        Join elements with dot notation.
        """
        return DOT.join(elements)

    PARENT_JOBS = join_elements([PARENT, JOBS])
    PARENT_INPUTS = join_elements([PARENT, INPUTS])
    PARENT_OUTPUTS = join_elements([PARENT, OUTPUTS])


class MLArgsDefinition(BaseModel):

    description: str
    type: str
    mode: str
    path: Optional[str] = None

    @staticmethod
    def check_if_valid_type(
        field: str, obj: Union[AssetTypes, InputOutputModes]
    ) -> bool:
        """
        Check if the type is valid.
        """
        ATTR = field.upper()
        try:
            VALUE = getattr(obj, ATTR)
            return True
        except:
            raise ValueError(f"{field} is not a valid type for {obj.__name__}")

    @model_validator(mode="after")
    @classmethod
    def validate_type_and_mode(cls, cls_instance) -> None:
        """
        Validate the type of the asset.
        """
        cls.check_if_valid_type(field=cls_instance.type, obj=AssetTypes)

        cls.check_if_valid_type(field=cls_instance.mode, obj=InputOutputModes)
        return cls_instance


class MLJobInputs(BaseModel):
    inputs: Optional[dict[str, str]] = None
    outputs: Optional[Union[dict[str, str], dict[str, MLArgsDefinition]]] = None


class MLJobAsset(MLJobInputs):
    environment: str

    @model_validator(mode="after")
    @classmethod
    def validate_environment(cls, cls_instance):
        """
        environment uri has to match azureml://environments/<environment_name>/version/<version>
        """
        pattern = r"azureml://environments/[^/]+/versions/(\d+|latest)"
        if not re.match(pattern, cls_instance.environment):
            raise ValueError(
                "Environment URI must match the pattern: azureml://environments/<environment_name>/versions/<version>"
            )
        return cls_instance


class Pipeline(BaseModel):

    name: str
    display_name: str
    description: str
    inputs: dict[str, MLArgsDefinition]
    outputs: Optional[dict[str, MLArgsDefinition]] = None
    jobs: dict[str, MLJobAsset]

    def get_pipeline_ml_inputs(self) -> dict[str, Input]:
        """
        Get the pipeline inputs.
        """
        ml_inputs = {}
        for key, value in self.inputs.items():
            ml_inputs[key] = Input(
                type=value.type,
                description=value.description,
                mode=value.mode,
                path=value.path,
            )
        return ml_inputs

    def get_ml_job_inputs_and_outputs_mapping(self):
        """
        Get the mapping of inputs and outputs for the jobs.
        """
        ml_job_inputs = {}
        ml_job_outputs = {}
        for job_name, job in self.jobs.items():
            job_inputs = job.inputs
            job_outputs = job.outputs
            if job_inputs:
                for input_key, input_value in job_inputs.items():
                    if YAMLPipelineSyntax.PARENT_INPUTS in input_value:
                        input_key = input_value.replace(
                            YAMLPipelineSyntax.PARENT_INPUTS, ""
                        )

    def get_ml_job_inputs(self) -> dict[str, Input]:
        """
        Get the inputs for the jobs.
        """
        ml_job_inputs = {}
        for job_name, job in self.jobs.items():
            if job.inputs:
                ml_job_inputs[job_name] = {
                    key: Input(
                        type=value.type,
                        description=value.description,
                        mode=value.mode,
                        path=value.path,
                    )
                    for key, value in job.inputs.items()
                }
        return ml_job_inputs


if __name__ == "__main__":

    import yaml
    from pathlib import Path

    CONFIG_PATH = Path(__file__).parent.parent.parent.parent / "config" / "config.yml"

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    pipeline = Pipeline(**config["pipeline"])

    print(pipeline.model_dump_json(indent=4))
    print(pipeline.get_pipeline_ml_inputs())
    print(pipeline.get_ml_job_inputs_and_outputs_mapping())
    print(pipeline.get_ml_job_inputs())
