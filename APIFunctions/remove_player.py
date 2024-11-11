from api_base import APIBase
from TutorialUtils import DBRunQuery, SqlToListOfDicts
from search_players import GetPlayerbyKey


class RemovePlayer(APIBase):
    __slots__ = "cols", "key", "value","playertablename","players"
    def __init__(self, key_param: str,value_param: str, **kwargs) -> None:
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
        self.key = key_param
        self.value =  value_param
        self.players=[]

    def DeletePlayerData(self):
        sql = (
        "DELETE FROM "
        + self.playertablename
        + " WHERE "
        + self.key + "="
        + f"'{self.value}'"
        )
        return DBRunQuery(raw_query=sql)
    

    def run(self):
        self.players = GetPlayerbyKey(self.playertablename,self.key,self.value,self.cols)
        self.DeletePlayerData()
        return {f"Deleted rows in {self.playertablename} where {self.key}=={self.value}:"
                :self.players}