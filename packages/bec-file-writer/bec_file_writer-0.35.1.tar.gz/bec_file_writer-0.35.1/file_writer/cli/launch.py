import argparse
import os
import threading

import file_writer
from bec_lib.core import RedisConnector, ServiceConfig, bec_logger

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.INFO


def main():
    """
    Launch the file writer.
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

    file_writer_manager = file_writer.FileWriterManager(config, RedisConnector)
    file_writer_manager.file_writer.configure(
        layout_file=os.path.abspath("./layout_cSAXS_NXsas.xml")
    )
    try:
        event = threading.Event()
        logger.success("Started FileWriter")
        event.wait()
    except KeyboardInterrupt as e:
        file_writer_manager.shutdown()
