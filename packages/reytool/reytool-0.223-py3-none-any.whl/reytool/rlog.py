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
        name: str = "Log",
        format_: Optional[str] = None
    ) -> None:
        """
        Build `log` instance.

        Parameters
        ----------
        name : Log name. When log name existed, then direct return, otherwise build.
        format_ : Log record format.
            - `None` : Use attribute `default_format`.
            - `str` : Use this value.
        """

        # Set parameter.
        self.name: Final[str] = name
        self.format = format_
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
        format_ : Print record format.

        Returns
        -------
        Handler.
        """

        # Get parameter.
        format_ = get_first_notnull(format_, self.format, self.default_format, default="exception")

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
        level: int = DEBUG,
        format_: Optional[str] = None,
        size: None = None,
        time: None = None
    ) -> FileHandler: ...

    @overload
    def add_file(
        self,
        path: Optional[str] = None,
        level: int = DEBUG,
        format_: Optional[str] = None,
        size: float = None,
        time: None = None
    ) -> RotatingFileHandler: ...

    @overload
    def add_file(
        self,
        path: Optional[str] = None,
        level: int = DEBUG,
        format_: Optional[str] = None,
        size: None = None,
        time: Union[float, Literal["w0", "w1", "w2", "w3", "w4", "w5", "w6"]] = None
    ) -> TimedRotatingFileHandler: ...

    @overload
    def add_file(
        self,
        path: Optional[str] = None,
        level: int = DEBUG,
        format_: Optional[str] = None,
        size: None = None,
        time: Any = None
    ) -> NoReturn: ...

    @overload
    def add_file(
        self,
        path: Optional[str] = None,
        level: int = DEBUG,
        format_: Optional[str] = None,
        size: float = None,
        time: Union[float, Literal["w0", "w1", "w2", "w3", "w4", "w5", "w6"]] = None
    ) -> NoReturn: ...

    def add_file(
        self,
        path: Optional[str] = None,
        level: int = DEBUG,
        format_: Optional[str] = None,
        size: Optional[float] = None,
        time: Optional[Union[float, Literal["w0", "w1", "w2", "w3", "w4", "w5", "w6"]]] = None
    ) -> Union[FileHandler, RotatingFileHandler, TimedRotatingFileHandler]:
        """
        Add `file output` handler.
        Can split files based on condition, only one split condition can be used.

        Parameters
        ----------
        path : File path.
            - `None` : Use '%s.log' %s self.name.
            - `str` : Use this value.

        level : Handler level.
        format_ : Print record format.
        size : File split condition, max megabyte. 
        time : File split condition, interval time.
            - `float` : Interval hours.
            - `Literal['w0', 'w1', 'w2', 'w3', 'w4', 'w5', 'w6']` : Fixed week, 'w0' is monday, 'w6' is sunday, and so on.

        Returns
        -------
        Handler.
        """

        # Get parameter.
        format_ = get_first_notnull(format_, self.format, self.default_format, default="exception")
        if path is None:
            path = "%s.log" % self.name

        # Create handler.

        ## Raise.
        if (
            size is not None
            and time is not None
        ):
            raise AssertionError("parameter 'mb' and 'time' cannot be used together")

        ## By size split.
        elif size is not None:
            size_mb = size * 1024 * 1024
            handler = RotatingFileHandler(
                path,
                "a",
                size_mb,
                100_0000
            )

        ## By time split.
        elif time is not None:

            ## Interval hours.
            if time.__class__ in (int, float):
                time_s = int(time * 60 * 60)
                handler = TimedRotatingFileHandler(
                    path,
                    "s",
                    time_s,
                    100_0000
                )

            ## Fixed week.
            elif (
                time.__class__ == str
                and time in ("w0", "w1", "w2", "w3", "w4", "w5", "w6")
            ):
                handler = TimedRotatingFileHandler(
                    path,
                    time,
                    backupCount=100_0000
                )

            ## Raise.
            else:
                rexc(ValueError, time)

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
        level: int = DEBUG,
        queue: Optional[Queue] = None
    ) -> Tuple[QueueHandler, Queue]:
        """
        Add `queue output` handler.

        Parameters
        ----------
        level : Handler level.
        queue : Queue instance.
            - `None` : Create queue and use.
            - `Queue` : Use this queue.

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
    def add_method(self, method: Callable[[LogRecord, Any, Any], Any], *args: Any, level: int = DEBUG, **kwargs: Any) -> None:
        """
        Add `method` handler.

        Parameters
        ----------
        method : Handler method. The first parameter is the `LogRecord` instance.
        level : Handler level.
        args : Position parameters of method function.
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
        level: int = INFO,
        message: Optional[Any] = None
    ) -> None:
        """
        Record log.

        Parameters
        ----------
        level : Record level.
        message : Record content.
        """

        # Get parameter.

        ## Stack.
        stack_param = rstack.get_stack_param(limit=3)
        file_name = os_basename(stack_param["filename"])
        extra = {
            "stack_filepath": stack_param["filename"],
            "stack_lineno": stack_param["lineno"],
            "stack_name": stack_param["name"],
            "stack_line": stack_param["line"],
            "stack_filename": file_name
        }

        ## Format message.
        message_format = to_text(message, self.default_format_width)
        if "\n" in message_format:
            message_format = "\n" + message_format
        extra["message_format"] = message_format

        # Record.
        self.logger.log(level, message, extra=extra)


    def debug(
        self,
        message: Optional[Any] = None
    ) -> None:
        """
        Record `debug` level log.

        Parameters
        ----------
        message : Record content.
        """

        # Record.
        self.log(DEBUG, message)


    def info(
        self,
        message: Optional[Any] = None
    ) -> None:
        """
        Record `info` level log.

        Parameters
        ----------
        message : Record content.
        """

        # Record.
        self.log(INFO, message)


    def warn(
        self,
        message: Optional[Any] = None
    ) -> None:
        """
        Record `warning` level log.

        Parameters
        ----------
        message : Record content.
        """

        # Record.
        self.log(WARNING, message)


    def error(
        self,
        message: Optional[Any] = None
    ) -> None:
        """
        Record `error` level log.

        Parameters
        ----------
        message : Record content.
        """

        # Record.
        self.log(ERROR, message)


    def critical(
        self,
        message: Optional[Any] = None
    ) -> None:
        """
        Record `critical` level log.

        Parameters
        ----------
        message : Record content.
        """

        # Record.
        self.log(CRITICAL, message)


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


    __call__ = info