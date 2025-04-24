import yaml

from pathlib import Path
from mlops.config.config import MLOpsConfig

ROOT_PATH = Path(__file__).parent.parent.parent.parent
SRC_PATH = ROOT_PATH / "src"
MY_JOBS_FOLDER = "my_jobs"
CONFIG_PATH = Path(__file__).parent.parent.parent.parent / "config" / "config.yml"


class Utils:
    @staticmethod
    def load_config(config_path: Path = CONFIG_PATH):

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return MLOpsConfig(**config)

    @staticmethod
    def get_my_jobs_path(
        src_path: Path = SRC_PATH, jobs_folder: str = MY_JOBS_FOLDER
    ) -> Path:
        return src_path / jobs_folder
