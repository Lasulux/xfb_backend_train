import polars as pl
import requests
import base64
import os


def get_img_in_base64(img_url):
    r = requests.get(img_url)
    if r.status_code != requests.codes.ok:
        r.raise_for_status
    return encode_to_base64(r.content)


def encode_to_base64(data):
    return base64.b64encode(data)


def group_by_and_merge_df(
    df: pl.DataFrame, cols_to_group_by: str | list, new_col_name: str = "data", return_as_list_of_dicts: bool = False
) -> list | pl.DataFrame:
    """
    Groups a Polars DataFrame by specified columns and merges the rest into a single column.

    Args:
        df (pl.DataFrame): The input Polars DataFrame to process.
        cols_to_group_by (list): List of column names to group by.
        new_col_name (str, optional): Name of the new column that will contain the merged data. Defaults to 'data'.
        return_as_list_of_dicts (bool, optional): Flag indicating whether to return the result as a list of dictionaries or a Polars DataFrame. Defaults to False.

    Returns:
        list| pl.DataFrame: The processed DataFrame or list of dictionaries, depending on the return_as_list_of_dicts flag.
    """
    if isinstance(cols_to_group_by, str):
        cols_to_group_by = [cols_to_group_by]

    # Calculate the columns to merge by finding the difference between the DataFrame's columns and the columns specified to group by
    cols_to_merge = list(set(df.columns) - set(cols_to_group_by))

    # Add a new column to the DataFrame by structuring the columns selected for merging into a single column, named according to the new_col_name parameter
    df = df.with_columns(pl.struct(cols_to_merge).alias(new_col_name))

    # Drop the original columns that were merged to create the new column, avoiding redundancy
    df = df.drop(cols_to_merge)

    # Group the DataFrame by the specified columns and aggregate the newly created column, reducing the DataFrame to unique rows based on the grouping criteria and combining the merged data into a single column
    df = df.group_by(cols_to_group_by).agg(pl.col(new_col_name).drop_nulls())

    # Check the return_as_list_of_dicts flag. If true, convert the DataFrame to a list of dictionaries using.to_dicts() and return it. Otherwise, return the DataFrame as is
    if return_as_list_of_dicts:
        return df.to_dicts()
    return df


def get_exception_info(e: Exception) -> dict:
    """
    Extracts detailed information from a raised exception, including traceback details and custom attributes if present.

    Args:
        e (Exception): The exception instance from which to extract information.

    Returns:
        dict: A dictionary containing detailed information about the exception, including traceback, error message, and custom attributes.
    """
    # Initialize an empty list to collect traceback information
    trace = []

    # Start extracting traceback information from the given exception
    tb = e.__traceback__
    while tb is not None:
        # Append the current frame's filename, name, and line number to the trace list
        trace.append(
            {
                "filename": tb.tb_frame.f_code.co_filename,  # Filename of the current frame
                "name": tb.tb_frame.f_code.co_name,  # Name of the current frame
                "lineno": tb.tb_lineno,  # Line number within the current frame
            }
        )
        # Move to the next frame in the traceback
        tb = tb.tb_next

    # Set the traceback pointer to None to prevent infinite loops
    tb = None

    # Attempt to extract custom attribute 'Data' from the exception
    data = e.Data if "Data" in e.__dict__ else None

    # Attempt to extract custom attribute 'ErrorCd' from the exception
    error_cd = e.ErrorCd if "ErrorCd" in e.__dict__ else None

    # Return a dictionary containing the extracted information
    return {
        "ErrorType": type(e).__name__,  # Type of the exception
        "ErrorMsg": str(e),  # Error message associated with the exception
        "ErrorTrace": trace,  # Traceback information
        "ErrorData": data,  # Custom 'Data' attribute, if present
        "ErrorCd": error_cd,  # Custom 'ErrorCd' attribute, if present
    }


def string_multi_replace(text: str, replace_dict: dict):
    """runs a multi replace in one go

    Args:
        text (str): text to run replace on
        replace_dict (dict): key: value to replace, value: string to replace the key with
    """

    for k, v in replace_dict.items():
        text = text.replace(k, v)
    return text


def create_dir_if_needed(location: str):
    """Checks and creates the directories and all intermediate subdirectories specified in the input

    Args:
        location (str): path of the folder structures that are needed
    """
    # Create all intermediate subdirectories --> os.makedirs()
    if not os.path.isdir(location):
        os.makedirs(location, exist_ok=True)
