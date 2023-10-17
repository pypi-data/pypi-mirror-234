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
custom_loggers: A module providing custom logger functionality.

This module contains classes for creating custom loggers with advanced features such as
inserting process IDs and function names into log messages, as well as emitting log
records by calling a specified log function.

Classes:
    - CustomLogger: A custom logger supporting process ID and function name insertion.
    - UILogHandler: A custom logging handler for emitting log records through a log function.
"""
import threading
import logging
from contextlib import contextmanager
import inspect
import threading


class CustomLogger(logging.Logger):
    """
    A custom logger that supports inserting process ID and function name into log messages.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the CustomLogger.

        Args:
            *args: Variable length arguments to be passed to the base class logger.
            **kwargs: Arbitrary keyword arguments to be passed to the base class logger.
        """
        super().__init__(*args, **kwargs)
        self.thread_local = threading.local()
    def debug(self, msg, *args, **kwargs):
        """
        Log a debug-level message.

        Args:
            msg (str): The log message to be recorded.
            *args: Variable length arguments to be passed to the log message.
            **kwargs: Arbitrary keyword arguments to be passed to the log message.
        """
        custom_msg = self.get_custome_msg(msg)
        super().debug(custom_msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Log an info-level message.

        Args:
            msg (str): The log message to be recorded.
            *args: Variable length arguments to be passed to the log message.
            **kwargs: Arbitrary keyword arguments to be passed to the log message.
        """
        custom_msg = self.get_custome_msg(msg)
        super().info(custom_msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Log a warning-level message.

        Args:
            msg (str): The log message to be recorded.
            *args: Variable length arguments to be passed to the log message.
            **kwargs: Arbitrary keyword arguments to be passed to the log message.
        """
        custom_msg = self.get_custome_msg(msg)
        super().warning(custom_msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Log an error-level message.

        Args:
            msg (str): The log message to be recorded.
            *args: Variable length arguments to be passed to the log message.
            **kwargs: Arbitrary keyword arguments to be passed to the log message.
        """
        custom_msg = self.get_custome_msg(msg)
        super().error(custom_msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Log a critical-level message.

        Args:
            msg (str): The log message to be recorded.
            *args: Variable length arguments to be passed to the log message.
            **kwargs: Arbitrary keyword arguments to be passed to the log message.
        """
        custom_msg = self.get_custome_msg(msg)
        super().critical(custom_msg, *args, **kwargs)

    def get_custome_msg(self, msg):
        """
        Get the custom log message with process ID and function name.

        Args:
            msg (str): The original log message.

        Returns:
            str: The custom log message with process ID and function name, if available.
        """
        frame = inspect.currentframe().f_back.f_back
        func_name = frame.f_code.co_name
        proc_id = getattr(self.thread_local, 'proc_id', None)
        is_print_func_name = getattr(self.thread_local, 'is_print_func_name', False)

        custom_msg = msg
        if is_print_func_name:
            custom_msg = f"{func_name} - {custom_msg}"
        if proc_id:
            custom_msg = f"{proc_id} - {custom_msg}"
        return custom_msg

    @contextmanager
    def insert_func_name(self):
        """
        Context manager to enable printing the function name in log messages within the block.

        Usage:
            with logger.insert_func_name():
                logger.info('This message will include the function name.')

        Note:
            Log messages outside the block will not include the function name.
        """
        setattr(self.thread_local, 'is_print_func_name', True)
        try:
            yield
        finally:
            setattr(self.thread_local, 'is_print_func_name', False)

    @contextmanager
    def insert_proc_id(self, proc_id: str):
        """
        Context manager to insert a process ID into log messages within the block.

        Args:
            proc_id (str): The process ID to be included in log messages.

        Usage:
            with logger.insert_proc_id('123'):
                logger.info('This message will include the process ID.')

        Note:
            Log messages outside the block will not include the process ID.
        """
        setattr(self.thread_local, 'proc_id', proc_id)
        try:
            yield
        finally:
            setattr(self.thread_local, 'proc_id', None)


class UILogHandler(logging.Handler):
    """
    Custom logging handler that emits log records by calling a specified log function.
    """

    def __init__(self, log_func):
        """
        Initialize the UILogHandler.

        Args:
            log_func (callable): The log function to be called for emitting log records.
        """
        super().__init__()
        self.log_func = log_func

    def emit(self, record):
        """
        Emit a log record by calling the specified log function.

        Args:
            record (logging.LogRecord): The log record to be emitted.
        """
        msg = self.format(record)
        self.log_func(msg)
