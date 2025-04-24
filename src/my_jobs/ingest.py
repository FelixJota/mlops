from mlops.command_script.base import CommandScript


class MyIngester(CommandScript):

    def __init__(self, name: str) -> None:
        super().__init__(name=__class__.__name__)
