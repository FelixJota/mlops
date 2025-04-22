import yaml
from pathlib import Path

from mlops.config.pipeline import Pipeline
from mlops.config.project import Project


CONFIG_PATH = Path(__file__).parent.parent.parent.parent / "config" / "config.yml"

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)



class MLOpsConfig(BaseModel):
    
    """
    MLOpsConfig class to hold the configuration for the MLOps pipeline.
    """
    project: Project
    pipeline: Pipeline


class Utils:
    @staticmethod
    def load_config(config_path:Path=CONFIG_PATH):

        if not config_path.exists():
          raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return MLOpsConfig(**config)