# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:09:42
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : System methods.
"""


from typing import Any, List, Dict, Tuple, Iterable, Type, Literal, Optional, Union, NoReturn, overload
from types import TracebackType
from sys import exc_info
from traceback import format_exc, format_stack, extract_stack
from warnings import warn as warnings_warn
from varname import argname


__all__ = (
    "is_iterable",
    "is_table",
    "is_number_str",
    "get_first_notnull",
    "get_name",
    "RException",
    "RStack",
    "rexc",
    "rstack"
)


def is_iterable(obj: Any, exclude_types: Iterable[Type] = [str, bytes]) -> bool:
    """
    Judge whether it is `iterable`.

    Parameters
    ----------
    obj : Judge object.
    exclude_types : Non iterative types.

    Returns
    -------
    Judgment result.
    """

    # Exclude types.
    if obj.__class__ in exclude_types:
        return False

    # Judge.
    try:
        obj_dir = obj.__dir__()
    except TypeError:
        return False
    if "__iter__" in obj_dir:
        return True
    else:
        return False


def is_table(obj: Any, check_fields: bool = True) -> bool:
    """
    Judge whether it is `List[Dict]` table format and keys and keys sort of the Dict are the same.

    Parameters
    ----------
    obj : Judge object.
    check_fields : Do you want to check the keys and keys sort of the Dict are the same.

    Returns
    -------
    Judgment result.
    """

    # Judge.
    if obj.__class__ != list:
        return False
    for element in obj:
        if element.__class__ != dict:
            return False

    ## Check fields of table.
    if check_fields:
        keys_strs = [
            ":".join([str(key) for key in element.keys()])
            for element in obj
        ]
        keys_strs_only = set(keys_strs)
        if len(keys_strs_only) != 1:
            return False

    return True


def is_number_str(string: str) -> bool:
    """
    Judge whether it is `number` string.

    Parameters
    ----------
    string : String.

    Returns
    -------
    Judgment result.
    """

    # Judge.
    try:
        int(string)
    except (ValueError, TypeError):
        return False

    return True


def get_first_notnull(
    *values: Any,
    default: Union[None, Any, Literal["exception"]] = None,
    nulls: Tuple = (None,)) -> Any:
    """
    Get the first value that is not `None`.

    Parameters
    ----------
    values : Check values.
    default : When all are null, then return this is value, or throw exception.
        - `Any` : Return this is value.
        - `Literal['exception']` : Throw `exception`.

    nulls : Range of null values.

    Returns
    -------
    Return first not null value, when all are `None`, then return default value.
    """

    # Get value.
    for value in values:
        if value not in nulls:
            return value

    # Throw exception.
    if default == "exception":
        vars_name = get_name(values)
        if vars_name is not None:
            vars_name_de_dup = list(set(vars_name))
            vars_name_de_dup.sort(key=vars_name.index)
            vars_name_str = " " + " and ".join([f"'{var_name}'" for var_name in vars_name_de_dup])
        else:
            vars_name_str = ""
        raise ValueError(f"at least one of parameters{vars_name_str} is not None")

    return default


def get_name(obj: Any, frame: int = 2) -> Optional[Union[str, Tuple[str, ...]]]:
    """
    Get object `name`.

    Parameters
    ----------
    obj : Object.
    frame : Number of code to upper level.

    Returns
    -------
    Object name or None.
    """

    # Get name using built in method.
    try:
        name = obj.__name__
    except AttributeError:

        # Get name using module method.
        name = "obj"
        try:
            for _frame in range(1, frame + 1):
                name = argname(name, frame=_frame)
            if name.__class__ != str:
                if "".join(name) == "":
                    name = None
        except:
            name = None

    return name


class RException(object):
    """
    Rey's `exception` type.
    """


    def throw(
        self,
        exception: Type[BaseException] = AssertionError,
        value: Optional[Any] = None,
        frame: int = 2
    ) -> NoReturn:
        """
        Throw `exception`.

        Parameters
        ----------
        exception : Exception Type.
        value : Exception value.
        frame : Number of code to upper level.
        """

        # Get parameter.
        if value is not None:
            value_name = get_name(value, frame)
        else:
            value_name = None

        ## Exception text.
        if exception == AssertionError:
            if value_name is None:
                text = "use error"
            else:
                text = "parameter '%s' use error" % value_name
        elif exception == ValueError:
            if value_name is None:
                text = "value error"
            else:
                text = "parameter '%s' value error, now is %s" % (value_name, repr(value))
        elif exception == TypeError:
            if value_name is None:
                text = "value type error"
            else:
                text = "parameter '%s' value type error, now is %s" % (value_name, value.__class__)

        # Raise.
        exception = exception(text)
        raise exception


    def catch(self, title: Optional[str] = None) -> Tuple[str, Type[BaseException], BaseException, TracebackType]:
        """
        Catch `exception information` and print, must used in `except` syntax.

        Parameters
        ----------
        title : Print title.
            - `None` : Not print.
            - `str` : Print and use this title.

        Returns
        -------
        Exception report text and exception type and exception instance and exception position instance.
        """

        # Get parameter.
        exception_report = format_exc()
        exception_report = exception_report.strip()
        exception_type, exception, traceback = exc_info()

        # Print.
        if title is not None:

            ## Import.
            from .rprint import rprint

            ## Execute.
            rprint(exception_report, title=title, frame="half")

        return exception_report, exception_type, exception, traceback


    def warn(self, *infos: Any, exception: Type[BaseException] = UserWarning, stacklevel: int = 3) -> None:
        """
        Throw `warning`.

        Parameters
        ----------
        infos : Warn informations.
        exception : Exception type.
        stacklevel : Warning code location, number of recursions up the code level.
        """

        # Handle parameter.
        if infos == ():
            infos = "Warning!"
        elif len(infos) == 1:
            if infos[0].__class__ == str:
                infos = infos[0]
            else:
                infos = str(infos[0])
        else:
            infos = str(infos)

        # Throw warning.
        warnings_warn(infos, exception, stacklevel)


    def check_target(self, value: Any, *targets: Union[Any, Literal["_iterable"]], check_element: bool = False) -> None:
        """
        Check the content or type of the value, when check fail, then throw `exception`.

        Parameters
        ---------
        value : Check object.
        targets : Correct target, can be type.
            - `Any` : Check whether it is the target.
            - `Literal['_iterable']` : Check whether it can be iterable.

        check_element : Whether check element in value.
        """

        # Handle parameter.
        if check_element:
            values = value
        else:
            values = [value]

        # Check.
        for element in values:

            ## Check sub elements.
            if "_iterable" in targets and is_iterable(element):
                continue

            ## Right target.
            if element.__class__ in targets:
                continue
            for target in targets:
                if element is target:
                    continue

            ## Throw exception.
            var_name = get_name(value)
            if var_name is not None:
                var_name = f" '{var_name}'"
            else:
                var_name = ""
            correct_targets_str = ", ".join([repr(target) for target in targets])
            if check_element:
                raise ValueError(f"parameter{var_name} the elements content or type must in [{correct_targets_str}], now: {repr(value)}")
            else:
                raise ValueError(f"parameter{var_name} the content or type must in [{correct_targets_str}], now: {repr(value)}")


    def check_least_one(self, *values: Any) -> None:
        """
        Check that at least one of multiple values is not `None`, when check fail, then throw `exception`.

        Parameters
        ----------
        values : Check values.
        """

        # Check.
        for value in values:
            if value is not None:
                return

        # Throw exception.
        vars_name = get_name(values)
        if vars_name is not None:
            vars_name_de_dup = list(set(vars_name))
            vars_name_de_dup.sort(key=vars_name.index)
            vars_name_str = " " + " and ".join([f"'{var_name}'" for var_name in vars_name_de_dup])
        else:
            vars_name_str = ""
        raise ValueError(f"at least one of parameters{vars_name_str} is not None")


    def check_most_one(self, *values: Any) -> None:
        """
        Check that at most one of multiple values is not `None`, when check fail, then throw `exception`.

        Parameters
        ----------
        values : Check values.
        """

        # Check.
        none_count = 0
        for value in values:
            if value is not None:
                none_count += 1

        # Throw exception.
        if none_count > 1:
            vars_name = get_name(values)
            if vars_name is not None:
                vars_name_de_dup = list(set(vars_name))
                vars_name_de_dup.sort(key=vars_name.index)
                vars_name_str = " " + " and ".join([f"'{var_name}'" for var_name in vars_name_de_dup])
            else:
                vars_name_str = ""
            raise ValueError(f"at most one of parameters{vars_name_str} is not None")


    __call__ = throw


class RStack(object):
    """
    Rey's `stack` type.
    """


    def get_stack_text(self, format_: Literal["plain", "full"] = "plain", limit: int = 2) -> str:
        """
        Get code stack text.

        Parameters
        ----------
        format_ : Stack text format.
            - `Literal['plain'] : Floor stack position.
            - `Literal['full'] : Full stack information.

        limit : Stack limit level.

        Returns
        -------
        Code stack text.
        """

        # Plain.
        if format_ == "plain":
            limit += 1
            stacks = format_stack(limit=limit)

            ## Check.
            if len(stacks) != limit:
                raise rexc(value=limit)

            ## Convert.
            text = stacks[0]
            index_end = text.find(", in ")
            text = text[2:index_end]

        # Full.
        elif format_ == "full":
            stacks = format_stack()
            index_limit = len(stacks) - limit
            stacks = stacks[:index_limit]

            ## Check.
            if len(stacks) == 0:
                raise rexc(value=limit)

            ## Convert.
            stacks = [
                stack[2:].replace("\n  ", "\n", 1)
                for stack in stacks
            ]
            text = "".join(stacks)
            text = text[:-1]

        # Raise.
        else:
            rexc(ValueError, format_)

        return text


    @overload
    def get_stack_param(self, format_: Literal["floor"] = "floor", limit: int = 2) -> Dict: ...

    @overload
    def get_stack_param(self, format_: Literal["full"] = "floor", limit: int = 2) -> List[Dict]: ...

    def get_stack_param(self, format_: Literal["floor", "full"] = "floor", limit: int = 2) -> Union[Dict, List[Dict]]:
        """
        Get code stack parameters.

        Parameters
        ----------
        format_ : Stack parameters format.
            - `Literal['floor']` : Floor stack parameters.
            - `Literal['full']` : Full stack parameters.

        limit : Stack limit level.

        Returns
        -------
        Code stack parameters.
        """

        # Get.
        stacks = extract_stack()
        index_limit = len(stacks) - limit
        stacks = stacks[:index_limit]

        # Check.
        if len(stacks) == 0:
            raise rexc(value=limit)

        # Convert.

        ## Floor.
        if format_ == "floor":
            stack = stacks[-1]
            params = {
                "filename": stack.filename,
                "lineno": stack.lineno,
                "name": stack.name,
                "line": stack.line
            }

        ## Full.
        elif format_ == "full":
            params = [
                {
                    "filename": stack.filename,
                    "lineno": stack.lineno,
                    "name": stack.name,
                    "line": stack.line
                }
                for stack in stacks
            ]

        return params


    @property
    def text(self) -> str:
        """
        Get stack plain text.
        """

        # Get.
        result = self.get_stack_text("plain", 3)

        return result


    @property
    def texts(self) -> str:
        """
        Get stack full text.
        """

        # Get.
        result = self.get_stack_text("full", 3)

        return result


    @property
    def param(self) -> Dict:
        """
        Get stack floor parameter.
        """

        # Get.
        result = self.get_stack_param("floor", 3)

        return result


    @property
    def params(self) -> List[Dict]:
        """
        Get stack full parameters.
        """

        # Get.
        result = self.get_stack_param("full", 3)

        return result


# Instance.

## Type "RException".
rexc = RException()

## Type "RStack".
rstack = RStack()