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

    announcementvolume = "announcementvolume"
    announcementvolume_default = 1.0

    randomvoice = "randomvoice"
    randomvoice_default = False

    voicename = "voicename"
    voicename_default = ""

    def __init__(self):
        pass

    def __decode_configuration(self, configuration_filename):
        print(configuration_filename)
        with open(configuration_filename) as f:
            announcer_config = json.load(f)

        config = {}
        for key, value in announcer_config.items():
            config[key.lower()] = value
        print(config)

        m_announcement_volume = config.get(self.announcementvolume, self.announcementvolume_default)
        m_randomvoice = config.get(self.randomvoice, self.randomvoice_default)
        m_voicename = config.get(self.voicename, self.voicename_default)

        announcer = Announcer(volume=m_announcement_volume, random_voice=m_randomvoice, voice_name=m_voicename)
        announcer.configure()

        return announcer

    def decode_configuration(self, configuration_filename):
        return self.__decode_configuration(configuration_filename)

    def decode_common_configuration(self):
        return self.decode_configuration(self.common_config_location)
