""" This file is  responsible for outlining the 
forms and type of data we import and export from API """
from datetime import date
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

class StaticPlayer(BaseModel):
    """ Main API Endpoint for player info"""
    player_id : int = Field(alias="id")
    name : str = Field(alias="full_name")

class IndexPlayer(BaseModel):
    """ Represents Needed Info from playerindex endpoint"""
    player_id :int = Field(alias="PERSON_ID")
    position : str = Field(alias="POSITION")
    current_team_id : int = Field(alias="TEAM_ID")
    current_team_name : str | None = Field(alias="TEAM_NAME")
## Player.position
## Player.current_team_id
##player.stats

class GameLogRow(BaseModel):
    """ Represents information from teamgamelogs API endpoint """
    game_id : str = Field(alias="GAME_ID")
    game_date : date = Field(alias="GAME_DATE")
    season : str = Field(alias="SEASON_YEAR")
    team_id : int = Field(alias="TEAM_ID")
    final_score : int = Field(alias="PTS")
    matchup : str = Field(alias="MATCHUP")
    team_name : str = Field(alias="TEAM_NAME")

class PlayerLogRow(BaseModel):
    """ Represents information from playergamelogs API endpoint"""
    game_id: str = Field(alias="GAME_ID")
    player_id : int = Field(alias="PLAYER_ID")
    player_name : str =Field(alias="PLAYER_NAME")
    team_id : int = Field(alias="TEAM_ID")
    pts : int = Field(alias="PTS")
    ast: int = Field(alias="AST")
    total_rebounds : int = Field(alias="REB")
    fga : int = Field(alias="FGA")
    fgm: int = Field(alias="FGM")
    threepm : int = Field(alias="FG3M")
    threepa : int = Field(alias="FG3A")
    min : float = Field(alias="MIN")
    fta : int  = Field(alias="FTA")
    ftm : int = Field(alias="FTM")
    steals : int = Field(alias="STL")
    blocks : int = Field(alias="BLK")
    off_rebounds : int = Field(alias="OREB")
    def_rebounds :int = Field(alias="DREB")
    turnovers : int = Field(alias="TOV")
