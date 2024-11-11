from api_base import APIBase
from TutorialUtils import SqlToListOfDicts


def GetPlayerbyKey(playertablename, key, value, cols_to_show, count=False):
    if count:
        countinsert = f"SELECT COUNT({key}) cnt FROM ("
        countinsert2 = " ) subquery"
    else:
        countinsert = ""
        countinsert2 = ""
    sql = (
    countinsert    
    + "SELECT * FROM "
    + playertablename
    + " WHERE "
    + f"{key}='{value}'"
    + countinsert2
    )
    if count: 
        output = SqlToListOfDicts(keys=cols_to_show, raw_query=sql) #unable to get count column to be called cnt
        return output[0]['player_id']
    else:
        return SqlToListOfDicts(keys=cols_to_show, raw_query=sql)

class SearchPlayer(APIBase):
    __slots__ = "cols", "player_ids", "players", "search_param","playertablename"

    def __init__(self, search_param: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.cols = [
            "player_id",
            "club_name",
            "team_id",
            "team_short_name",
            "surname",
            "first_name",
            "birthdate",
            "alias",
            "team_logo_url",
        ]
        self.playertablename = "Players_tutorial"
        self.players = []
        self.search_param = search_param.lower()
        
    def GetPlayerData(self):
        sql = (
            "SELECT "
            + ",".join(self.cols)
            + " FROM " 
            + (self.playertablename)
            + " WHERE "
            + f" LOWER(alias) COLLATE SQL_Latin1_General_CP1_CI_AI LIKE '%{self.search_param}%'"
        )
        self.players = SqlToListOfDicts(keys=self.cols, raw_query=sql)

    def run(self):
        
        self.GetPlayerData()
        return {"Players": self.players}