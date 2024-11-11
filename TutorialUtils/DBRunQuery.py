# 2. Third party packages
from django.db import connections
from TutorialUtils import MTKExceptions
import polars as pl


def DBRunQuery(raw_query: str, can_be_empty: bool = False, db_name="default") -> list | None:
    """Runs the SQL query on the DB and returns the output of that query.

    Args:
        raw_query (str): SQL query

    Args:
        raw_query (str): SQL query
        can_be_empty (bool, optional): If the return of the query can be empty. Defaults to False.
        db_name (str, optional): Database name. Defaults to "default". Can be default or ZION

    Returns:
        dict: status dict, data has a list of lists of the table (list of rows that has the list of columns)
    """
    if db_name != "default":
        db_name = db_name.upper()
    # DB read by the given raw query
    row = None
    with connections[db_name].cursor() as cursor:  # create a connection cursor
        try:
            cursor.execute(raw_query)  # execute the query
        except Exception as e:
            raise MTKExceptions.DBError(sql=raw_query, message=f"An error occured with the database: {e}")
        if raw_query.upper().startswith("SELECT") or cursor.description is not None:
            row = cursor.fetchall()  # get all the rows
            if not row and not can_be_empty:  # if empty error
                raise MTKExceptions.DBError(sql=raw_query, message=f"No output for sql")
    return row


def sql_output_to_list_of_dicts(keys: list, list_of_rows: list) -> list:
    """
    Generates a dict from the sql output of list of lists
    """

    return [dict(zip(keys, list_)) for list_ in list_of_rows]


def sql_output_to_pl_df(keys: list, list_of_rows: list) -> pl.DataFrame:
    """Generates polars DataFrame from SQL output

    Args:
        keys (list): List of column names
        list_of_rows (list): List of rows, where each row is represented as a tuple

    Returns:
        pl.DataFrame: Polars DataFrame
    """
    list_of_dicts = sql_output_to_list_of_dicts(keys=keys, list_of_rows=list_of_rows)
    # raise MTKExceptions.DataError(message=str(list_of_dicts))
    # Create Polars DataFrame
    return pl.DataFrame(list_of_dicts, infer_schema_length=5000)


def SqlToPlDF(keys, raw_query: str, can_be_empty: bool = False, db_name="default"):
    out = DBRunQuery(raw_query=raw_query, can_be_empty=can_be_empty, db_name=db_name)
    return sql_output_to_pl_df(keys=keys, list_of_rows=out)


def SqlToListOfDicts(keys, raw_query: str, can_be_empty: bool = False, db_name="default"):
    out = DBRunQuery(raw_query=raw_query, can_be_empty=can_be_empty, db_name=db_name)
    return sql_output_to_list_of_dicts(keys=keys, list_of_rows=out)
