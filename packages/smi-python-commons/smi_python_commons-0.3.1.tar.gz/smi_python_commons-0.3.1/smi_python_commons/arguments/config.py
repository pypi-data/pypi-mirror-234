from abc import ABC

from smi_python_commons.arguments.argument import Argument


class ConfigBase(ABC):
    pass


class Config(ConfigBase):

    def __init__(self, description: str, arguments: [Argument]):
        self.description = description
        self.arguments = arguments


class SubCommandsConfig(ConfigBase):
    def __init__(self, help: str):
        pass
