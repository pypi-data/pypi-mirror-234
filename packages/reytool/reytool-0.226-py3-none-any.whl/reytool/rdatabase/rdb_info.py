# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:02
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database information methods.
"""


from __future__ import annotations
from typing import Any, List, Dict, Union, Literal, Optional, overload

from .rdb_engine import REngine, RConnection


class RInfo(object):
    """
    Rey's `database base information` type.
    """


    @overload
    def __call__(self, name: None = None) -> List[Dict]: ...

    @overload
    def __call__(self: RInfoSchema, name: str = None) -> RInfoDatabase: ...

    @overload
    def __call__(self: RInfoDatabase, name: str = None) -> RInfoTable: ...

    @overload
    def __call__(self: RInfoTable, name: str = None) -> RInfoColumn: ...

    def __call__(self, name: Optional[str] = None) -> Union[
        List[Dict],
        RInfoDatabase,
        RInfoTable,
        RInfoColumn
    ]:
        """
        Get information table or subclass instance.

        Parameters
        ----------
        name : 

        Returns
        -------
        Information table or subclass instance.
        """

        # Information table.
        if name is None:

            ## Break.
            if "_get_info_table" not in self.__dir__():
                raise AssertionError("class '%s' does not have this method" % self.__class__.__name__)

            ## Get.
            result: List[Dict] = self._get_info_table()

        # Subobject.
        else:

            ## Break.
            if "__getattr__" not in self.__dir__():
                raise AssertionError("class '%s' does not have this method" % self.__class__.__name__)

            ## Get.
            result = self.__getattr__(name)

        return result


    @overload
    def __getitem__(self, key: Literal["*", "all", "ALL"]) -> Dict: ...

    @overload
    def __getitem__(self, key: str) -> Any: ...

    def __getitem__(self, key: str) -> Any:
        """
        Get information attribute value or dictionary.

        Parameters
        ----------
        key : Attribute key. When key not exist, then try all caps key.
            - `Literal['*', 'all', 'ALL']` : Get attribute dictionary.
            - `str` : Get attribute value.

        Returns
        -------
        Information attribute value or dictionary.
        """

        # Break.
        if "_get_info_attrs" not in self.__dir__():
            raise AssertionError("class '%s' does not have this method" % self.__class__.__name__)

        # Get.
        info_attrs: Dict = self._get_info_attrs()

        # Return.

        ## Dictionary.
        if key in ("*", "all", "ALL"):
            return info_attrs

        ## Value.
        info_attr = info_attrs.get(key)
        if info_attr is None:
            key_upper = key.upper()
            info_attr = info_attrs[key_upper]
        return info_attr


    @overload
    def __getattr__(self, key: Literal["_rengine"]) -> Union[REngine, RConnection]: ...

    @overload
    def __getattr__(self, key: Literal["_database_name", "_table_name"]) -> str: ...

    @overload
    def __getattr__(self: RInfoSchema, key: str) -> RInfoDatabase: ...

    @overload
    def __getattr__(self: RInfoDatabase, key: str) -> RInfoTable: ...

    @overload
    def __getattr__(self: RInfoTable, key: str) -> RInfoColumn: ...

    def __getattr__(self, key: str) -> Union[
        Union[REngine, RConnection],
        str,
        RInfoDatabase,
        RInfoTable,
        RInfoColumn
    ]:
        """
        Get `attribute` or build subclass instance.

        Parameters
        ----------
        key : Attribute key or table name.

        Returns
        -------
        Attribute or subclass instance.
        """

        # Filter private
        if key in ("_rengine", "_database_name", "_table_name"):
            return self.__dict__[key]

        # Build.
        if self.__class__ == RInfoSchema:
            rtable = RInfoDatabase(self._rengine, key)
        elif self.__class__ == RInfoDatabase:
            rtable = RInfoTable(self._rengine, self._database_name, key)
        elif self.__class__ == RInfoTable:
            rtable = RInfoColumn(self._rengine, self._database_name, self._table_name, key)
        else:
            raise AssertionError("class '%s' does not have this method" % self.__class__.__name__)

        return rtable


class RInfoSchema(RInfo):
    """
    Rey's `database schema information` type.

    Examples
    --------
    Get databases information of server.
    >>> databases_info = RInfoSchema()

    Get tables information of database.
    >>> tables_info = RInfoSchema.database()

    Get columns information of table.
    >>> columns_info = RInfoSchema.database.table()

    Get database attribute.
    >>> database_attr = RInfoSchema.database["attribute"]

    Get table attribute.
    >>> database_attr = RInfoSchema.database.table["attribute"]

    Get column attribute.
    >>> database_attr = RInfoSchema.database.table.column["attribute"]
    """


    def __init__(
        self,
        rengine: Union[REngine, RConnection]
    ) -> None:
        """
        Build `database schema information` instance.

        Parameters
        ----------
        rengine : REngine object or RConnection object.
        """

        # Set parameter.
        self._rengine = rengine


    def _get_info_table(self) -> List[Dict]:
        """
        Get information table.

        Returns
        -------
        Information table.
        """

        # Select.
        result = self._rengine.execute_select(
            "information_schema.SCHEMATA",
            order="`schema_name`"
        )

        # Convert.
        info_table = result.fetch_table()

        return info_table


class RInfoDatabase(RInfo):
    """
    Rey's `database library information` type.

    Examples
    --------
    Get tables information of database.
    >>> tables_info = RInfoDatabase()

    Get columns information of table.
    >>> columns_info = RInfoDatabase.table()

    Get database attribute.
    >>> database_attr = RInfoDatabase["attribute"]

    Get table attribute.
    >>> database_attr = RInfoDatabase.table["attribute"]

    Get column attribute.
    >>> database_attr = RInfoDatabase.table.column["attribute"]
    """


    def __init__(
        self,
        rengine: Union[REngine, RConnection],
        database_name: str
    ) -> None:
        """
        Build `database library information` instance.

        Parameters
        ----------
        rengine : REngine object or RConnection object.
        database_name : Database name.
        """

        # Set parameter.
        self._rengine = rengine
        self._database_name = database_name


    def _get_info_attrs(self) -> Dict:
        """
        Get information attribute dictionary.

        Returns
        -------
        Information attribute dictionary.
        """

        # Select.
        where = "`SCHEMA_NAME` = :database_name"
        result = self._rengine.execute_select(
            "information_schema.SCHEMATA",
            where=where,
            limit=1,
            database_name=self._database_name
        )

        # Check.
        assert result.rowcount != 0, "database '%s' not exist" % self._database_name

        # Convert.
        info_table = result.fetch_table()
        info_attrs = info_table[0]

        return info_attrs


    def _get_info_table(self) -> List[Dict]:
        """
        Get information table.

        Returns
        -------
        Information table.
        """

        # Select.
        where = "`TABLE_SCHEMA` = :database_name"
        result = self._rengine.execute_select(
            "information_schema.TABLES",
            where=where,
            order="`TABLE_NAME`",
            database_name=self._database_name
        )

        # Check.
        assert result.rowcount != 0, "database '%s' not exist" % self._database_name

        # Convert.
        info_table = result.fetch_table()

        return info_table


class RInfoTable(RInfo):
    """
    Rey's `database table information` type.

    Examples
    --------
    Get columns information of table.
    >>> columns_info = RInfoTable()

    Get table attribute.
    >>> database_attr = RInfoTable["attribute"]

    Get column attribute.
    >>> database_attr = RInfoTable.column["attribute"]
    """


    def __init__(
        self,
        rengine: Union[REngine, RConnection],
        database_name: str,
        table_name: str
    ) -> None:
        """
        Build `database table information` instance.

        Parameters
        ----------
        rengine : REngine object or RConnection object.
        database_name : Database name.
        table_name : Table name.
        """

        # Set parameter.
        self._rengine = rengine
        self._database_name = database_name
        self._table_name = table_name


    def _get_info_attrs(self) -> Dict:
        """
        Get information attribute dictionary.

        Returns
        -------
        Information attribute dictionary.
        """

        # Select.
        where = "`TABLE_SCHEMA` = :database_name AND `TABLE_NAME` = :table_name"
        result = self._rengine.execute_select(
            "information_schema.TABLES",
            where=where,
            limit=1,
            database_name=self._database_name,
            table_name=self._table_name
        )

        # Check.
        assert result.rowcount != 0, "database '%s' or table '%s' not exist" % (self._database_name, self._table_name)

        # Convert.
        info_table = result.fetch_table()
        info_attrs = info_table[0]

        return info_attrs


    def _get_info_table(self) -> List[Dict]:
        """
        Get information table.

        Returns
        -------
        Information table.
        """

        # Select.
        where = "`TABLE_SCHEMA` = :database_name AND `TABLE_NAME` = :table_name"
        result = self._rengine.execute_select(
            "information_schema.COLUMNS",
            where=where,
            order="`TABLE_NAME`",
            database_name=self._database_name,
            table_name=self._table_name
        )

        # Check.
        assert result.rowcount != 0, "database '%s' not exist" % self._database_name

        # Convert.
        info_table = result.fetch_table()

        return info_table


class RInfoColumn(RInfo):
    """
    Rey's `database column information` type.

    Examples
    --------
    Get column attribute.
    >>> database_attr = RInfoColumn["attribute"]
    """


    def __init__(
        self,
        rengine: Union[REngine, RConnection],
        database_name: str,
        table_name: str,
        column_name: str
    ) -> None:
        """
        Build `database column information` instance.

        Parameters
        ----------
        rengine : REngine object or RConnection object.
        database_name : Database name.
        table_name : Table name.
        column_name : Column name.
        """

        # Set parameter.
        self._rengine = rengine
        self._database_name = database_name
        self._table_name = table_name
        self._column_name = column_name


    def _get_info_attrs(self) -> Dict:
        """
        Get information attribute dictionary.

        Returns
        -------
        Information attribute dictionary.
        """

        # Select.
        where = "`TABLE_SCHEMA` = :database_name AND `TABLE_NAME` = :table_name AND `COLUMN_NAME` = :column_name"
        result = self._rengine.execute_select(
            "information_schema.COLUMNS",
            where=where,
            limit=1,
            database_name=self._database_name,
            table_name=self._table_name,
            column_name=self._column_name
        )

        # Check.
        assert result.rowcount != 0, "database '%s' or table '%s' or column '%s' not exist" % (self._database_name, self._table_name, self._column_name)

        # Convert.
        info_table = result.fetch_table()
        info_attrs = info_table[0]

        return info_attrs