from argparse import ArgumentParser, Namespace
from abc import ABC, abstractmethod
from ast import Name
from mlops.core.custom_logger import CustomLogger


class CommandScript(ABC):

    def __init__(self, name: str) -> None:
        self.name = __class__.__name__
        self.logger = CustomLogger(name=self.name)

    def _parse_args(self) -> Namespace:
        self.logger.info("Parsing Args of the job...")
        argparser = ArgumentParser(prog=self.name)
        return argparser.parse_args()

    @abstractmethod
    def init():
        pass

    @abstractmethod
    def run():
        pass
