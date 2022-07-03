
import argparse
from wap_generator.configuration.configuration_decoder import ConfigurationDecoder
from wap_generator.ui.user_interface import UserInterface


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    configuration_decoder = ConfigurationDecoder()
    configuration = configuration_decoder.decode_common_configuration()

    UserInterface().run()
