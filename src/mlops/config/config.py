import yaml
from pathlib import Path
from pydantic import BaseModel
from mlops.config.pipeline import Pipeline
from mlops.config.project import Project


class MLOpsConfig(BaseModel):
    """
    MLOpsConfig class to hold the configuration for the MLOps pipeline.
    """

    project: Project
    pipeline: Pipeline
