# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:02
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database execute methods.
"""


from __future__ import annotations
from typing import Any, List, Dict, Tuple, Union, Optional, Literal, overload

from .rdb_engine import REngine, RConnection, RResult
from ..rsystem import rexc
from ..rtable import Table


class RExecute(object):
    """
    Rey's `database execute` type.

    Examples
    --------
    Execute.
    >>> sql = 'select :value'
    >>> result = RExecute(sql, value=1)

    Select.
    >>> field = ["id", "value"]
    >>> where = "`id` = ids"
    >>> ids = (1, 2)
    >>> result = RExecute.database.table(field, where, ids=ids)

    Insert.
    >>> data = [{'id': 1}, {'id': 2}]
    >>> duplicate = 'ignore'
    >>> result = RExecute.database.table + data
    >>> result = RExecute.database.table + (data, duplicate)
    >>> result = RExecute.database.table + {"data": data, "duplicate": duplicate}

    Update.
    >>> data = [{'name': 'a', 'id': 1}, {'name': 'b', 'id': 2}]
    >>> where_fields = 'id'
    >>> result = RExecute.database.table & data
    >>> result = RExecute.database.table & (data, where_fields)
    >>> result = RExecute.database.table & {"data": data, "where_fields": where_fields}

    Delete.
    >>> where = '`id` IN (1, 2)'
    >>> report = True
    >>> result = RExecute.database.table - where
    >>> result = RExecute.database.table - (where, report)
    >>> result = RExecute.database.table - {"where": where, "report": report}

    Copy.
    >>> where = '`id` IN (1, 2)'
    >>> limit = 1
    >>> result = RExecute.database.table * where
    >>> result = RExecute.database.table * (where, limit)
    >>> result = RExecute.database.table * {"where": where, "limit": limit}

    Exist.
    >>> where = '`id` IN (1, 2)'
    >>> report = True
    >>> result = where in RExecute.database.table
    >>> result = (where, report) in RExecute.database.table
    >>> result = {"where": where, "report": report} in RExecute.database.table

    Count.
    >>> result = len(RExecute.database.table)

    Default database.
    >>> field = ["id", "value"]
    >>> engine = REngine(**server, database)
    >>> result = engine.exe.table()
    """


    def __init__(self, rengine: Union[REngine, RConnection]) -> None:
        """
        Build `database execute` instance.

        Parameters
        ----------
        rengine : REngine object or RConnection object.
        """

        # Set parameter.
        self._rengine = rengine
        self._path: List[str] = []


    @overload
    def __getattr__(self, key: Literal["_rengine"]) -> Union[REngine, RConnection]: ...

    @overload
    def __getattr__(self, key: Literal["_path"]) -> List[str]: ...

    @overload
    def __getattr__(self, key: str) -> RExecute: ...

    def __getattr__(self, key: str) -> Union[
        Union[REngine, RConnection],
        List[str],
        RExecute
    ]:
        """
        Get `attribute` or set `database name` or set `table name`.

        Parameters
        ----------
        key : Attribute key or database name or table name.

        Returns
        -------
        Value of attribute or self.
        """

        # Filter private
        if key in ("_rengine", "_path"):
            return self.__dict__[key]

        # Check parameter.
        if len(self._path) not in (0, 1):
            rexc(AssertionError)

        # Set parameter.
        self._path.append(key)

        return self


    def _get_path(self, raising: bool = True) -> Tuple[str, str]:
        """
        Get database name and table name.

        Parameters
        ----------
        raising : Whether throw exception, when usage error, otherwise return None.

        Returns
        -------
        Database name and table name.
        """

        # Get.
        path_len = len(self._path)
        if path_len == 1:
            database = self._rengine.database
            table = self._path[0]
        elif path_len == 2:
            database = self._path[0]
            table = self._path[1]
        elif raising:
            rexc(AssertionError)
        else:
            return

        return database, table


    def __call__(
        self,
        *args: Any,
        **kwargs: Any
    ) -> RResult:
        """
        `Execute` SQL or `Select` the data of table in the datebase.

        Parameters
        ----------
        args : Position parameters.
        kwargs : Keyword parameters.

        Returns
        -------
        Result object.
        """

        # Get parameter.
        path = self._get_path(False)

        # Execute.
        if path is None:
            result = self._rengine.execute(*args, **kwargs)

        # Selete.
        else:
            result = self._rengine.execute_select(path, *args, **kwargs)

        return result


    def __add__(
        self,
        params: Union[Tuple, Dict, Table]
    ) -> RResult:
        """
        `Insert` the data of table in the datebase.

        Parameters
        ----------
        params : Insert parameters.
            - `Tuple` : Enter parameters in '(path, *params)' format.
            - `Dict` : Enter parameters in '(path, **params)' format.
            - `Table` : Enter parameters in '(path, params)' format.

        Returns
        -------
        Result object.
        """

        # Get parameter.
        path = self._get_path()

        # Insert.
        if params.__class__ == tuple:
            result = self._rengine.execute_insert(path, *params)
        elif params.__class__ == dict:
            result = self._rengine.execute_insert(path, **params)
        else:
            result = self._rengine.execute_insert(path, params)

        return result


    def __and__(
        self,
        params: Union[Tuple, Dict, Table]
    ) -> RResult:
        """
        `Update` the data of table in the datebase.

        Parameters
        ----------
        params : Update parameters.
            - `Tuple` : Enter parameters in '(path, *params)' format.
            - `Dict` : Enter parameters in '(path, **params)' format.
            - `Table` : Enter parameters in '(path, params)' format.

        Returns
        -------
        Result object.
        """

        # Get parameter.
        path = self._get_path()

        # Update.
        if params.__class__ == tuple:
            result = self._rengine.execute_update(path, *params)
        elif params.__class__ == dict:
            result = self._rengine.execute_update(path, **params)
        else:
            result = self._rengine.execute_update(path, params)

        return result


    def __sub__(
        self,
        params: Union[Tuple, Dict, str]
    ) -> RResult:
        """
        `Delete` the data of table in the datebase.

        Parameters
        ----------
        params : Update parameters.
            - `Tuple` : Enter parameters in '(path, *params)' format.
            - `Dict` : Enter parameters in '(path, **params)' format.
            - `str` : Enter parameters in '(path, params)' format.

        Returns
        -------
        Result object.
        """

        # Get parameter.
        path = self._get_path()

        # Update.
        if params.__class__ == tuple:
            result = self._rengine.execute_delete(path, *params)
        elif params.__class__ == dict:
            result = self._rengine.execute_delete(path, **params)
        else:
            result = self._rengine.execute_delete(path, params)

        return result


    def __mul__(
        self,
        params: Union[Tuple, Dict, str]
    ) -> RResult:
        """
        `Copy` record of table in the datebase.

        Parameters
        ----------
        params : Update parameters.
            - `Tuple` : Enter parameters in '(path, *params)' format.
            - `Dict` : Enter parameters in '(path, **params)' format.
            - `str` : Enter parameters in '(path, params)' format.

        Returns
        -------
        Result object.
        """

        # Get parameter.
        path = self._get_path()

        # Update.
        if params.__class__ == tuple:
            result = self._rengine.execute_copy(path, *params)
        elif params.__class__ == dict:
            result = self._rengine.execute_copy(path, **params)
        else:
            result = self._rengine.execute_copy(path, params)

        return result


    def __contains__(
        self,
        params: Union[Tuple, Dict, str]
    ) -> bool:
        """
        Judge the `exist` of record.

        Parameters
        ----------
        params : Update parameters.
            - `Tuple` : Enter parameters in '(path, *params)' format.
            - `Dict` : Enter parameters in '(path, **params)' format.
            - `str` : Enter parameters in '(path, params)' format.

        Returns
        -------
        Result object.
        """

        # Get parameter.
        path = self._get_path()

        # Update.
        if params.__class__ == tuple:
            result = self._rengine.execute_exist(path, *params)
        elif params.__class__ == dict:
            result = self._rengine.execute_exist(path, **params)
        else:
            result = self._rengine.execute_exist(path, params)

        return result


    def __len__(
        self
    ) -> int:
        """
        `Count` records.

        Returns
        -------
        Record count.
        """

        # Get parameter.
        path = self._get_path()

        # Update.
        result = self._rengine.execute_count(path)

        return result