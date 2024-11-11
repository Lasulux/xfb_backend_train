from .DBRunQuery import DBRunQuery
from .BackendUtils import get_exception_info, string_multi_replace, create_dir_if_needed
import os
from datetime import date, datetime
from json import dump as json_dump
from django.http import HttpResponse
from .mailing import send_email
import io
from inspect import currentframe


def GetNewIndentityID():
    """When inserting a row to a table with identity ID column, we may need that id.
    This function returns that id (be aware that this uses SCOPE_IDENTITY therefore that is a DB level information inside a scope)

    Returns:
        _type_: status where the data is the newest id in the scope
    """
    sql = "SELECT SCOPE_IDENTITY() AS [SCOPE_IDENTITY];"
    out = DBRunQuery(raw_query=sql)
    return out[0][0]


def GetUserData(UserOID, can_be_empty=False):
    if UserOID:
        cols = ["user_id", "user_name"]
        sql = "SELECT " + ", ".join(cols) + " FROM dim_users " + f"WHERE OID = '{UserOID}'"
        out = DBRunQuery(raw_query=sql, can_be_empty=can_be_empty)
        if out:
            return {x: y for x, y in zip(cols, out[0])}
    return {x: None for x in cols}


def HandleError(e, input):
    CalledAPI = currentframe().f_back.f_code.co_name
    exception_info = get_exception_info(e=e)
    ErrorMsg = "An unexpected error occurred"
    if exception_info["ErrorMsg"]:
        ErrorMsg = exception_info["ErrorMsg"]
    out = {"ErrorMsg": ErrorMsg}
    if os.environ.get("DEBUG") == "True":
        out["ErrorData"] = exception_info
    # Get the value for 'UserID' key or default to ''
    if input:
        user_id = input.get("UserID", "")
        # Get the user name or default to "unknown user"
        input["UserName"] = "unknown user"
        if user_id:
            input["UserName"] = GetUserData(user_id, can_be_empty=True).get("UserName", "unknown user")
        # Delete the 'UserID' key from the dictionary
        input.pop("UserID", None)
    # send_logs(exception_info=exception_info, input=input, CalledAPI=CalledAPI)
    return out


def send_logs(exception_info, input, CalledAPI):
    time_of_error = string_multi_replace(
        text=str(datetime.now()).split(".")[0], replace_dict={k: "_" for k in [" ", ":", "-"]}
    )
    # create the message
    username = "Unknown User"
    if input:
        if "UserName" in input:
            username = input["UserName"]
    msg = f"Error occured for endpoint {CalledAPI} for UserName: {username} generated an error."
    attachments = []
    attachments.append({"file_name": "Exception.txt", "file_content": str(exception_info), "mime_type": "text/plain"})
    if "FILE" in input:
        attachments.append(
            {
                "file_name": input["FILE"].name,
                "file_content": input["FILE"].read(),
                "mime_type": input["FILE"].content_type,
            }
        )
        del input["FILE"]
    attachments.append({"file_name": "Input.txt", "file_content": str(input), "mime_type": "text/plain"})
    # send the message
    send_email(
        message=msg,
        subject=f'Nucleus Scouting {os.environ.get("ENVIRONMENT_NAME")} runtime error: {time_of_error}',
        recipient_list_name="ERROR_RECIPIENTS",
        attachments=attachments,
    )


def SaveLog(status: dict, user_id=""):
    base_path = os.path.join("error_logs", str(date.today()))
    path = os.path.join("/tmp/cube", base_path)
    create_dir_if_needed(path)

    # create file name
    time_of_error = string_multi_replace(
        text=str(datetime.now()).split(".")[0], replace_dict={k: "_" for k in [" ", ":", "-"]}
    )
    path = os.path.join(path, f"{user_id}_{time_of_error}.json")
    # add session cache to status data
    data = status.copy()
    # save the log data
    with open(path, "w") as f:
        json_dump(data, f)


def GenFileResponse(file, filename: str) -> HttpResponse:
    """Generate an HttpResponse for file download

    Args:
        file (_type_): file as a variable to be returned
        filename (str): the filename to be used

    Returns:
        HttpResponse: HttpResponse for file download
    """
    # Create a response object
    response = HttpResponse(file, content_type="text/plain")
    # update content disposition to be able to be downloaded
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
