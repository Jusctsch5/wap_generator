from pathlib import PurePath
from types import SimpleNamespace
import json

from wap_generator.announcer.announcer import Announcer


class AnnouncerDecoder:
    """
     AnnouncerDecoder - Decodes input json Configuration file and creates a Configuration class
    """

    common_config_location = PurePath(
        '.', 'user', 'announcer', 'announcer.json')

    def __init__(self):
        pass

    def __decode_configuration(self, configuration_filename):
        print(configuration_filename)
        with open(configuration_filename) as f:
            x = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        announcer = Announcer(x.AnnouncementVolume)
        announcer.configure()

        return announcer

    def decode_configuration(self, configuration_filename):
        return self.__decode_configuration(configuration_filename)

    def decode_common_configuration(self):
        return self.decode_configuration(self.common_config_location)
