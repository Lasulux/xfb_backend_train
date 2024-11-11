from TutorialUtils import GetUserData


class APIBase:
    """Base API class

    Raises:
        NotImplementedError: _description_
    """

    __slots__ = "LangID", "UserID", "UserName"

    def __init__(self, UserOID=None, UserID=None, LangID: str | None = None) -> None:
        self.LangID = LangID
        self.UserID = UserID
        # if self.UserID is None and UserOID is not None:
        #     UserData = GetUserData(UserOID=UserOID)
        #     self.UserID = UserData["user_id"]
        #     self.UserName = UserData["user_name"]
        #     del UserData

    def run(self):
        raise NotImplementedError("run has to be implemented")
