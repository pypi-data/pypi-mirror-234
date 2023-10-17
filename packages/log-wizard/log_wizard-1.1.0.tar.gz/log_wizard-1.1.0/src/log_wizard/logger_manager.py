#Copyright 2023 izharus
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
"""
custom_logger: A module providing custom logger functionality.

This module contains classes for creating custom loggers with advanced features such as
inserting process IDs and function names into log messages, as well as emitting log
records by calling a specified log function.

Classes:
    - CustomLogger: A custom logger supporting process ID and function name insertion.
    - UILogHandler: A custom logging handler for emitting log records through a log function.
"""
import datetime
import os
import logging
from typing import Callable, Any
from .custom_loggers import CustomLogger, UILogHandler


class DefaultConfig:
    """
    Singleton class for managing default configuration settings.

    This class provides a single instance to manage default configuration settings for the application,
    such as log file locations, log file postfixes, UI logging function, and console log printing.

    Attributes:
        ui_log_func (Callable[[str], Any]): A custom function for logging to the UI.
        info_file_postfix (str): The postfix for info log files.
        debug_file_postfixh (str): The postfix for debug log files.
        is_print_in_con (bool): Flag to enable printing log messages to the console.
        log_dir (str): The directory to store log files.

    Usage:
        To access the default configuration, use the DefaultConfig singleton instance:
        default_config = DefaultConfig(log_dir = 'data_log')
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Create a new DefaultConfig instance if one does not already exist."""
        if cls._instance is None:
            cls._instance = super(DefaultConfig, cls).__new__(cls)
            cls._instance.init_config(*args, **kwargs)
        return cls._instance

    # pylint: disable=W0201
    def init_config(
        self,
        log_dir: str = "data/log",
        info_file_postfix="log_info.txt",
        debug_file_postfixh="log_debug.txt",
        ui_log_func: Callable[[str], Any] = None,
        is_print_in_con=True,
    ):
        """
        Initialize the configuration for DefaultConfig.

        Args:
            log_dir (str, optional): The directory to store log files. Defaults to "data/log".
            info_file_postfix (str, optional): The postfix for info log files. Defaults to 'log_info.txt'.
            debug_file_postfixh (str, optional): The postfix for debug log files. Defaults to 'log_debug.txt'.
            ui_log_func (Callable[[str], Any], optional): A custom function for logging to the UI. Defaults to None.
            is_print_in_con (bool, optional): Flag to enable printing log messages to the console. Defaults to True.

        Returns:
            None
        """
        self.ui_log_func = ui_log_func
        self.info_file_postfix = info_file_postfix
        self.debug_file_postfixh = debug_file_postfixh
        self.is_print_in_con = is_print_in_con
        self.log_dir = log_dir


class CustomLoggerManager:
    """
    A manager for creating and configuring custom loggers.

    This class follows the singleton pattern to ensure that only one instance of a logger manager is created.

    Args:
        default_config (DefaultConfig, optional): The default logging configuration. If not provided, a default configuration is used.

    Attributes:
        logger (logging.Logger): The custom logger instance configured by this manager.

    Usage:
        To access the custom logger, use the log() function:
        log().info("some info")
        log().error("some error")
        with log().insert_proc_id(proc_id):
            log().info("here should be proc id")
            with log().insert_func_name():
                log().info("here also should be proc id and a func name")
    """

    _instance = None

    def __new__(cls, default_config: DefaultConfig = None):
        """Create a new instance of CustomLoggerManager or return
        the existing instance if one exists."""
        if cls._instance is None:
            cls._instance = super(CustomLoggerManager, cls).__new__(cls)
            cls._instance.init_logger(default_config)
        return cls._instance

    # pylint: disable=W0201
    def init_logger(self, default_config: DefaultConfig = None) -> None:
        """
        Initialize the custom logger instance based on the provided or default configuration.

        Args:
            default_config (DefaultConfig, optional): The default logging configuration.
                If not provided, a default configuration is used.
        """
        if default_config is None:
            default_config = DefaultConfig()
        self.logger = self.init_logging(default_config)

    @staticmethod
    def get_custome_logger(logger_name="forgelog") -> CustomLogger:
        """
        Get a custom logger instance with the specified name.

        Args:
            logger_name (str, optional): The name of the logger. Defaults to 'forgelog'.

        Returns:
            logging.Logger: A custom logger instance.

        """
        # Check if the logger with the specified name already exists
        if logger_name in logging.Logger.manager.loggerDict:
            return logging.getLogger(logger_name)
        logger = CustomLogger(logger_name)
        logging.Logger.manager.loggerDict[logger_name] = logger
        return logger

    @staticmethod
    def create_filehandler(
        default_config, log_level, log_formatter, file_postfix
    ) -> logging.FileHandler:
        """
        Create a file handler for logging.

        Args:
            default_config (DefaultConfig): The default logging configuration.
            log_level (int): The log level for the handler.
            log_formatter (logging.Formatter): The log message formatter.
            file_postfix (str): The postfix for log files.

        Returns:
            logging.FileHandler: A file handler for logging.

        """
        os.makedirs(default_config.log_dir, exist_ok=True)

        # Get the current month and year
        current_month = datetime.datetime.now().strftime("%m")
        current_year = datetime.datetime.now().strftime("%Y")

        # Create the log file name using the current month and year
        log_file_name = f"{current_month}.{current_year}.{file_postfix}"
        # Create the full path to the log file
        log_file_path = os.path.join(default_config.log_dir, log_file_name)

        # Configure the logging module

        file_handler = logging.FileHandler(log_file_path, mode="a")
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(log_level)

        return file_handler

    @classmethod
    def init_logging(cls, default_config: DefaultConfig) -> CustomLogger:
        """
        Initialize the logging configuration based on the provided or default configuration.

        Args:
            default_config (DefaultConfig): The default logging configuration.

        Returns:
            logging.Logger: The custom logger instance.

        """
        os.makedirs(default_config.log_dir, exist_ok=True)
        log_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%d.%m.%Y %H:%M:%S"
        )
        file_handler_info = cls.create_filehandler(
            default_config, logging.INFO, log_formatter, default_config.info_file_postfix
        )
        file_handler_debug = cls.create_filehandler(
            default_config,
            logging.DEBUG,
            log_formatter,
            default_config.debug_file_postfixh,
        )

        # file_handler_info = create_filehandler
        # Get the root logger and add the handlers
        # logger = logging.getLogger()
        logger = cls.get_custome_logger()
        logger.handlers = []
        # Each handlers could have own log level, because this func
        # could be called multiple times
        logger.addHandler(file_handler_info)
        logger.addHandler(file_handler_debug)

        # Create a console handler
        if default_config.is_print_in_con:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_formatter)
            console_handler.setLevel(logging.INFO)
            logger.addHandler(console_handler)
        # A file handler for saving logs to the file
        if default_config.ui_log_func:
            ui_handler = UILogHandler(default_config.ui_log_func)
            ui_handler.setFormatter(log_formatter)
            ui_handler.setLevel(logging.DEBUG)
            logger.addHandler(ui_handler)
        return logger


def log() -> CustomLogger:
    """Emitting the log message."""
    logger_instance = CustomLoggerManager()
    return logger_instance.logger
