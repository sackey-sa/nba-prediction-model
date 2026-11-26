""" File is dedicated to validating and loading player data"""

from typing import Any
from sqlalchemy.orm import Session
from nba_api.stats.endpoints import playerindex  #type: ignore[import-untyped]
from nba_api.stats.static import players #type: ignore[import-untyped]
from data_access.database import engine
from data_access.models import Player
from data_access.dataschema import StaticPlayer,IndexPlayer

##Info I neeed
## Per Player We need
## Player.player_d
##Player.name

## Player.position
## Player.current_team_id
##player.stats

## Step 1-> Find and Understamd API endpoints and static info


SEASON = "2026-27"

def fetchplayers() -> tuple[list[dict[str,Any]],dict[str,Any]]:
    """ Function grabs player specific information from nba_api"""
    active_players = players.get_active_players()
    player_data = playerindex.PlayerIndex(season=SEASON,timeout=30).get_normalized_dict()
    print(len(active_players))
    return active_players,player_data

 ## Step 2 -> Match and validate each player within the list of active players to
 # their proper commonplayer info including team info
def validateplayers(active_players : list[dict[str,Any]],player_data : dict[str,Any]) -> tuple[list[StaticPlayer],dict[int,IndexPlayer]]:
    """ Function transform validated and proper data into structured pydantic objects"""

    valid_players = [StaticPlayer.model_validate(p) for p in active_players]
    ## Basically shrinks the list of ALL that player info into just the info we need, so list of like static player objects
    player_data_per = player_data["PlayerIndex"]
    ## Huge list of dictionary values, with all  OTHER information for player
    valid_data_per = [IndexPlayer.model_validate(p) for p in player_data_per]
    ## Shrinks all the extra info into index player objects so we have the other info
    player_by_id = {p.player_id: p for  p in valid_data_per}
    ## Creates a hashmap of player ID's to the extra information we need to complete the object

    return valid_players,player_by_id

def to_player(static_info :StaticPlayer,endpoint_info : IndexPlayer ) -> Player:
    """ Creates player objects for each properly validated player"""
    return Player(
        player_id = static_info.player_id,
        name = static_info.name,
        position = endpoint_info.position,
        current_team_id = endpoint_info.current_team_id if endpoint_info.current_team_id != 0 else None
    )
  


def load_players() -> None:
    """ This Function fully loads players, from fethcing to validation to the database """

    players_data = fetchplayers()
    static_info_total = players_data[0]
    endpoint_info_total = players_data[1]
    valid_players_data = validateplayers(static_info_total,endpoint_info_total)
    static_valid = valid_players_data[0]
    endpoint_valid = valid_players_data[1]

    with Session(engine) as session,session.begin():
        for player in static_valid:
            endpoint_info = endpoint_valid.get(player.player_id)
            if endpoint_info is None:
                print(f"Warning: No PLayerIndex info for {player.name}({player.player_id}),skipping")
                continue 
            session.merge(to_player(static_info=player,endpoint_info=endpoint_info))

    print("Players Saved")

if __name__ == "__main__":
    load_players()