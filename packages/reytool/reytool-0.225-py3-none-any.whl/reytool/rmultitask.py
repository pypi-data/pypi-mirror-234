# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-19 20:06:20
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Multi task methods.
"""


from typing import Any, Tuple, Union, Optional, Callable, Generator
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from .rwrap import update_tqdm


__all__ = (
    "threads",
)


def threads(
    func: Callable,
    *args: Union[Tuple, Any],
    max_workers: Optional[int] = None,
    thread_name: Optional[str] = None,
    timeout: Optional[int] = None,
    to_tqdm: bool = False,
    **kwargs: Union[Tuple, Any]
) -> Generator:
    """
    Concurrent `multi tasks` using thread pool.

    Parameters
    ----------
    func : Task function.
    args : Position parameters of task function.
        - `Tuple` : Parameter sequence.
        - `Any` : Become shortest sequence.

    max_workers: Maximum number of threads.
        - `None` : Number of CPU + 4, 32 maximum.
        - `int` : Use this value, no maximum limit.

    thread_name: Thread name prefix.
        - `None` : Use function name.
        - `str` : Use this value.

    timeout : Call generator maximum waiting second, overtime throw exception.
        - `None` : Unlimited.
        - `int` : Use this value.

    to_tqdm : Whether print progress bar.
    kwargs : Keyword parameters of task function.
        - `Value is Tuple` : Value is parameter sequence.
        - `Value is Any` : Value is become shortest sequence.

    Returns
    -------
    Generator with multi Future object, object from concurrent package.
    When called, it will block until all tasks are completed.
    When `for` syntax it, the task that complete first return first.

    Examples
    --------
    Get value.
    >>> func = lambda a, b, c, d: (a, b, c, d)
    >>> generator = threads(func, 0, (1, 2), c=10, d=(11, 12, 13))
    >>> [future.result() for future in generator]
    [(0, 1, 10, 11), (0, 2, 10, 12)]
    """

    # Handle parameter.

    ## Thread name.
    if thread_name is None:
        thread_name = func.__name__

    ## Element min length.
    element_len_set = {
        len(element)
        for element in [
            *args,
            *kwargs.values()
        ]
        if element.__class__ == tuple
    }
    if element_len_set == set():
        element_len_min = 0
    else:
        element_len_min = min(element_len_set)

    # Lengthen element.
    args = [
        element
        if element.__class__ == tuple
        else [element] * element_len_min
        for element in args
    ]
    kwargs = [
        [
            [key, value_]
            for value_ in value
        ]
        if value.__class__ == tuple
        else [(key, value)] * element_len_min
        for key, value in kwargs.items()
    ]

    # Zip element.
    args = zip(*args)
    kwargs = zip(*kwargs)
    kwargs = [dict(params) for params in kwargs]
    if kwargs == []:
        kwargs = [{}] * element_len_min
    data = zip(args, kwargs)

    # Create thread pool.
    thread_pool = ThreadPoolExecutor(max_workers, thread_name)

    # Add progress bar.
    if to_tqdm:
        tqdm_desc = "ThreadPool " + thread_name
        obj_tqdm = tqdm(desc=tqdm_desc, total=element_len_min)
        func = update_tqdm(func, obj_tqdm, _execute=False)

    # Start thread pool.
    tasks = [
        thread_pool.submit(func, *args, **kwargs)
        for args, kwargs in data
    ]

    # Return generator.
    obj_tasks = as_completed(tasks, timeout)
    return obj_tasks