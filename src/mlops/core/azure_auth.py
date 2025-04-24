import os

from dataclasses import dataclass, asdict

from azure.identity import DefaultAzureCredential

from azure.ai.ml import MLClient

from mlops.core.custom_logger import CustomLogger


@dataclass(frozen=True)
class WorkspaceConfig:
    subscription_id: str = os.getenv("SUBSCRIPTION_ID", "")
    resource_group_name: str = os.getenv("RESOURCE_GROUP_NAME", "")
    workspace_name: str = os.getenv("WORKSPACE_NAME", "")


class AzureAuth:

    def __init__(self, workspace_config: WorkspaceConfig = WorkspaceConfig()) -> None:

        self._credential = None
        self._ml_client = None

        self.logger = CustomLogger(name=__class__.__name__)
        self.workspace_config = workspace_config

    def _get_credential(self) -> DefaultAzureCredential:
        self.logger.info("Getting Credential...")
        return DefaultAzureCredential()

    @property
    def credential(self) -> DefaultAzureCredential:
        if self._credential is None:
            self._credential = self._get_credential()
        return self._credential

    def _get_ml_client(self) -> MLClient:
        self.logger.info("Getting ML Client...")
        return MLClient(credential=self.credential, **asdict(self.workspace_config))

    @property
    def ml_client(self) -> MLClient:
        if self._ml_client is None:
            self._ml_client = self._get_ml_client()
        return self._ml_client


if __name__ == "__main__":

    auth = AzureAuth()

    ml_client = auth.ml_client
