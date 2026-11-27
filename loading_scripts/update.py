""" File Responscibile for updating database Information"""
import time
from loading_scripts.gameloader import load_games
from loading_scripts.playerloader import load_players
from loading_scripts.playergameloader import load_player_game_info

CURRENT_SEASON = "2026-27"
def update_database() -> None:
    """ Update Database with most recent data"""
    load_players(CURRENT_SEASON)
    time.sleep(3)
    load_games(CURRENT_SEASON)
    time.sleep(3)
    load_player_game_info(CURRENT_SEASON)
    print("Update Complete")



if __name__ == "__main__" :
    update_database()
