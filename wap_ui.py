
import argparse
from datetime import datetime
from wap_generator.ui.user_interface import UserInterface

import logging
import logging.config

logging.basicConfig(
    level=logging.getLevelName(logging.DEBUG),
)

fh = logging.FileHandler('logs/wap_{:%Y-%m-%d}.log'.format(datetime.now()))
formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
fh.setFormatter(formatter)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    UserInterface().run()
