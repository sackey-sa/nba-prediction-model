""" Scrap File to view the shape of API Endpoints"""
from pprint import pprint
from typing import Any
from sqlalchemy.orm import Session
from nba_api.stats.endpoints import TeamGameLogs,teamgamelogs  #type: ignore[import-untyped]
from nba_api.stats.static import players #type: ignore[import-untyped]
from data_access.database import engine
from data_access.models import Player


SEASON = "2026-27"
SEASON_TYPE = "Regular Season"
STATUS = "FINISHED"

def fetch_games() -> dict[str,Any]:
    """ Function grabs initial game info from API"""

    game_info = teamgamelogs.TeamGameLogs(season_nullable=SEASON,season_type_nullable=SEASON_TYPE).get_normalized_dict()
    game_info_rows = game_info["TeamGameLogs"]

    game_by_id: dict[str,list[dict[str,Any]]] = {}

    for row in game_info_rows:
        game_id = row["GAME_ID"]
     
        if game_id not  in game_by_id:
            game_by_id[game_id] = []
          
        game_by_id[game_id].append(row)
        
    pprint(len(game_by_id))
    pprint(game_by_id["0022600281"]) 
    #pprint(game_by_id.keys())

    return game_by_id


fetch_games()
