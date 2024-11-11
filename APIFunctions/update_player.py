from api_base import APIBase
from TutorialUtils import DBRunQuery, SqlToListOfDicts
from search_players import GetPlayerbyKey

class UpdatePlayer(APIBase):
    __slots__ = "cols","playerkey", "key", "value","playertablename","players","updatedplayers"
    def __init__(self, playerkey_param:int, key_param: str,value_param: str, **kwargs) -> None:
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
        self.playerkey = playerkey_param

    def UpdatePlayerData(self):
        sql = (
        f"UPDATE {self.playertablename} "
        +f"SET {self.key} = '{self.value}'"
        +f" WHERE player_id={self.playerkey}"
        )
        return DBRunQuery(raw_query=sql)
        
    

    def run(self):
        if self.key=="player_id":
            return {"Cannot update player ID, please remove and add new entry instead"}
        else:
            self.players = GetPlayerbyKey(self.playertablename,"player_id",self.playerkey,self.cols)
            self.UpdatePlayerData()
            self.updatedplayers = GetPlayerbyKey(self.playertablename,"player_id",self.playerkey,self.cols)
            return {f"Updated entries in {self.playertablename} where {self.key}=={self.value}:"
                    :self.players,
                    "updated:"
                    :self.updatedplayers}