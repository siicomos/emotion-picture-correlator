#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: logger.py
# Description:
"""This class implements logger sub-package.
"""

import logging, logging.config
from os import path


class Logger:
    def __init__(
        self, logger_config_file: str = "logger.conf", level: str = "DEFAULT", loggers: list = None
    ):
        if loggers is None:
            loggers = []
        self.log_file_path = path.join(
            path.dirname(path.abspath(__file__)), logger_config_file
        )  # default config file
        logging.config.fileConfig(self.log_file_path, disable_existing_loggers=False)

        self.self_logger = logging.getLogger(__name__)  # this is a myself logger
        self.logger_list = []

        self.create_loggers(loggers)  # create logger
        self.logging_level = logging.INFO
        if level.upper() != "DEFAULT":
            self.parse_logging_level(level)
            logging.getLogger().setLevel(self.logging_level)
            if level.upper() == "NONE":
                for logger in self.logger_list:
                    self.self_logger.warning(f"\nLogger {logger.name} is omitted")
                logging.disable()
            # if(level.upper() == "DEBUG"):
            #     handler = logging.StreamHandler()
            #     handler.setLevel(logging.DEBUG)
            #     formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")
            #     handler.setFormatter(formatter)
            #     logging.getLogger("asyncio").addHandler(handler)

    def parse_logging_level(self, level):
        if level.upper() == "DEBUG":
            self.logging_level = logging.DEBUG
        elif level.upper() == "INFO":
            self.logging_level = logging.INFO
        elif level.upper() == "WARNING":
            self.logging_level = logging.WARNING
        elif level.upper() == "ERROR":
            self.logging_level = logging.ERROR
        elif level.upper() == "CRITICAL":
            self.logging_level = logging.CRITICAL
        elif level.upper() == "NONE":
            self.logging_level = logging.NOTSET
        else:
            self.self_logger.warning(
                "\nLogging level not recognized, possible logging level: DEBUG, INFO, WARNING, ERROR. CRITICAL\nBy default is INFO"
            )

    def create_loggers(self, logger_names):
        for logger_name in logger_names:
            self.logger_parser = logging.getLogger(logger_name)
            self.logger_list.append(self.logger_parser)
