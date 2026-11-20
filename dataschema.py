from pydantic import BaseModel, Field

class StaticTeam(BaseModel):
    id:int
    full_name:str
    abbreviation:str
    
class StandingsTeam(BaseModel):
    team_id : int = Field(alias="TeamID")
    conference : str = Field("Conference")
    division : str = Field("Division")
    
    ## Rule of thumb, if the API's name already fits your code style,use it directly. if it dosen't alias it 