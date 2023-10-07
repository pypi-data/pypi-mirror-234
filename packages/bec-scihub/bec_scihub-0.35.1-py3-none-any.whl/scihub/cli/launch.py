import argparse
import threading

import scihub
from bec_lib.core import RedisConnector, ServiceConfig, bec_logger

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.INFO


def main():
    """
    Launch the SciHub connector.
    """

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--config",
        default="",
        help="path to the config file",
    )
    clargs = parser.parse_args()
    config_path = clargs.config

    config = ServiceConfig(config_path)

    sh = scihub.SciHub(config, RedisConnector)

    try:
        event = threading.Event()
        logger.success("Started SciHub connector")
        event.wait()
    except KeyboardInterrupt as e:
        sh.shutdown()
