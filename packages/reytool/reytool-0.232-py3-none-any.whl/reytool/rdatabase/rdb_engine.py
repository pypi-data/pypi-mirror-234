# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:02
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database engine and connection methods.
"""


from __future__ import annotations
from typing import Any, List, Dict, Tuple, Union, Optional, Literal, Iterable, ClassVar, NoReturn, overload
from re import findall
from sqlalchemy import create_engine as sqlalchemy_create_engine, text
from sqlalchemy.engine.base import Engine, Connection
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.exc import OperationalError
from pandas import DataFrame

from ..rdata import objs_in
from ..rmonkey import sqlalchemy_add_result_more_fetch, sqlalchemy_support_row_index_by_field
from ..rprint import rprint
from ..rregular import search
from ..rsystem import rexc, get_first_notnull
from ..rtable import Table, to_table
from ..rtext import join_data_text
from ..rwrap import runtime, retry


# Add more fetch methods to CursorResult object.
RResult = sqlalchemy_add_result_more_fetch()

# Support Row object of package sqlalchemy index by field name.
sqlalchemy_support_row_index_by_field()


class REngine(object):
    """
    Rey's `database engine` type.
    """


    # Values to be converted to "NULL".
    nulls: ClassVar[Tuple] = ("", " ", b"", [], (), {}, set())

    # Default value.
    default_report: bool = False


    @overload
    def __init__(
        self,
        host: None = None,
        port: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: None = None,
        engine: None = None,
        **query: str
    ) -> NoReturn: ...

    @overload
    def __init__(
        self,
        host: Optional[str] = None,
        port: None = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: None = None,
        engine: None = None,
        **query: str
    ) -> NoReturn: ...

    @overload
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        username: None = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: None = None,
        engine: None = None,
        **query: str
    ) -> NoReturn: ...

    @overload
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        username: Optional[str] = None,
        password: None = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: None = None,
        engine: None = None,
        **query: str
    ) -> NoReturn: ...

    @overload
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: Optional[Union[str, URL]] = None,
        engine: Optional[Union[Engine, Connection]] = None,
        **query: str
    ) -> None: ...

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_recycle: Optional[int] = None,
        url: Optional[Union[str, URL]] = None,
        engine: Optional[Union[Engine, Connection]] = None,
        **query: str
    ) -> None:
        """
        Build `database engine` instance.

        Parameters
        ----------
        host : Server host.
        port : Server port.
        username : Server user name.
        password : Server password.
        database : Database name in the server.
        drivername : Database backend and driver name.
            - `None` : Automatic select and try.
            - `str` : Use this value.

        pool_size : Number of connections `keep open`.
        max_overflow : Number of connections `allowed overflow`.
        pool_timeout : Number of seconds `wait create` connection.
        pool_recycle : Number of seconds `recycle` connection.
            - `None` : Use database variable `wait_timeout` value.
            - `Literal[-1]` : No recycle.
            - `int` : Use this value.

        url: Get parameter from server `URL`, but preferred input parameters.
            Parameters include `username`, `password`, `host`, `port`, `database`, `drivername`, `query`.
        engine : Use existing `Engine` or `Connection` object, and get parameter from it.
            Parameters include `username`, `password`, `host`, `port`, `database`, `drivername`, `query`,
            `pool_size`, `max_overflow`, `pool_timeout`, `pool_recycle`.
        query : Server parameters.
        """

        # From existing Engine or Connection object.
        if engine is not None:

            ## Extract Engine object from Connection boject.
            if engine.__class__ == Connection:
                engine = engine.engine

            ## Extract parameter.
            params = self.extract_from_engine(engine)

            ## Set.
            self.drivername = params["drivername"]
            self.username = params["username"]
            self.password = params["password"]
            self.host = params["host"]
            self.port = params["port"]
            self.database = params["database"]
            self.query = params["query"]
            self.pool_size = params["pool_size"]
            self.max_overflow = params["max_overflow"]
            self.pool_timeout = params["pool_timeout"]
            self.pool_recycle = params["pool_recycle"]
            self.engine = engine

        # From parameters create.
        else:

            ## Extract parameters from URL.
            if url is not None:
                params = self.extract_from_url(url)
            else:
                params = dict.fromkeys(
                    (
                        "drivername",
                        "username",
                        "password",
                        "host",
                        "port",
                        "database",
                        "query"
                    )
                )

            ## Set parameters by priority.
            self.drivername = get_first_notnull(drivername, params["drivername"])
            self.username = get_first_notnull(username, params["username"], default="exception")
            self.password = get_first_notnull(password, params["password"], default="exception")
            self.host = get_first_notnull(host, params["host"], default="exception")
            self.port = get_first_notnull(port, params["port"], default="exception")
            self.database = get_first_notnull(database, params["database"])
            self.query = get_first_notnull(query, params["query"], default={"charset": "utf8"}, nulls=(None, {}))
            self.pool_size = pool_size
            self.max_overflow = max_overflow
            self.pool_timeout = pool_timeout

            ## Create Engine object.
            if pool_recycle is None:
                self.pool_recycle = -1
                self.engine = self.create_engine()
                wait_timeout = int(self.variables["wait_timeout"])
                self.pool_recycle = wait_timeout
                self.engine.pool._recycle = wait_timeout
            else:
                self.pool_recycle = pool_recycle
                self.engine = self.create_engine()


    def extract_from_url(self, url: Union[str, URL]) -> Dict[
        Literal["drivername", "username", "password", "host", "port", "database", "query"],
        Any
    ]:
        """
        Extract parameters from `URL` of string.

        Parameters
        ----------
        url : URL of string.

        Returns
        -------
        Extracted parameters.
        """

        # Extract.

        ## When str object.
        if url.__class__ == str:
            pattern = "^([\w\+]+)://(\w+):(\w+)@(\d+\.\d+\.\d+\.\d+):(\d+)[/]?([\w/]+)?[\?]?([\w&=]+)?$"
            result = search(pattern, url)
            if result is None:
                rexc(ValueError, url)
            (
                drivername,
                username,
                password,
                host,
                port,
                database,
                query_str
            ) = result
            if query_str is not None:
                pattern = "(\w+)=(\w+)"
                query_findall = findall(pattern, query_str)
                query = {key: value for key, value in query_findall}
            else:
                query = {}

        ## When URL object.
        elif url.__class__ == URL:
            drivername = url.drivername
            username = url.username
            password = url.password
            host = url.host
            port = url.port
            database = url.database
            query = dict(url.query)

        # Generate parameter.
        params = {
            "drivername": drivername,
            "username": username,
            "password": password,
            "host": host,
            "port": port,
            "database": database,
            "query": query
        }

        return params


    def extract_from_engine(self, engine: Union[Engine, Connection]) -> Dict[
        Literal[
            "drivername", "username", "password", "host", "port", "database", "query",
            "pool_size", "max_overflow", "pool_timeout", "pool_recycle"
        ],
        Any
    ]:
        """
        Extract parameters from `Engine` or `Connection` object.

        Parameters
        ----------
        engine : Engine or Connection object.

        Returns
        -------
        Extracted parameters.
        """

        ## Extract Engine object from Connection boject.
        if engine.__class__ == Connection:
            engine = engine.engine

        ## Extract.
        drivername = engine.url.drivername
        username = engine.url.username
        password = engine.url.password
        host = engine.url.host
        port = engine.url.port
        database = engine.url.database
        query = dict(engine.url.query)
        pool_size = engine.pool._pool.maxsize
        max_overflow = engine.pool._max_overflow
        pool_timeout = engine.pool._timeout
        pool_recycle = engine.pool._recycle

        # Generate parameter.
        params = {
            "drivername": drivername,
            "username": username,
            "password": password,
            "host": host,
            "port": port,
            "database": database,
            "query": query,
            "pool_size": pool_size,
            "max_overflow": max_overflow,
            "pool_timeout": pool_timeout,
            "pool_recycle": pool_recycle
        }

        return params


    @property
    def url(self) -> str:
        """
        Generate server `URL`.

        Returns
        -------
        Server URL.
        """

        # Generate URL.
        _url = f"{self.drivername}://{self.username}:{self.password}@{self.host}:{self.port}"

        # Add database path.
        if self.database is not None:
            _url = f"{_url}/{self.database}"

        # Add Server parameter.
        if self.query != {}:
            query = "&".join(
                [
                    f"{key}={value}"
                    for key, value in self.query.items()
                ]
            )
            _url = f"{_url}?{query}"

        return _url


    def create_engine(self, **kwargs) -> Engine:
        """
        Create database `Engine` object.

        Parameters
        ----------
        kwargs : Keyword parameters of create engine method.

        Returns
        -------
        Engine object.
        """

        # Handle parameter.
        if self.drivername is None:
            drivernames = ("mysql+mysqldb", "mysql+pymysql")
        else:
            drivernames = (self.drivername,)

        # Create Engine object.
        for drivername in drivernames:

            ## Set engine parameter.
            self.drivername = drivername
            engine_params = {
                "url": self.url,
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "pool_timeout": self.pool_timeout,
                "pool_recycle": self.pool_recycle,
                **kwargs
            }

            ## Try create.
            try:
                engine = sqlalchemy_create_engine(**engine_params)
            except ModuleNotFoundError:
                pass
            else:
                return engine

        # Throw exception.
        drivernames_str = " and ".join(
            [
                dirvername.split("+", 1)[-1]
                for dirvername in drivernames
            ]
        )
        raise ModuleNotFoundError(f"module {drivernames_str} not fund")


    @property
    def count(self) -> Tuple[int, int]:
        """
        Count number of `keep open` and `allowed overflow` connection.

        Returns
        -------
        Number of keep open and allowed overflow connection.
        """

        # Get parameter.
        if "engine" in self.__dict__:
            rengine = self
        else:
            rengine: REngine = self.rengine

        # Count.
        _overflow = rengine.engine.pool._overflow
        if _overflow < 0:
            keep_n = rengine.pool_size + _overflow
            overflow_n = 0
        else:
            keep_n = rengine.pool_size
            overflow_n = _overflow

        return keep_n, overflow_n


    def fill_data(
        self,
        data: Table,
        sql: Union[str, TextClause],
    ) -> List[Dict]:
        """
        `Fill` missing data according to contents of `TextClause` object of package `sqlalchemy`, and filter out empty Dict.

        Parameters
        ----------
        data : Data set for filling.
        sql : SQL in method sqlalchemy.text format, or TextClause object.

        Returns
        -------
        Filled data.
        """

        # Handle parameter.
        if data.__class__ == dict:
            data = [data]
        elif data.__class__ != list:
            data = to_table(data)
        if sql.__class__ == TextClause:
            sql = sql.text

        # Extract fill field names.
        pattern = "(?<!\\\):(\w+)"
        sql_keys = findall(pattern, sql)

        # Fill data.
        for row in data:

            # Filter empty Dict.
            if row == {}:
                continue

            # Fill.
            for key in sql_keys:
                value = row.get(key)
                if (
                    value is None
                    or value in self.nulls
                ):
                    row[key] = None

        return data


    def get_syntax(self, sql: Union[str, TextClause]) -> List[str]:
        """
        Extract `SQL syntax` type for each segment form SQL.

        Parameters
        ----------
        sql : SQL text or TextClause object.

        Returns
        -------
        SQL syntax type for each segment.
        """

        # Handle parameter.
        if sql.__class__ == TextClause:
            sql = sql.text

        # Extract.
        syntax = [
            search("[a-zA-Z]+", sql_part).upper()
            for sql_part in sql.split(";")
        ]

        return syntax


    def is_multi_sql(self, sql: Union[str, TextClause]) -> bool:
        """
        Judge whether it is `multi segment SQL`.

        Parameters
        ----------
        sql : SQL text or TextClause object.

        Returns
        -------
        Judgment result.
        """

        # Handle parameter.
        if sql.__class__ == TextClause:
            sql = sql.text

        # Judge.
        if ";" in sql.rstrip()[:-1]:
            return True
        return False


    def executor(
        self,
        connection: Connection,
        sql: TextClause,
        data: List[Dict],
        report: bool
    ) -> RResult:
        """
        `SQL` executor.

        Parameters
        ----------
        connection : Connection object.
        sql : TextClause object.
        data : Data set for filling.
        report : Whether report SQL execute information.

        Returns
        -------
        Result object.
        """

        # Create Transaction object.
        with connection.begin():

            # Execute.

            ## Report.
            if report:
                result, report_runtime = runtime(connection.execute, sql, data, _return_report=True)
                report_info = (
                    f"{report_runtime}\n"
                    f"Row Count: {result.rowcount}"
                )
                sqls = [
                    sql_part.strip()
                    for sql_part in sql.text.split(";")
                ]
                if data == []:
                    rprint(report_info, *sqls, title="SQL")
                else:
                    rprint(report_info, *sqls, data, title="SQL")

            ## Not report.
            else:
                result = connection.execute(sql, data)

        return result


    def execute(
        self,
        sql: Union[str, TextClause],
        data: Optional[Table] = None,
        report: Optional[bool] = None,
        **kwdata: Any
    ) -> RResult:
        """
        `Execute` SQL.

        Parameters
        ----------
        sql : SQL in method `sqlalchemy.text` format, or `TextClause` object.
        data : Data set for filling.
        report : Whether report SQL execute information.
            - `None` : Use attribute `default_report`.
            - `bool` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.
        """

        # Get parameter by priority.
        report = get_first_notnull(report, self.default_report, default="exception")

        # Handle parameter.
        if sql.__class__ == str:
            sql = text(sql)
        if data is None:
            if kwdata == {}:
                data = []
            else:
                data = [kwdata]
        else:
            if data.__class__ == dict:
                data = [data]
            elif isinstance(data, CursorResult):
                data = to_table(data)
            elif data.__class__ == DataFrame:
                data = to_table(data)
            else:
                data = data.copy()
            for param in data:
                param.update(kwdata)

        # Fill missing data.
        data = self.fill_data(data, sql)

        # Execute.

        ## Create Connection object.
        with self.engine.connect() as connection:

            ## Can retry.
            if not self.is_multi_sql(sql):
                result = retry(
                    self.executor,
                    connection,
                    sql,
                    data,
                    report,
                    _report="Database execute operational error",
                    _exception=OperationalError
                )

            ## Cannot retry.
            else:
                result = self.executor(connection, sql, data, report)

        return result


    def execute_select(
        self,
        path: Union[str, Tuple[str, str]],
        fields: Optional[Union[str, Iterable[str]]] = None,
        where: Optional[str] = None,
        group: Optional[str] = None,
        having: Optional[str] = None,
        order: Optional[str] = None,
        limit: Optional[Union[int, str, Tuple[int, int]]] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        Execute `select` SQL.

        Parameters
        ----------
        path : Table name, can contain database name.
            - `str` : Automatic split database name and table name.
                * `Not contain '.'`: Table name.
                * `Contain '.'` : Database name and table name. Example 'database_name.table_name'.
                * ```Contain '`'``` : Table name. Example '\`table_name_prefix.table_name\`'.
            - `Tuple[str, str]` : Database name and table name.

        fields : Select clause content.
            - `None` : Is `SELECT *`.
            - `str` : Join as `SELECT str`.
            - `Iterable[str]` : Join as `SELECT \`str\`, ...`.
                * `str and first character is ':'` : Use this syntax.
                * `str` : Use this field.

        where : Clause `WHERE` content, join as `WHERE str`.
        group : Clause `GROUP BY` content, join as `GROUP BY str`.
        having : Clause `HAVING` content, join as `HAVING str`.
        order : Clause `ORDER BY` content, join as `ORDER BY str`.
        limit : Clause `LIMIT` content.
            - `Union[int, str]` : Join as `LIMIT int/str`.
            - `Tuple[int, int]` : Join as `LIMIT int, int`.

        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.

        Examples
        --------
        Parameter `fields`.
        >>> fields = ['id', ':`id` + 1 AS `id_`']
        >>> result = REngine.execute_select('database.table', fields)
        >>> print(result.fetch_table())
        [{'id': 1, 'id_': 2}, ...]

        Parameter `kwdata`.
        >>> fields = '`id`, `id` + :value AS `id_`'
        >>> result = REngine.execute_select('database.table', fields, value=1)
        >>> print(result.fetch_table())
        [{'id': 1, 'id_': 2}, ...]
        """

        # Handle parameter.
        if path.__class__ == str:
            database = None
            if "`" in path:
                table = path.replace("`", "")
            elif "." in path:
                database, table = path.split(".", 1)
            else:
                table = path
        else:
            database, table = path

        # Get parameter by priority.
        database = get_first_notnull(database, self.database, default="exception")

        # Generate SQL.
        sql_list = []

        ## Part "SELECT" syntax.
        if fields is None:
            fields = "*"
        elif fields.__class__ != str:
            fields = ", ".join(
                [
                    field[1:]
                    if (
                        field[:1] == ":"
                        and field != ":"
                    )
                    else f"`{field}`"
                    for field in fields
                ]
            )
        sql_select = f"SELECT {fields}"
        sql_list.append(sql_select)

        ## Part "FROM" syntax.
        sql_from = f"FROM `{database}`.`{table}`"
        sql_list.append(sql_from)

        ## Part "WHERE" syntax.
        if where is not None:
            sql_where = f"WHERE {where}"
            sql_list.append(sql_where)

        ## Part "GROUP BY" syntax.
        if group is not None:
            sql_group = f"GROUP BY {group}"
            sql_list.append(sql_group)

        ## Part "GROUP BY" syntax.
        if having is not None:
            sql_having = f"HAVING {having}"
            sql_list.append(sql_having)

        ## Part "ORDER BY" syntax.
        if order is not None:
            sql_order = f"ORDER BY {order}"
            sql_list.append(sql_order)

        ## Part "LIMIT" syntax.
        if limit is not None:
            if limit.__class__ in (str, int):
                sql_limit = f"LIMIT {limit}"
            else:
                if len(limit) == 2:
                    sql_limit = f"LIMIT {limit[0]}, {limit[1]}"
                else:
                    rexc(ValueError, limit)
            sql_list.append(sql_limit)

        ## Join sql part.
        sql = "\n".join(sql_list)

        # Execute SQL.
        result = self.execute(sql, report=report, **kwdata)

        return result


    def execute_insert(
        self,
        path: Union[str, Tuple[str, str]],
        data: Table,
        duplicate: Optional[Literal["ignore", "update"]] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        `Insert` the data of table in the datebase.

        Parameters
        ----------
        path : Table name, can contain database name.
            - `str` : Automatic split database name and table name.
                * `Not contain '.'`: Table name.
                * `Contain '.'` : Database name and table name. Example 'database_name.table_name'.
                * ```Contain '`'``` : Table name. Example '\`table_name_prefix.table_name\`'.
            - `Tuple[str, str]` : Database name and table name.

        data : Insert data.
        duplicate : Handle method when constraint error.
            - `None` : Not handled.
            - `ignore` : Use `UPDATE IGNORE INTO` clause.
            - `update` : Use `ON DUPLICATE KEY UPDATE` clause.

        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.
            - `str and first character is ':'` : Use this syntax.
            - `Any` : Use this value.

        Returns
        -------
        Result object.

        Examples
        --------
        Parameter `data` and `kwdata`.
        >>> data = [{'key': 'a'}, {'key': 'b'}]
        >>> kwdata = {'value1': 1, 'value2': ':(SELECT 2)'}
        >>> result = REngine.execute_insert('database.table', data, **kwdata)
        >>> print(result.rowcount)
        2
        >>> result = REngine.execute_select('database.table')
        >>> print(result.fetch_table())
        [{'key': 'a', 'value1': 1, 'value2': 2}, {'key': 'b', 'value1': 1, 'value2': 2}]
        """

        # Handle parameter.
        if path.__class__ == str:
            database = None
            if "`" in path:
                table = path.replace("`", "")
            elif "." in path:
                database, table = path.split(".", 1)
            else:
                table = path
        else:
            database, table = path

        # Get parameter by priority.
        database = get_first_notnull(database, self.database, default="exception")

        # Handle parameter.

        ## Data.
        if data.__class__ == dict:
            data = [data]
        elif isinstance(data, CursorResult):
            data = to_table(data)
        elif data.__class__ == DataFrame:
            data = to_table(data)

        ## Check.
        if data in ([], [{}]):
            rexc(ValueError, data)

        ## Keyword data.
        kwdata_method = {}
        kwdata_replace = {}
        for key, value in kwdata.items():
            if (
                value.__class__ == str
                and value[:1] == ":"
                and value != ":"
            ):
                kwdata_method[key] = value[1:]
            else:
                kwdata_replace[key] = value

        # Generate SQL.

        ## Part "fields" syntax.
        fields_replace = {
            field
            for row in data
            for field in row
        }
        fields_replace = {
            field
            for field in fields_replace
            if field not in kwdata
        }
        sql_fields_list = (
            *kwdata_method,
            *kwdata_replace,
            *fields_replace
        )
        sql_fields = ", ".join(
            [
                f"`{field}`"
                for field in sql_fields_list
            ]
        )

        ## Part "values" syntax.
        sql_values_list = (
            *kwdata_method.values(),
            *[
                ":" + field
                for field in (
                    *kwdata_replace,
                    *fields_replace
                )
            ]
        )
        sql_values = ", ".join(sql_values_list)

        ## Join sql part.

        ### Ignore.
        if duplicate == "ignore":
            sql = (
                f"INSERT IGNORE INTO `{database}`.`{table}`({sql_fields})\n"
                f"VALUES({sql_values})"
            )

        ### Update.
        elif duplicate == "update":
            update_content = ",\n    ".join([f"`{field}` = VALUES(`{field}`)" for field in sql_fields_list])
            sql = (
                f"INSERT INTO `{database}`.`{table}`({sql_fields})\n"
                f"VALUES({sql_values})\n"
                "ON DUPLICATE KEY UPDATE\n"
                f"    {update_content}"
            )

        ### Not handle.
        else:
            sql = (
                f"INSERT INTO `{database}`.`{table}`({sql_fields})\n"
                f"VALUES({sql_values})"
            )

        # Execute SQL.
        result = self.execute(sql, data, report, **kwdata_replace)

        return result


    def execute_update(
        self,
        path: Union[str, Tuple[str, str]],
        data: Table,
        where_fields: Optional[Union[str, Iterable[str]]] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        `Update` the data of table in the datebase.

        Parameters
        ----------
        path : Table name, can contain database name.
            - `str` : Automatic split database name and table name.
                * `Not contain '.'`: Table name.
                * `Contain '.'` : Database name and table name. Example 'database_name.table_name'.
                * ```Contain '`'``` : Table name. Example '\`table_name_prefix.table_name\`'.
            - `Tuple[str, str]` : Database name and table name.

        data : Update data, clause `WHERE` and `SET` content.
            - `Key` : Table field.
            - `Value` : Table value.
                * `Union[List, Tuple]` : Clause WHERE form is 'field IN :field'.
                * `Any` : Clause WHERE form is 'field = :field'.

        where_fields : Clause `WHERE` content fields.
            - `None` : The first key value pair of each item is judged.
            - `str` : This key value pair of each item is judged.
            - `Iterable[str]` : Multiple judged, `and` relationship.

        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.
            - `str and first character is ':'` : Use this syntax.
            - `Any` : Use this value.

        Returns
        -------
        Result object.

        Examples
        --------
        Parameter `data` and `kwdata`.
        >>> data = [{'key': 'a'}, {'key': 'b'}]
        >>> kwdata = {'value': 1, 'name': ':`key`'}
        >>> result = REngine.execute_update('database.table', data, **kwdata)
        >>> print(result.rowcount)
        2
        >>> result = REngine.execute_select('database.table')
        >>> print(result.fetch_table())
        [{'key': 'a', 'value': 1, 'name': 'a'}, {'key': 'b', 'value': 1, 'name': 'b'}]
        """

        # Handle parameter.
        if path.__class__ == str:
            database = None
            if "`" in path:
                table = path.replace("`", "")
            elif "." in path:
                database, table = path.split(".", 1)
            else:
                table = path
        else:
            database, table = path

        # Get parameter by priority.
        database = get_first_notnull(database, self.database, default="exception")

        # Handle parameter.

        ## Data.
        if data.__class__ == dict:
            data = [data]
        elif isinstance(data, CursorResult):
            data = to_table(data)
        elif data.__class__ == DataFrame:
            data = to_table(data)

        ## Check.
        if data in ([], [{}]):
            rexc(ValueError, data)

        ## Keyword data.
        kwdata_method = {}
        kwdata_replace = {}
        for key, value in kwdata.items():
            if (
                value.__class__ == str
                and value[:1] == ":"
                and value != ":"
            ):
                kwdata_method[key] = value[1:]
            else:
                kwdata_replace[key] = value
        sql_set_list_kwdata = [
            f"`{key}` = {value}"
            for key, value in kwdata_method.items()
        ]
        sql_set_list_kwdata.extend(
            [
                f"`{key}` = :{key}"
                for key in kwdata_replace
            ]
        )

        # Generate SQL.
        data_flatten = kwdata_replace
        sqls_list = []
        if where_fields is None:
            no_where = True
        else:
            no_where = False
            if where_fields.__class__ == str:
                where_fields = [where_fields]
        for index, row in enumerate(data):
            for key, value in row.items():
                index_key = f"{index}_{key}"
                data_flatten[index_key] = value
            if no_where:
                for key in row:
                    where_fields = [key]
                    break

            ## Part "SET" syntax.
            sql_set_list = sql_set_list_kwdata.copy()
            sql_set_list.extend(
                [
                    f"`{key}` = :{index}_{key}"
                    for key in row
                    if (
                        key not in where_fields
                        and key not in kwdata
                    )
                ]
            )
            sql_set = ",\n    ".join(sql_set_list)

            ## Part "WHERE" syntax.
            sql_where_list = []
            for field in where_fields:
                index_field = f"{index}_{field}"
                index_value = data_flatten[index_field]
                if index_value.__class__ in (list, tuple):
                    sql_where_part = f"`{field}` IN :{index_field}"
                else:
                    sql_where_part = f"`{field}` = :{index_field}"
                sql_where_list.append(sql_where_part)
            sql_where = "\n    AND ".join(sql_where_list)

            ## Join sql part.
            sql = (
                f"UPDATE `{database}`.`{table}`\n"
                f"SET {sql_set}\n"
                f"WHERE {sql_where}"
            )
            sqls_list.append(sql)

        ## Join sqls.
        sqls = ";\n".join(sqls_list)

        # Execute SQL.
        result = self.execute(sqls, data_flatten, report)

        return result


    def execute_delete(
        self,
        path: Union[str, Tuple[str, str]],
        where: Optional[str] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        `Delete` the data of table in the datebase.

        Parameters
        ----------
        path : Table name, can contain database name.
            - `str` : Automatic split database name and table name.
                * `Not contain '.'`: Table name.
                * `Contain '.'` : Database name and table name. Example 'database_name.table_name'.
                * ```Contain '`'``` : Table name. Example '\`table_name_prefix.table_name\`'.
            - `Tuple[str, str]` : Database name and table name.

        where : Clause `WHERE` content, join as `WHERE str`.
        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.

        Examples
        --------
        Parameter `where` and `kwdata`.
        >>> where = '`id` IN :ids'
        >>> ids = (1, 2)
        >>> result = REngine.execute_delete('database.table', where, ids=ids)
        >>> print(result.rowcount)
        2
        """

        # Handle parameter.
        if path.__class__ == str:
            database = None
            if "`" in path:
                table = path.replace("`", "")
            elif "." in path:
                database, table = path.split(".", 1)
            else:
                table = path
        else:
            database, table = path

        # Get parameter by priority.
        database = get_first_notnull(database, self.database, default="exception")

        # Generate SQL.
        sqls = []

        ## Part 'DELETE' syntax.
        sql_delete = f"DELETE FROM `{database}`.`{table}`"
        sqls.append(sql_delete)

        ## Part 'WHERE' syntax.
        if where is not None:
            sql_where = f"WHERE {where}"
            sqls.append(sql_where)

        ## Join sqls.
        sqls = "\n".join(sqls)

        # Execute SQL.
        result = self.execute(sqls, report=report, **kwdata)

        return result


    def execute_copy(
        self,
        path: Union[str, Tuple[str, str]],
        where: Optional[str] = None,
        limit: Optional[Union[int, str, Tuple[int, int]]] = None,
        report: bool = None,
        **kwdata: Any
    ) -> RResult:
        """
        `Copy` record of table in the datebase.

        Parameters
        ----------
        path : Table name, can contain database name.
            - `str` : Automatic split database name and table name.
                * `Not contain '.'`: Table name.
                * `Contain '.'` : Database name and table name. Example 'database_name.table_name'.
                * ```Contain '`'``` : Table name. Example '\`table_name_prefix.table_name\`'.
            - `Tuple[str, str]` : Database name and table name.

        where : Clause `WHERE` content, join as `WHERE str`.
        limit : Clause `LIMIT` content.
            - `Union[int, str]` : Join as `LIMIT int/str`.
            - `Tuple[int, int]` : Join as `LIMIT int, int`.

        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.
            - `In 'WHERE' syntax` : Fill 'WHERE' syntax.
            - `Not in 'WHERE' syntax` : Fill 'INSERT' and 'SELECT' syntax.

        Returns
        -------
        Result object.

        Examples
        --------
        Parameter `where` and `kwdata`.
        >>> where = '`id` IN :ids'
        >>> ids = (1, 2, 3)
        >>> result = REngine.execute_copy('database.table', where, 2, ids=ids)
        >>> print(result.rowcount)
        2
        """

        # Handle parameter.
        if path.__class__ == str:
            database = None
            if "`" in path:
                table = path.replace("`", "")
            elif "." in path:
                database, table = path.split(".", 1)
            else:
                table = path
        else:
            database, table = path

        # Get parameter by priority.
        database = get_first_notnull(database, self.database, default="exception")

        # Get parameter.
        table_info: List[Dict] = self.info(database)(table)()
        fields = [
            row["COLUMN_NAME"]
            for row in table_info
        ]
        pattern = "(?<!\\\):(\w+)"
        if where.__class__ == str:
            where_keys = findall(pattern, where)
        else:
            where_keys = ()

        # Generate SQL.
        sqls = []

        ## Part "INSERT" syntax.
        sql_fields = ", ".join(
            f"`{field}`"
            for field in fields
            if field not in kwdata
        )
        if kwdata != {}:
            sql_fields_kwdata = ", ".join(
                f"`{field}`"
                for field in kwdata
                if field not in where_keys
            )
            sql_fields = f"{sql_fields}, {sql_fields_kwdata}"
        sql_insert = f"INSERT INTO `{database}`.`{table}`({sql_fields})"
        sqls.append(sql_insert)

        ## Part "SELECT" syntax.
        sql_values = ", ".join(
            f"`{field}`"
            for field in fields
            if field not in kwdata
        )
        if kwdata != {}:
            sql_values_kwdata = ", ".join(
                f":{field}"
                for field in kwdata
                if field not in where_keys
            )
            sql_values = f"{sql_values}, {sql_values_kwdata}"
        sql_select = (
            f"SELECT {sql_values}\n"
            f"FROM `{database}`.`{table}`"
        )
        sqls.append(sql_select)

        ## Part "WHERE" syntax.
        if where is not None:
            sql_where = f"WHERE {where}"
            sqls.append(sql_where)

        ## Part "LIMIT" syntax.
        if limit is not None:
            if limit.__class__ in (str, int):
                sql_limit = f"LIMIT {limit}"
            else:
                if len(limit) == 2:
                    sql_limit = f"LIMIT {limit[0]}, {limit[1]}"
                else:
                    rexc(ValueError, limit)
            sqls.append(sql_limit)

        ## Join.
        sql = "\n".join(sqls)

        # Execute SQL.
        result = self.execute(sql, report=report, **kwdata)

        return result


    def execute_exist(
        self,
        path: Union[str, Tuple[str, str]],
        where: Optional[str] = None,
        report: bool = None,
        **kwdata: Any
    ) -> bool:
        """
        Judge the `exist` of record.

        Parameters
        ----------
        path : Table name, can contain database name.
            - `str` : Automatic split database name and table name.
                * `Not contain '.'`: Table name.
                * `Contain '.'` : Database name and table name. Example 'database_name.table_name'.
                * ```Contain '`'``` : Table name. Example '\`table_name_prefix.table_name\`'.
            - `Tuple[str, str]` : Database name and table name.

        where : Match condition, `WHERE` clause content, join as `WHERE str`.
            - `None` : Match all.
            - `str` : Match condition.

        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Judged result.

        Examples
        --------
        Parameter `where` and `kwdata`.
        >>> data = [{'id': 1}]
        >>> REngine.execute_insert('database.table', data)
        >>> where = '`id` = :id_'
        >>> id_ = 1
        >>> result = REngine.execute_exist('database.table', where, id_=id_)
        >>> print(result)
        True
        """

        # Handle parameter.
        if path.__class__ == str:
            database = None
            if "`" in path:
                table = path.replace("`", "")
            elif "." in path:
                database, table = path.split(".", 1)
            else:
                table = path
        else:
            database, table = path

        # Execute.
        result = self.execute_select((database, table), "1", where=where, limit=1, report=report, **kwdata)

        # Judge.
        judge = result.rowcount != 0

        return judge


    def execute_count(
        self,
        path: Union[str, Tuple[str, str]],
        where: Optional[str] = None,
        report: bool = None,
        **kwdata: Any
    ) -> int:
        """
        `Count` records.

        Parameters
        ----------
        path : Table name, can contain database name.
            - `str` : Automatic split database name and table name.
                * `Not contain '.'`: Table name.
                * `Contain '.'` : Database name and table name. Example 'database_name.table_name'.
                * ```Contain '`'``` : Table name. Example '\`table_name_prefix.table_name\`'.
            - `Tuple[str, str]` : Database name and table name.

        where : Match condition, `WHERE` clause content, join as `WHERE str`.
            - `None` : Match all.
            - `str` : Match condition.

        report : Whether report SQL execute information.
            - `None` : Use attribute `report_execute_info` of object `ROption`.
            - `int` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Record count.

        Examples
        --------
        Parameter `where` and `kwdata`.
        >>> where = '`id` IN :ids'
        >>> ids = (1, 2)
        >>> result = REngine.execute_count('database.table', where, ids=ids)
        >>> print(result)
        2
        """

        # Handle parameter.
        if path.__class__ == str:
            database = None
            if "`" in path:
                table = path.replace("`", "")
            elif "." in path:
                database, table = path.split(".", 1)
            else:
                table = path
        else:
            database, table = path

        # Execute.
        result = self.execute_select((database, table), "1", where=where, report=report, **kwdata)
        count = result.rowcount

        return count


    def connect(self) -> RConnection:
        """
        Build `database connection` instance.
        """

        # Build.
        rconnection = RConnection(
            self.engine.connect(),
            self
        )

        return rconnection


    @property
    def schema(self) -> Dict[str, Dict[str, List]]:
        """
        Get schemata of `databases` and `tables` and `columns`.

        Returns
        -------
        Schemata of databases and tables and columns.
        """

        # Select.
        result = self.execute_select(
            "information_schema.COLUMNS",
            ["TABLE_SCHEMA", "TABLE_NAME", "COLUMN_NAME"]
        )

        # Convert.
        database_dict = {}
        for database, table, column in result:

            ## Index database.
            if database not in database_dict:
                database_dict[database] = {table: [column]}
                continue
            table_dict: Dict = database_dict[database]

            ## Index table. 
            if table not in table_dict:
                table_dict[table] = [column]
                continue
            column_list: List = table_dict[table]

            ## Add column.
            column_list.append(column)

        return database_dict


    @property
    def exe(self):
        """
        Build `database execute` instance.

        Returns
        -------
        Database execute instance.

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


        # Import.
        from .rdb_execute import RExecute


        # Build.
        rexecute = RExecute(self)

        return rexecute


    @property
    def info(self):
        """
        Build `database schema information` instance.

        Returns
        -------
        Database schema information instance.

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


        # Import.
        from .rdb_info import RInfoSchema


        # Build.
        rschema = RInfoSchema(self)

        return rschema


    @property
    def status(self):
        """
        Build `database status parameters` instance.

        Returns
        -------
        Database status parameters instance.
        """


        # Import.
        from .rdb_param import RParamStatus


        # Build.
        rstatus = RParamStatus(self, False)

        return rstatus


    @property
    def global_status(self):
        """
        Build global `database status parameters` instance.

        Returns
        -------
        Global database status parameters instance.
        """


        # Import.
        from .rdb_param import RParamStatus


        # Build.
        rstatus = RParamStatus(self, True)

        return rstatus


    @property
    def variables(self):
        """
        Build `database variable parameters` instance.

        Returns
        -------
        Database variable parameters instance.
        """


        # Import.
        from .rdb_param import RParamVariable


        # Build.
        rvariables = RParamVariable(self, False)

        return rvariables


    @property
    def global_variables(self):
        """
        Build global `database variable parameters` instance.

        Returns
        -------
        Global database variable parameters instance.
        """


        # Import.
        from .rdb_param import RParamVariable


        # Build.
        rvariables = RParamVariable(self, True)

        return rvariables


    __call__ = execute


    def __str__(self) -> str:
        """
        Return connection information text.
        """

        # Get parameter.
        if "engine" in self.__dict__:
            attr_dict = self.__dict__
        else:
            rengine: REngine = self.rengine
            attr_dict = {
                **self.__dict__,
                **rengine.__dict__
            }

        # Generate.
        filter_key = (
            "engine",
            "connection",
            "rengine",
            "begin"
        )
        info = {
            key: value
            for key, value in attr_dict.items()
            if key not in filter_key
        }
        info["count"] = self.count
        text = join_data_text(info)

        return text


class RConnection(REngine):
    """
    Rey's `database connection` type.
    """


    def __init__(
        self,
        connection: Connection,
        rengine: REngine
    ) -> None:
        """
        Build `database connection` instance.

        Parameters
        ----------
        connection : Connection object.
        rengine : REngine object.
        """

        # Set parameter.
        self.connection = connection
        self.rengine = rengine
        self.begin = None
        self.begin_count = 0
        self.drivername = rengine.drivername
        self.username = rengine.username
        self.password = rengine.password
        self.host = rengine.host
        self.port = rengine.port
        self.database = rengine.database
        self.query = rengine.query
        self.pool_recycle = rengine.pool_recycle


    def executor(
        self,
        connection: Connection,
        sql: TextClause,
        data: List[Dict],
        report: bool
    ) -> RResult:
        """
        `SQL` executor.

        Parameters
        ----------
        connection : Connection object.
        sql : TextClause object.
        data : Data set for filling.
        report : Whether report SQL execute information.

        Returns
        -------
        Result object.
        """

        # Create Transaction object.
        if self.begin_count == 0:
            self.rollback()
            self.begin = connection.begin()

        # Execute.

        ## Report.
        if report:
            result, report_runtime = runtime(connection.execute, sql, data, _return_report=True)
            report_info = (
                f"{report_runtime}\n"
                f"Row Count: {result.rowcount}"
            )
            sqls = [
                sql_part.strip()
                for sql_part in sql.text.split(";")
            ]
            if data == []:
                rprint(report_info, *sqls, title="SQL")
            else:
                rprint(report_info, *sqls, data, title="SQL")

        ## Not report.
        else:
            result = connection.execute(sql, data)

        # Count.
        syntaxes = self.get_syntax(sql)
        if objs_in(syntaxes, "INSERT", "UPDATE", "DELETE"):
            self.begin_count += 1

        return result


    def execute(
        self,
        sql: Union[str, TextClause],
        data: Optional[Table] = None,
        report: Optional[bool] = None,
        **kwdata: Any
    ) -> RResult:
        """
        Execute `SQL`.

        Parameters
        ----------
        sql : SQL in method `sqlalchemy.text` format, or `TextClause` object.
        data : Data set for filling.
        report : Whether report SQL execute information.
            - `None` : Use attribute `default_report`.
            - `bool` : Use this value.

        kwdata : Keyword parameters for filling.

        Returns
        -------
        Result object.
        """

        # Get parameter by priority.
        report = get_first_notnull(report, self.default_report, default="exception")

        # Handle parameter.
        if sql.__class__ == str:
            sql = text(sql)
        if data is None:
            if kwdata == {}:
                data = []
            else:
                data = [kwdata]
        else:
            if data.__class__ == dict:
                data = [data]
            elif isinstance(data, CursorResult):
                data = to_table(data)
            elif data.__class__ == DataFrame:
                data = to_table(data)
            else:
                data = data.copy()
            for param in data:
                param.update(kwdata)

        # Fill missing data.
        data = self.fill_data(data, sql)

        # Execute.

        ## Can retry.
        if self.begin_count == 0 and not self.is_multi_sql(sql):
            result = retry(
            self.executor,
            self.connection,
            sql,
            data,
            report,
            _report="Database execute operational error",
            _exception=OperationalError
        )

        ## Cannot retry.
        else:
            result = self.executor(self.connection, sql, data, report)

        return result


    def commit(self) -> None:
        """
        `Commit` cumulative executions.
        """

        # Commit.
        if self.begin is not None:
            self.begin.commit()
            self.begin = None
            self.begin_count = 0


    def rollback(self) -> None:
        """
        `Rollback` cumulative executions.
        """

        # Rollback.
        if self.begin is not None:
            self.begin.rollback()
            self.begin = None
            self.begin_count = 0


    def close(self) -> None:
        """
        `Close` database connection.
        """

        # Close.
        self.connection.close()


    __call__ = execute


    __del__ = close