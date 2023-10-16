# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-08 21:26:43
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Log methods.
"""


from typing import Any, Tuple, Optional, Union, Literal, Final, Callable, ClassVar, NoReturn, overload
from queue import Queue
from os.path import basename as os_basename
from logging import getLogger, Handler, StreamHandler, FileHandler, Formatter, LogRecord, DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, QueueHandler

from .rprint import rprint
from .rsystem import get_first_notnull, rexc, rstack
from .rtext import to_text
from .rwrap import start_thread


__all__ = (
    "RLog",
)


class RLog(object):
    """
    Rey's `log` type.
    """

    # State
    print_replaced: ClassVar[bool] = False

    # Default value.
    default_format: ClassVar[str] = "%(asctime)s.%(msecs)-3i | %(levelname)-8s | %(stack_filepath)s:%(stack_lineno)s | %(message_format)s"
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
            - `None` : Use attribute `default_format`.
            - `str` : Use this value.

        Returns
        -------
        Handler.
        """

        # Get parameter.
        format_ = get_first_notnull(format_, self.default_format, default="exception")

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
            - `None` : Use attribute `default_format`.
            - `str` : Use this value.

        Returns
        -------
        Handler.
        """

        # Get parameter.
        format_ = get_first_notnull(format_, self.default_format, default="exception")
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
        if exc_type is not None:
            messages = (
                exc_stack,
                *messages
            )

        ## Level.
        if level is None:
            if exc_type is None:
                level = INFO
            else:
                level = ERROR

        ## Stack.
        stack_params = rstack.get_stack_param("full", 2)
        stack_param = stack_params[-1]

        ### Compatible "__call__".
        if (
            stack_param["name"] in ("debug", "info", "warn", "error", "critical")
            and "\\reytool\\" in stack_param["filename"]
        ):
            stack_param = stack_params[-2]

        ### Compatible "print".
        if (
            stack_param["name"] == "preprocess"
            and "\\reytool\\" in stack_param["filename"]
        ):
            stack_param = stack_params[-3]

        ### Compatible "rprint".
        if (
            stack_param["name"] == "rprint"
            and "\\reytool\\" in stack_param["filename"]
        ):
            stack_param = stack_params[-4]

        file_name = os_basename(stack_param["filename"])
        extra = {
            "stack_filepath": stack_param["filename"],
            "stack_lineno": stack_param["lineno"],
            "stack_name": stack_param["name"],
            "stack_line": stack_param["line"],
            "stack_filename": file_name
        }

        ## Format message.
        message_format = "\n".join(
            [
                to_text(message, self.default_format_width)
                for message in messages
            ]
        )
        if "\n" in message_format:
            message_format = "\n" + message_format
        extra["message_format"] = message_format

        # Record.
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


    def warn(
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