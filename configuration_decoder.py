from configuration import Configuration
from types import SimpleNamespace
import json

class ConfigurationDecoder:

    """
     ConfigurationDecoder - Decodes input json Configuration file and creates a Configuration class
    """

    def __init__(self):
        pass

    def __decode_configuration(self, configuration_filename):
        with open(configuration_filename) as f:
            x = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        configuration = Configuration(x)
        return configuration

    def decode_configuration(self, configuration_filename):
        return self.__decode_configuration(configuration_filename)
