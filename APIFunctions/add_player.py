from api_base import APIBase
from TutorialUtils import DBRunQuery
from search_players import GetPlayerbyKey



class AddPlayer(APIBase):
    __slots__ = "cols", "player_ids", "players", "add_param_dict","playertablename"
    def __init__(self, add_param_dict: dict, **kwargs) -> None:
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
        self.add_param_dict =  add_param_dict

    def InsertPlayerData(self):
        # sql = (
        # "Insert into "
        # + self.playertablename
        # + f" ({','.join(self.cols)})"
        # + " VALUES('"
        # + "','".join(self.add_params)
        # + "');"
        # )
        
        sql = "INSERT Into "+ self.playertablename +" (" #keys here, , 
        values =""
        for key,val in self.add_param_dict.items():
            sql+=f"{key},"
            if val is None:
                values+= "NULL,"
            else:
                if isinstance (val, str):
                    values+= f"'{val}',"
                else:
                    values+= f"{val}," #a number
        sql=sql[:-1] # remove last ","
        values=values[:-1] # remove last ","
        sql+=f") VALUES({values})"

        return DBRunQuery(raw_query=sql) 

    def run(self):
        if GetPlayerbyKey(self.playertablename,"player_id",self.add_param_dict["player_id"],self.cols,count=True) > 0:
            return{"Player with same ID already in database. Ignoring command"}
        else:
            output = self.InsertPlayerData()
            return {f"Added player with id: {self.add_param_dict['player_id']}"}