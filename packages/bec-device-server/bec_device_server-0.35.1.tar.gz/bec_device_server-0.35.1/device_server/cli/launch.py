# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# we need to run the startup script before we import anything else. This is
# to ensure that the epics environment variables are set correctly.

try:
    from bec_plugins.device_server import startup
except ImportError:
    startup = None

if startup is not None:
    startup.run()


import argparse
import threading

from bec_lib.core import RedisConnector, ServiceConfig, bec_logger

import device_server

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.INFO


def main():
    """
    Launch the BEC device server.
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

    s = device_server.DeviceServer(config, RedisConnector)
    try:
        event = threading.Event()
        s.start()
        logger.success("Started DeviceServer")
        event.wait()
    except KeyboardInterrupt as e:
        s.shutdown()
