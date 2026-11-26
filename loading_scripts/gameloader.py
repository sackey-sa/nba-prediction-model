""" Script For loading all game objects into MYSQL Database"""
from typing import Any
from sqlalchemy.orm import Session
from nba_api.stats.endpoints import teamgamelogs  #type: ignore[import-untyped]
from data_access.database import engine
from data_access.dataschema import GameLogRow
from data_access.models import Game

SEASON = "2026-27"
SEASON_TYPE = "Regular Season"
STATUS = "FINISHED"

def fetch_games() -> dict[str,Any]:
    """ Function grabs initial game info from API"""

    game_info = teamgamelogs.TeamGameLogs(season_nullable=SEASON,
                                          season_type_nullable=SEASON_TYPE).get_normalized_dict()
    game_info_rows = game_info["TeamGameLogs"]

    game_by_id: dict[str,list[dict[str,Any]]] = {}

    for row in game_info_rows:
        game_id = row["GAME_ID"]

        if game_id not  in game_by_id:
            game_by_id[game_id] = []

        game_by_id[game_id].append(row)

    return game_by_id


def validate_game(game_teams:dict[str,Any])-> dict[str,tuple[GameLogRow,GameLogRow]]:
    """ Function transforms game info into structured pydantic objects"""
    valid_games = {}
    for game_id in game_teams:
        home_game = None
        away_game = None
        game_list = game_teams[game_id] ## Gives me the perspectives PER GAME
        for game in game_list:
            if  "vs." in game["MATCHUP"]:
                home_game = GameLogRow.model_validate(game)

            elif "@" in game["MATCHUP"]:
                away_game = GameLogRow.model_validate(game)
        if home_game is None or away_game is None  :
            print(f"No Matchup Info Found for {game_id},skipping")
            continue
        valid_games[game_id] = (home_game,away_game)

    return valid_games

def to_game(home_game:GameLogRow,away_game:GameLogRow) -> Game:
    """ Function that creates the database objects properly"""
    return Game(
        game_id = home_game.game_id,
        game_date = home_game.game_date,
        season = SEASON,
        home_team_id = home_game.team_id,
        home_team_name = home_game.team_name,
        away_team_id = away_game.team_id,
        away_team_name = away_game.team_name,
        home_final_score = home_game.final_score,
        away_final_score = away_game.final_score,
        game_status = STATUS,
        season_type = SEASON_TYPE
    )

def load_games() -> None:
    "Actually loads game values into database from API and helper functions to validate"

    game_data = fetch_games()
    validated_games = validate_game(game_data)

    with Session(engine) as session,session.begin():
        for home_game,away_game in validated_games.values():
            session.merge(to_game(home_game,away_game))
        print("Games Saved")


if __name__ == "__main__":
    load_games()
