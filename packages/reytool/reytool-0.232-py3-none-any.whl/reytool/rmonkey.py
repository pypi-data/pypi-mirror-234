# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-03-19 19:36:47
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Monkey patch methods.
"""


from __future__ import annotations


__all__ = (
    "sqlalchemy_add_result_more_fetch",
    "sqlalchemy_support_row_index_by_field",
    "pprint_modify_format_width_judgment"
)


def sqlalchemy_add_result_more_fetch():
    """
    `Modify` package `sqlalchemy`, add more fetch methods to CursorResult object.

    Returns
    -------
    SQL execute result object.
    """


    from typing import Optional
    from sqlalchemy.engine.cursor import CursorResult
    from pandas import DataFrame, NA, concat

    from .rprint import rprint
    from .rtable import to_table, to_dict, to_df, to_json, to_sql, to_html, to_csv, to_excel
    from .rtime import time_to


    # Fetch result as table in "List[Dict]" format.
    CursorResult.fetch_table = to_table

    # Fetch result as dictionary.
    CursorResult.fetch_dict = to_dict

    # Fetch result as DataFrame object.
    CursorResult.fetch_df = to_df

    # Fetch result as JSON string.
    CursorResult.fetch_json = to_json

    # Fetch result as SQL string.
    CursorResult.fetch_sql = to_sql

    # Fetch result as HTML string.
    CursorResult.fetch_html = to_html

    # Fetch result as save csv format file.
    CursorResult.fetch_csv = to_csv

    # Fetch result as save excel file.
    CursorResult.fetch_excel = to_excel


    # Print result.
    def print_result(self: RResult, limit: Optional[int] = None) -> None:
        """
        Print result.

        Parameters
        ----------
        limit : Limit row.
            - `>0` : Limit first few row.
            - `<0` : Limit last few row.
        """

        # Handle parameter.
        if limit is None:
            limit = 0

        # Convert.
        df: DataFrame = self.fetch_df()
        df = df.applymap(time_to, raising=False)
        df = df.astype(str)
        df.replace(["NaT", "<NA>"], "None", inplace=True)
        row_len, column_len = df.shape

        # Create omit row.
        omit_row = (("...",) * column_len,)
        omit_row = DataFrame(
            omit_row,
            columns=df.columns
        )

        # Limit.
        if (
            limit > 0
            and limit < row_len
        ):
            df = df.head(limit)
            omit_row.index = (row_len - 1,)
            df = concat((df, omit_row))
        elif (
            limit < 0
            and -limit < row_len
        ):
            df = df.tail(-limit)
            omit_row.index = (0,)
            df = concat((omit_row, df))

        # Print.
        rprint(df, title="Result")


    CursorResult.show = print_result


    # Update annotations.
    class RResult(CursorResult):
        """
        `Update` based on `CursorResult` object, for annotation return value.
        """

        # Inherit document.
        __doc__ = CursorResult.__doc__

        # Add more fetch methods.
        fetch_table = to_table
        fetch_dict = to_dict
        fetch_df = to_df
        fetch_json = to_json
        fetch_sql = to_sql
        fetch_html = to_html
        fetch_csv = to_csv
        fetch_excel = to_excel
        show = print_result


    return RResult


def sqlalchemy_support_row_index_by_field():
    """
    `Modify` package `sqlalchemy`, support Row object of package sqlalchemy index by field name.
    """


    from typing import Any, Tuple, Union, overload
    from sqlalchemy.engine.row import Row


    # Define method.
    @overload
    def __getitem__(self, index: Union[str, int]) -> Any: ...

    @overload
    def __getitem__(self, index: slice) -> Tuple: ...

    def __getitem__(self, index: Union[str, int, slice]) -> Union[Any, Tuple]:
        """
        `Index` row value.

        Parameters
        ----------
        index : Field name or subscript or slice.

        Returns
        -------
        Index result.
        """

        # Index.
        if index.__class__ == str:
            value = self._mapping[index]
        else:
            value = self._data[index]

        return value


    # Modify method.
    Row.__getitem__ = __getitem__


def pprint_modify_format_width_judgment() -> None:
    """
    Based on module `pprint.pformat`, `modify` the chinese width judgment.
    """


    from pprint import PrettyPrinter, _recursion
    from urwid import old_str_util


    # Chinese width can be determined.
    def get_width(text: str) -> int:
        """
        `Get` text `display width`.

        Parameters
        ----------
        text : Text.

        Returns
        -------
        Text display width.
        """

        # Get width.
        total_width = 0
        for char in text:
            char_unicode = ord(char)
            char_width = old_str_util.get_width(char_unicode)
            total_width += char_width

        return total_width


    # New method.
    def _format(_self, obj, stream, indent, allowance, context, level):
        objid = id(obj)
        if objid in context:
            stream.write(_recursion(obj))
            _self._recursive = True
            _self._readable = False
            return
        rep = _self._repr(obj, context, level)
        max_width = _self._width - indent - allowance
        width = get_width(rep)
        if width > max_width:
            p = _self._dispatch.get(type(obj).__repr__, None)
            if p is not None:
                context[objid] = 1
                p(_self, obj, stream, indent, allowance, context, level + 1)
                del context[objid]
                return
            elif isinstance(obj, dict):
                context[objid] = 1
                _self._pprint_dict(obj, stream, indent, allowance,
                                context, level + 1)
                del context[objid]
                return
        stream.write(rep)


    # Modify the chinese width judgment.
    PrettyPrinter._format = _format