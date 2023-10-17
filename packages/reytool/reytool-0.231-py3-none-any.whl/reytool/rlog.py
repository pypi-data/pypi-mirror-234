# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-08 21:26:43
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Log methods.
"""


from typing import Any, Tuple, Dict, Optional, Union, Literal, Final, Callable, ClassVar, NoReturn, overload
from queue import Queue
from os.path import abspath as os_abspath, basename as os_basename
from logging import getLogger, Handler, StreamHandler, FileHandler, Formatter, LogRecord, DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, QueueHandler
from re import sub as re_sub

from .rprint import rprint, abspath_rprint
from .rregular import search
from .rsystem import get_first_notnull, rexc, rstack
from .rtext import to_text
from .rwrap import start_thread


__all__ = (
    "RLog",
)


abspath_rlog = os_abspath(__file__)


class RLog(object):
    """
    Rey's `log` type.
    """

    # State
    print_replaced: ClassVar[bool] = False

    # Default value.
    default_format_print: ClassVar[str] = "\033[32m%(asctime)s.%(msecs)-3i\033[0m | %(levelname_color)s%(levelname)-8s\033[0m | \033[36m%(stack_filepath)s:%(stack_lineno)s\033[0m | %(message_color)s%(message_print)s\033[0m"
    default_format_file: ClassVar[str] = "%(asctime)s.%(msecs)-3i | %(levelname)-8s | %(stack_filepath)s:%(stack_lineno)s | %(message_file)s"
    default_format_date: ClassVar[str] = "%Y-%m-%d %H:%M:%S"
    default_format_width: ClassVar[int] = 100


    def __init__(
        self,
        name: str = "Log"
    ) -> None:
        """
        Build `log` instance.

        Parameters
        ----------
        name : Log name. When log name existed, then direct return, otherwise build.
        """

        # Set parameter.
        self.name: Final[str] = name
        self.stoped = False

        # Get logger.
        self.logger = getLogger(name)

        # Set level.
        self.logger.setLevel(DEBUG)


    def add_print(
        self,
        level: int = DEBUG,
        format_: Optional[str] = None
    ) -> StreamHandler:
        """
        Add `print output` handler.

        Parameters
        ----------
        level : Handler level.
        format_ : Record format.
            - `None` : Use attribute `default_format_print`.
            - `str` : Use this value.

        Returns
        -------
        Handler.
        """

        # Get parameter.
        format_ = get_first_notnull(format_, self.default_format_print, default="exception")

        # Create handler.
        handler = StreamHandler()
        formatter = Formatter(format_, self.default_format_date)
        handler.setFormatter(formatter)
        handler.setLevel(level)

        # Add.
        self.logger.addHandler(handler)

        return handler


    @overload
    def add_file(
        self,
        path: Optional[str] = None,
        mb: None = None,
        hour: None = None,
        level: int = DEBUG,
        format_: Optional[str] = None
    ) -> FileHandler: ...

    @overload
    def add_file(
        self,
        path: Optional[str] = None,
        mb: float = None,
        hour: None = None,
        level: int = DEBUG,
        format_: Optional[str] = None
    ) -> RotatingFileHandler: ...

    @overload
    def add_file(
        self,
        path: Optional[str] = None,
        mb: None = None,
        hour: float = None,
        level: int = DEBUG,
        format_: Optional[str] = None
    ) -> TimedRotatingFileHandler: ...

    @overload
    def add_file(
        self,
        path: Optional[str] = None,
        mb: float = None,
        hour: float = None,
        level: int = DEBUG,
        format_: Optional[str] = None
    ) -> NoReturn: ...

    def add_file(
        self,
        path: Optional[str] = None,
        mb: Optional[float] = None,
        hour: Optional[float] = None,
        level: int = DEBUG,
        format_: Optional[str] = None
    ) -> Union[FileHandler, RotatingFileHandler, TimedRotatingFileHandler]:
        """
        Add `file output` handler, can split files based on size or time.

        Parameters
        ----------
        path : File path.
            - `None` : Use '%s.log' %s self.name.
            - `str` : Use this value.

        mb : File split condition, max megabyte. Conflict with parameter `hour`. Cannot be less than 1, prevent infinite split file.
        hour : File split condition, interval hours. Conflict with parameter `mb`.

        level : Handler level.
        format_ : Record format.
            - `None` : Use attribute `default_format_file`.
            - `str` : Use this value.

        Returns
        -------
        Handler.
        """

        # Get parameter.
        format_ = get_first_notnull(format_, self.default_format_file, default="exception")
        if path is None:
            path = "%s.log" % self.name

        # Create handler.

        ## Raise.
        if (
            mb is not None
            and hour is not None
        ):
            raise AssertionError("parameter 'mb' and 'hour' cannot be used together")

        ## By size split.
        elif mb is not None:
            if mb < 1:
                rexc(ValueError, mb)
            byte = int(mb * 1024 * 1024)
            handler = RotatingFileHandler(
                path,
                "a",
                byte,
                100_0000
            )

        ## By time split.
        elif hour is not None:
            second = int(hour * 60 * 60)
            handler = TimedRotatingFileHandler(
                path,
                "s",
                second,
                100_0000
            )

        ## Not split.
        else:
            handler = FileHandler(
                path,
                "a"
            )

        formatter = Formatter(format_, self.default_format_date)
        handler.setFormatter(formatter)
        handler.setLevel(level)

        # Add.
        self.logger.addHandler(handler)

        return handler


    def add_queue(
        self,
        queue: Optional[Queue] = None,
        level: int = DEBUG
    ) -> Tuple[QueueHandler, Queue]:
        """
        Add `queue output` handler.

        Parameters
        ----------
        queue : Queue instance.
            - `None` : Create queue and use.
            - `Queue` : Use this queue.

        level : Handler level.

        Returns
        -------
        Handler and queue.
        """

        ## Create queue.
        if queue is None:
            queue = Queue()

        # Create handler.
        handler = QueueHandler(queue)
        handler.setLevel(level)

        # Add.
        self.logger.addHandler(handler)

        return handler, queue


    @start_thread
    def add_method(
        self,
        method: Callable[[LogRecord, Any, Any], Any],
        *args: Any,
        level: int = DEBUG,
        **kwargs: Any
    ) -> None:
        """
        Add `method` handler.

        Parameters
        ----------
        method : Handler method. The first parameter is the `LogRecord` instance.
        args : Position parameters of method function.
        level : Handler level.
        kwargs : Keyword parameters of method function.
        """

        # Add queue out.
        _, queue = self.add_queue(level)

        # Execute.
        while True:
            record: LogRecord = queue.get()
            method(record, *args, **kwargs)


    def delete_handler(self, handler: Optional[Handler] = None) -> None:
        """
        Delete handler.

        Parameters
        ----------
        handler : Handler.
            - `None` : Delete all handler.
            - `Handler` : Delete this handler.
        """

        # Delete.

        ## This.
        if handler is None:
            for handle in self.logger.handlers:
                self.logger.removeHandler(handle)

        ## All.
        else:
            self.logger.removeHandler(handler)


    def replace_print(self) -> None:
        """
        Use log `replace` print.
        """


        # Define.
        def preprocess(__s: str) -> str:
            """
            Preprocess function.

            Parameters
            ----------
            __s : Standard ouput text.

            Returns
            -------
            Preprocessed text.
            """

            # Break.
            if __s in ("\n", "[0m"): return

            # Log.
            self(__s)


        # Modify.
        rprint.modify(preprocess)

        # Update state.
        self.print_replaced = True


    def reset_print(self) -> None:
        """
        Reset log `replace` print.
        """

        # Break.
        if not self.print_replaced: return

        # Reset.
        rprint.reset()

        # Update state.
        self.print_replaced = False


    def _get_message_stack(self) -> Dict:
        """
        Get message stack parameters.

        Returns
        -------
        Stack parameters.
        """

        # Get parameter.
        stack_params = rstack.get_stack_param("full", 2)
        stack_param = stack_params[-2]

        # Compatible.

        ## Compatible "__call__".
        if (
            stack_param["filename"] == abspath_rlog
            and stack_param["name"] in ("debug", "info", "warning", "error", "critical")
        ):
            stack_param = stack_params[-3]

        ## Compatible "print".
        if (
            stack_param["filename"] == abspath_rlog
            and stack_param["name"] == "preprocess"
        ):
            stack_param = stack_params[-4]

        ## Compatible "rprint".
        if (
            stack_param["filename"] == abspath_rprint
            and stack_param["name"] == "rprint"
        ):
            stack_param = stack_params[-5]

        # Convert.
        file_name = os_basename(stack_param["filename"])
        params = {
            "stack_filepath": stack_param["filename"],
            "stack_lineno": stack_param["lineno"],
            "stack_name": stack_param["name"],
            "stack_line": stack_param["line"],
            "stack_filename": file_name
        }

        return params


    def _get_level_color_code(
        self,
        level: int
    ) -> str:
        """
        Get level color `ANSI code`.

        Parameters
        ----------
        level : Record level.

        Returns
        -------
        Level color ansi code.
        """

        # Set parameters.
        color_code_dict = {
            10: "\033[1;34m",
            20: "\033[1;37m",
            30: "\033[1;33m",
            40: "\033[1;31m",
            50: "\033[1;37;41m"
        }

        # Index.
        color_code = color_code_dict.get(level, "")

        return color_code


    def log(
        self,
        *messages: Optional[Any],
        level: Optional[int] = None
    ) -> None:
        """
        `Record` log.

        Parameters
        ----------
        messages : Record content.
        level : Record level.
            - `None` : Automatic judge.
                * `in 'except' syntax` : Use 'ERROR' level.
                * `Other` : Use 'INFO' level.
            - `int` : Use this value.
        """

        # Get parameter.

        ## Exception.
        exc_stack, exc_type, _, _ = rexc.catch()

        ## Level.
        if level is None:
            if exc_type is None:
                level = INFO
            else:
                level = ERROR

        ## Stack.
        message_stack = self._get_message_stack()

        ## Format message print.
        message_format = "\n".join(
            [
                to_text(message, self.default_format_width)
                for message in messages
            ]
        )
        if "\n" in message_format:
            message_format = "\n" + message_format
        message_print = message_format
        if exc_type is not None:
            message_print += "\n" + exc_stack

        ## Format message file.
        pattern = "\033\[[\d;]+?m"
        message_file = re_sub(pattern, "", message_format)

        ## Level color code.
        levelname_color = self._get_level_color_code(level)

        ## Message color code.
        pattern = "\033\[[\d;]+?m"
        result = search(pattern, message_format)
        if result is None:
            message_color = levelname_color
        else:
            message_color = "\033[1m"

        # Record.
        extra = {
            **message_stack,
            "message_print": message_print,
            "message_file": message_file,
            "levelname_color": levelname_color,
            "message_color": message_color
        }
        self.logger.log(level, messages, extra=extra)


    def debug(
        self,
        *messages: Optional[Any]
    ) -> None:
        """
        Record `debug` level log.

        Parameters
        ----------
        messages : Record content.
        """

        # Record.
        self.log(*messages, level=DEBUG)


    def info(
        self,
        *messages: Optional[Any]
    ) -> None:
        """
        Record `info` level log.

        Parameters
        ----------
        messages : Record content.
        """

        # Record.
        self.log(*messages, level=INFO)


    def warning(
        self,
        *messages: Optional[Any]
    ) -> None:
        """
        Record `warning` level log.

        Parameters
        ----------
        messages : Record content.
        """

        # Record.
        self.log(*messages, level=WARNING)


    def error(
        self,
        *messages: Optional[Any]
    ) -> None:
        """
        Record `error` level log.

        Parameters
        ----------
        messages : Record content.
        """

        # Record.
        self.log(*messages, level=ERROR)


    def critical(
        self,
        *messages: Optional[Any]
    ) -> None:
        """
        Record `critical` level log.

        Parameters
        ----------
        messages : Record content.
        """

        # Record.
        self.log(*messages, level=CRITICAL)


    def stop(self) -> None:
        """
        `Stop` record.
        """

        # Set level.
        self.logger.setLevel(100)

        # Update state.
        self.stoped = True


    def start(self) -> None:
        """
        `Start` record.
        """

        # Set level.
        self.logger.setLevel(DEBUG)

        # Update state.
        self.stoped = False


    def __del__(self) -> None:
        """
        Delete handle.
        """

        # Reset.
        self.reset_print()

        # Delete handler.
        self.delete_handler()


    __call__ = log