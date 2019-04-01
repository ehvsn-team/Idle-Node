<<<<<<< HEAD
# -*- coding: utf-8 -*-

import time
import random
import logging

"""
logger.py

Wrapper module for logging

Basic Usage:
    ```
    import logger

    # Get a logging object.
    log_obj = logger.LoggingObject(
        name='SampleLogger',
        logfile='logfile.log'
        )

    # Set the log level to show.
    log_obj.set_logging_level('NOTSET')

    # Show logs in the screen.
    log_obj.enable_logging()

    log_obj.info("Sample Information message.")
    log_obj.warning("Sample warning message.")
    log_obj.error("Sample error message.")
    log_obj.debug("Sample debug message.")
    log_obj.critical("Sample critical message.")
    ```
"""


class LoggingObject:
    """
    class LoggingObject():
        The main class of Logger.

        :**kwargs name: Specify the name of the logging object.
    """

    def __init__(self, **kwargs):
        """
        def __init__():
            Initialization method of the logging object.

            :**kwargs name: Name of the logging object.
            :**kwargs session_id: Session ID of the logging object.
            :**kwargs logfile: Path of logfile to write data into.
        """

        # Set the name of the logger.
        self.name = kwargs.get('name', __name__)

        # Set the session ID of the logger.
        rand_id = random.randint(100000, 999999)
        self.session_id = kwargs.get('session_id', rand_id)
        del rand_id

        # Set the path of the logfile to write data into.
        self.logfile = kwargs.get('logfile', None)

        # Initialize the main logging object.
        self.logger = logging.getLogger(self.name)

        # Set the logging level.
        self.level = None

        # Set the time when the logger has started.
        self.start_time = time.asctime()

        # Set the current data
        self.log_datas = []  # All logs inf dict form {log_type:  message}
        self.log_data = ""  # Current/Latest log

    def _write(self, message):
        """
        def _write():
            Write data into a logfile.
        """

        # I didn't put a try/except block to let
        # the user to customize it.

        if self.logfile is None:
            return None

        else:
            with open(self.logfile, 'a') as fopen:
                fopen.write(message + '\n')

    def _format(self, message, logtype):
        """
        def _format():
            Format the message into a more informative one.

            :param message: Log message
        """

        result = ":{}: [{}] ({}) {}".format(
                logtype.upper(),
                str(self.session_id),
                time.strftime("%H:%M:%S %b %d %Y"),
                message
                )

        return result

    def get_all_log_datas(self):
        """
        def get_all_log_datas():
            Return the log data in a form of tuple in a list.
        """

        return self.log_datas

    def get_log_data(self, log_number):
        """
        def get_log_data():
            Get a specific log data.

            :param log_number: The index number to get the data of log number.
            :type int:

            :returns: Return the content of the specified log number.
            :return type: str
        """

        return self.log_datas[log_number]

    def get_latest_log_data(self):
        """
        def get_latest_log_data():
            Return the last message recieved by logger.
        """

        return self.log_data

    def set_logging_level(self, level):
        if level.upper() == "NOTSET":
            self.level = "NOTSET"

        elif level.upper() == "INFO":
            self.level = "INFO"

        elif level.upper() == "WARNING":
            self.level = "WARNING"

        elif level.upper() == "ERROR":
            self.level = "ERROR"

        elif level.upper() == "DEBUG":
            self.level = "DEBUG"

        elif level.upper() == "CRITICAL":
            self.level = "CRITICAL"

        else:
            raise ValueError("argument `level` must be `NOTSET`, `INFO`, `WARNING`, `ERROR`, `DEBUG`, or `CRITICAL`!")

    def enable_logging(self):
        """
        def enable_logging():
            Show logging information.
        """

        if self.level is None:
            raise self.LevelNotSetError("Logging level is not yet defined! Run `logger.LoggingObject().set_logging_level([LEVEL])` to set the level.")

        else:
            logging.basicConfig(level=self.level)

    def info(self, message):
        """
        def info():
            Log information.

            :param message: Log message.
        """

        message = self._format(message, 'info')
        self.log_datas.append((message, 'info'))
        self.log_data = (message, 'info')
        self.logger.info(message)
        self._write(message)

    def warning(self, message):
        """
        def warning():
            Log warnings.

            :param message: Log message.
        """

        message = self._format(message, 'warning')
        self.log_datas.append((message, 'warning'))
        self.log_data = (message, 'warning')
        self.logger.info(message)
        self._write(message)

    def error(self, message):
        """
        def error():
            Log errors.

            :param message: Log message.
        """

        message = self._format(message, 'error')
        self.log_datas.append((message, 'error'))
        self.log_data = (message, 'error')
        self.logger.info(message)
        self._write(message)

    def debug(self, message):
        """
        def debug():
            Log debugging information.

            :param message: Log message.
        """

        message = self._format(message, 'debug')
        self.log_datas.append((message, 'debug'))
        self.log_data = (message, 'debug')
        self.logger.info(message)
        self._write(message)

    def critical(self, message):
        """
        def critical():
            Log critical errors.

            :param message: Log message.
        """

        message = self._format(message, 'critical')
        self.log_datas.append((message, 'critical'))
        self.log_data = (message, 'critical')
        self.logger.info(message)
        self._write(message)

    class LevelNotSetError(Exception):
        """
        class LevelNotSetError():
            An exception class.
        """

        pass
