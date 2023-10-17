from logging import getLogger
from uuid import uuid1

from src.photonic._logging.configs import console_config, json_file_config


def main():
    logger_name = "test_logger"

    console_config(logger_name)
    json_file_config(logger_name)

    logger = getLogger(logger_name)

    logger.debug(f"Test Message from logger.debug #{uuid1}")
    logger.info(f"Test Message from logger.info #{uuid1}")
    logger.warning(f"Test Message from logger.warning #{uuid1}")
    logger.error(f"Test Message from logger.error #{uuid1}")
    logger.critical(f"Test Message from logger.critical #{uuid1}")


if __name__ == "__main__":
    main()
