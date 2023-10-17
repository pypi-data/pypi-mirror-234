# CHANGE LOG
#
# 2023-09-05
# Added:
# generate_random_token()
# parse_row_into_object()
# afg_base_object_class
# afg_freezable_object_class
# query_result_class
# type hints to function definitions
#
# get_username() removed, now it is uwtool-specific, to be replaced with a general purpose
# session handling function (to be used not only in uwtool)

import time
import string
import secrets
# from os import environ
# from .db import DB, sql
from pandas import DataFrame
import pyodbc
from afgutils.db import DB

# session_token_cookie_name = "uwtool_session_token"


def print_log(log_line: str):
    print(time.strftime('%Y-%m-%d %H:%M:%S'), log_line)


def ci(cursor: pyodbc.Cursor, column_name: str)-> int:
    column_index_cnt = -1
    column_index = -1
    for column in cursor.description:
        column_index_cnt = column_index_cnt + 1
        if column[0] == column_name:
            column_index = column_index_cnt
            break
    if column_index == -1:
        raise SystemExit("ERROR: Column index not found for column: " + column_name)
    return column_index


def nvl(s, d):
    if s is None:
        return d
    else:
        return s


def iif(bool_val: bool, ret_true, ret_false):
    if bool_val:
        aaa = ret_true
    else:
        aaa = ret_false
    return aaa


def isnullorempty(v)-> bool:
    if v is None:
        return True
    if type(v) == str:
        v = v.strip()
        if len(v) == 0:
            return True
    return False


def clear_mfv(mfv: dict)-> dict:
    if type(mfv) == dict:
        for i in mfv.keys():
            mfv[i] = None
    return mfv


# def get_username()-> str:
#     conn_repserv = DB.get_connection('repserv')
#     cursor_repserv = conn_repserv.cursor()
#
#     username = None
#
#     if 'HTTP_COOKIE' in environ:
#         for cookie in map(str.strip, environ['HTTP_COOKIE'].split(';')):
#             key, value = cookie.split('=')
#             if key == session_token_cookie_name:
#                 uwtool_session_token = value
#                 result = DB.execute(cursor=cursor_repserv,
#                                     query=sql("find_session", 2),
#                                     fetch='one',
#                                     parameters=uwtool_session_token)
#                 if result:  # can be replaced by "if cursor_repserv.rowcount"
#                     username = result['username']
#                     DB.execute(cursor_repserv, sql("update_session", 1), None, (uwtool_session_token, username))
#                     cursor_repserv.commit()
#
#     cursor_repserv.close()
#
#     return username


def data_vector_to_sql_insert(data_vector: dict | DataFrame, insert_sql_tpl: str = None,
                              existing_values: list = None) -> (list, str):
    column_names_insert_text = ""
    item_values = []

    # convert data vector into a list
    if isinstance(data_vector, DataFrame):
        for column_name in data_vector.columns.tolist():
            column_names_insert_text = (column_names_insert_text + "," + column_name + "\r\n").replace(".", "_")
            item_values.append(data_vector.loc[0, column_name])

    elif type(data_vector) is dict:
        pass

    else:
        raise TypeError("data_vector_to_sql_insert: data_vector must be a pandas.DataFrame or a dictionary")

    # text-serialize any embedded lists or dictionaries
    item_values = [str(item_value) if type(item_value) in (list, dict) else item_value for item_value in item_values]

    # combine existing values with new values
    if type(existing_values) is list:
        result_items = existing_values + item_values
    elif existing_values is None:
        result_items = item_values
    else:
        raise TypeError("data_vector_to_sql_insert: existing_values must be a list or None")

    # generate SQL
    if type(insert_sql_tpl) is str:
        result_sql = insert_sql_tpl.format(column_names_insert_text, f"{', ?' * len(item_values)}")
    elif insert_sql_tpl is None:
        result_sql = column_names_insert_text
    else:
        raise TypeError("data_vector_to_sql_insert: insert_sql_tpl must be a string or None")

    return result_items, result_sql


def generate_random_token(length: int = 16)-> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def parse_row_into_object(result_row: dict, obj: object, strict_attributes: bool = True,
                          add_attributes: bool = False) -> None:
    # strict_attributes=true requires all attributes in the srouce row to be present in the target object
    # add_attributes=true adds attributes to the target object if they are not present in the source row

    # if (result_row is None) or (not isinstance(result_row, tuple)):
    #     raise Exception("parse_row_into_object: result_row is None or not a list")

    for column_name in result_row:
        if not hasattr(obj, column_name) and strict_attributes:
            raise Exception("parse_row_into_object: object does not have attribute: " + column_name)
        if not hasattr(obj, column_name) and not add_attributes:
            continue
        setattr(obj, column_name, result_row[column_name])


class afg_base_object_class(object):
    def __str__(self):
        result_dict = {}

        for b in dir(self):
            if not b.startswith("_") and not callable(getattr(self, b)):
                result_dict[b] = getattr(self, b)

        return str(result_dict)

    def __setattr__(self, key, value):
        if callable(getattr(self, key, None)):
            # callable attributes cannot be set/overloaded at runtime
            raise AttributeError("%r modification of callable attribute is not allowed: %s" % (self, key))
        super().__setattr__(key, value)

    def __iter__(self):
        for b in dir(self):
            if not b.startswith("_") and not callable(getattr(self, b)):
                yield b, getattr(self, b)


class afg_freezable_object_class(afg_base_object_class):
    __isfrozen = False

    def __init__(self):
        self._freeze()  # prevent adding new or altering existing attributes to the object after initialisation
        super().__init__()

    def __setattr__(self, key, value):
        if self.__isfrozen and (key[-10:] != "__isfrozen"):  # and not hasattr(self, key):
            raise TypeError("%r is a frozen class" % self)
        super().__setattr__(key, value)

    def __delattr__(self, item):
        if self.__isfrozen:
            raise TypeError("%r is a frozen class" % self)
        super().__delattr__(item)

    def _freeze(self):
        self.__isfrozen = True

    def _unfreeze(self):
        self.__isfrozen = False

    def set_frozen_attrib(self, key: str, value: any) -> None:
        self._unfreeze()
        setattr(self, key, value)
        self._freeze()

    def del_frozen_attrib(self, key: str) -> None:
        self._unfreeze()
        delattr(self, key)
        self._freeze()


class query_result_class(afg_freezable_object_class):
    def __init__(self, db_cursor: pyodbc.Cursor = None, query_text: str = None, query_params: tuple = None,
                 strict_attributes: bool = True, add_attributes: bool = False):
        if db_cursor is None or query_text is None:
            return
        if query_params is not None and type(query_params) is not tuple:
            raise Exception("%r query_params is not a tuple" % self)
        result_row = DB.execute(db_cursor, query_text, parameters=query_params, fetch='one')

        if result_row is not None:
            parse_row_into_object(result_row, self, strict_attributes, add_attributes)

        super().__init__()
