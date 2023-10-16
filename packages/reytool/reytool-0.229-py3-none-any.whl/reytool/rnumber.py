# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-04-22 22:32:34
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Number methods.
"""


from typing import Any, Tuple, Union, Optional, Literal, overload
from random import randint as random_randint

from .rsystem import rexc, is_number_str


__all__ = (
    "digits",
    "randn",
    "number",
    "number_ch"
)


def digits(number: Union[int, float]) -> Tuple[int, int]:
    """
    `Judge` the number of integer digits and decimal digits.

    Parameters
    ----------
    number : Number to judge.

    Returns
    -------
    Integer digits and decimal digits.
    """

    # Handle parameter.
    number_str = str(number)

    # Get digits.
    if "." in number_str:
        int_str, dec_str = number_str.split(".")
        int_digits = len(int_str)
        dec_digits = len(dec_str)
    else:
        int_digits = len(number_str)
        dec_digits = 0

    return int_digits, dec_digits


@overload
def randn(*thresholds: int, precision: None = None) -> int: ...

@overload
def randn(*thresholds: float, precision: None = None) -> float: ...

@overload
def randn(*thresholds: float, precision: Literal[0] = None) -> int: ...

@overload
def randn(*thresholds: float, precision: int = None) -> float: ...

def randn(*thresholds: float, precision: Optional[int] = None) -> Union[int, float]:
    """
    `Get` random number.

    Parameters
    ----------
    thresholds : Low and high thresholds of random range, range contains thresholds.
        - When `length is 0`, then low and high thresholds is `0` and `10`.
        - When `length is 1`, then low and high thresholds is `0` and `thresholds[0]`.
        - When `length is 2`, then low and high thresholds is `thresholds[0]` and `thresholds[1]`.

    precision : Precision of random range, that is maximum decimal digits of return value.
        - `None` : Set to Maximum decimal digits of element of parameter `thresholds`.
        - `int` : Set to this value.

    Returns
    -------
    Random number.
        - When parameters `precision` is 0, then return int.
        - When parameters `precision` is greater than 0, then return float.
    """

    # Handle parameter.
    thresholds_len = len(thresholds)
    if thresholds_len == 0:
        threshold_low = 0
        threshold_high = 10
    elif thresholds_len == 1:
        threshold_low = 0
        threshold_high = thresholds[0]
    elif thresholds_len == 2:
        threshold_low = thresholds[0]
        threshold_high = thresholds[1]
    else:
        raise ValueError("number of parameter 'thresholds' must is 0 or 1 or 2")
    if precision is None:
        threshold_low_desimal_digits = digits(threshold_low)[1]
        threshold_high_desimal_digits = digits(threshold_high)[1]
        desimal_digits_max = max(threshold_low_desimal_digits, threshold_high_desimal_digits)
        precision = desimal_digits_max

    # Get random number.
    magnifier = 10 ** precision
    threshold_low = int(threshold_low * magnifier)
    threshold_high = int(threshold_high * magnifier)
    number = random_randint(threshold_low, threshold_high)
    number = number / magnifier

    # Convert Integer.
    if precision == 0:
        number = int(number)

    return number


def number(string: str) -> Union[int, float]:
    """
    convert `string` to `number`.

    Parameters
    ----------
    string : String.

    Returns
    -------
    Converted number.
    """

    # Number.
    if is_number_str(string):
        if "." in string:
            number = float(string)
        else:
            number = int(string)
        return number

    # Throw exception.
    else:
        rexc(ValueError, string)


def number_ch(number: int) -> str:
    """
    Convert `number` to `chinese number`.

    Parameters
    ----------
    number : Number to convert.

    Returns
    -------
    Chinese number.
    """

    # Import.
    from .rregular import sub_batch

    # Set parameter.
    map_digit = {
        "0": "零",
        "1": "一",
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "七",
        "8": "八",
        "9": "九",
    }
    map_digits = {
        0: "",
        1: "十",
        2: "百",
        3: "千",
        4: "万",
        5: "十",
        6: "百",
        7: "千",
        8: "亿",
        9: "十",
        10: "百",
        11: "千",
        12: "万",
        13: "十",
        14: "百",
        15: "千",
        16: "兆"
    }

    # Handle parameter.
    number_str = str(number)

    # Replace digit.
    for digit, digit_ch in map_digit.items():
        number_str = number_str.replace(digit, digit_ch)

    # Add digits.
    number_list = []
    for index, digit_ch in enumerate(number_str[::-1]):
        digits_ch = map_digits[index]
        number_list.insert(0, digits_ch)
        number_list.insert(0, digit_ch)
    number_str = "".join(number_list)

    # Delete redundant content.
    number_str = sub_batch(
        number_str,
        ("(?<=零)[^万亿兆]", ""),
        ("零+", "零"),
        ("零(?=[万亿兆])", "")
    )
    if number_str[0:2] == "一十":
        number_str = number_str[1:]
    if number_str[-1:] == "零":
        number_str = number_str[:-1]

    return number_str