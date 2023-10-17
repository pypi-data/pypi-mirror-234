# -*- coding: utf-8 -*-
import configparser
import os
import logging
from datetime import datetime
from logging import handlers
from threading import Lock


class LoggerUtils:
    """
    Singleton class for configuring and obtaining a logger instance.

    This class ensures that only one instance of the logger is created and shared among different parts of the codebase.
    It uses the Python 'logging' module to manage logging operations.

    Usage:
    Logger = LoggerUtils.get_logger()

    :return: Logger instance
    :rtype: logging.Logger
    """

    _instance = None
    _lock = Lock()

    @classmethod
    def get_logger(cls):
        """
        Retrieve or create a logger instance.

        If an instance already exists, it returns that instance; otherwise, it creates and configures a new logger instance.

        :return: Logger instance
        :rtype: logging.Logger
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls._configure_logging()
        return cls._instance

    @staticmethod
    def _configure_logging():
        """
        Configure the logger based on settings from 'pytest.ini'.

        This method reads log-related configuration parameters from the 'pytest.ini' file, such as log path and log name.
        If the file is not found or doesn't contain the required sections/options, default values are used.

        :return: Configured logger instance
        :rtype: logging.Logger
        """
        config = configparser.ConfigParser()
        try:
            with open("pytest.ini", 'r') as file:
                config.read_file(file)
                try:
                    log_path = config.get('log', 'log_path')
                except (configparser.NoSectionError, configparser.NoOptionError):
                    log_path = "reports/"
                try:
                    log_name = config.get('log', 'log_name')
                except (configparser.NoSectionError, configparser.NoOptionError):
                    log_name = "%Y%m%d%H%M%S.log"
        except FileNotFoundError:
            log_path = "reports/"
            log_name = "%Y%m%d%H%M%S.log"

        log_format = logging.Formatter('%(asctime)s - %(levelname)s - [ %(filename)s: %(lineno)d ] - %(message)s')
        log_directory = os.path.join(os.getcwd(), log_path)
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        log_name = datetime.now().strftime(log_name)
        file_name = os.path.join(log_path, log_name)

        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

        file_handler = handlers.TimedRotatingFileHandler(filename=file_name, when='midnight', backupCount=30,
                                                         encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

        logger.debug("======Now LOG BEGIN=======")
        return logger


Logger = LoggerUtils.get_logger()
