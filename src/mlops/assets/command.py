from typing import Optional
from azure.ai.ml import command, Input, Output
from azure.ai.ml.entities import Command


from mlops.core.custom_logger import CustomLogger
from mlops.config.pipeline import MLJobAsset


class CommandBuilder:
    def __init__(
        self,
        job_config: MLJobAsset,
        inputs: Optional[dict[str, Input]],
        outputs: Optional[dict[str, Output]],
    ) -> None:
        self.logger = CustomLogger(name=__class__.__name__)

    def __call__(self) -> Command:

        return command(code=)
