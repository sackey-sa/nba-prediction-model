""" This file is  responsible for outlining the 
forms and type of data we import and export from API """
from pydantic import BaseModel, Field

class StaticTeam(BaseModel):
    """ Describes the form of static data for Teams(ID,Name,Abbreviation)"""
    id:int
    full_name:str
    abbreviation:str

class StandingsTeam(BaseModel):
    """ Describes the form of data from standings endpoint(conference,division)"""
    team_id : int = Field(alias="TeamID")
    conference : str = Field(alias="Conference")
    division : str = Field(alias="Division")

 ## Rule of thumb, if the API's name already fits your code style,
 # use it directly. if it dosen't alias it
