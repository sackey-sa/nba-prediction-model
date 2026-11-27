""" Loads individual player data into database"""
from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from nba_api.stats.endpoints import playergamelogs  #type: ignore[import-untyped]
from data_access.database import engine
from data_access.dataschema import PlayerLogRow
from data_access.models import PlayerGameStats,Player,Game


STATUS = "FINISHED"
SEASON_TYPE = "Regular Season"

def fetch_player_game_data(season:str) -> list[dict[str,Any]]:
    """ Function fetches individual player/game stats"""
    player_game_data = playergamelogs.PlayerGameLogs(season_nullable=season,
                                                     timeout=50,
                                                     season_type_nullable=
                                                     SEASON_TYPE).get_normalized_dict()
    player_rows: list[dict[str,Any]] = player_game_data["PlayerGameLogs"]
    return player_rows

def validate_player_game_data(player_rows : list[dict[str,Any]]) -> list[PlayerLogRow]:
    """ Function Validates each row and saves only the data I need"""

    player_game_valid = [PlayerLogRow.model_validate(p) for p in player_rows]

    return player_game_valid

def to_player_game(player_game:PlayerLogRow) -> PlayerGameStats:
    """ Function creates a playergamestats objects"""
    return PlayerGameStats(
        player_id = player_game.player_id,
        team_id = player_game.team_id,
        game_id = player_game.game_id,
        points = player_game.pts,
        assists = player_game.ast,
        total_rebounds = player_game.total_rebounds,
        field_goals_attempted = player_game.fga,
        field_goals_made = player_game.fgm,
        three_pointers_made = player_game.threepm,
        three_pointers_attempted = player_game.threepa,
        minutes = player_game.min,
        free_throws_made = player_game.ftm,
        free_throws_attempted = player_game.fta,
        steals = player_game.steals,
        blocks = player_game.blocks,
        offensive_rebounds = player_game.off_rebounds,
        defensive_rebounds = player_game.def_rebounds,
        turnovers = player_game.turnovers,
        status = STATUS)

def load_player_game_info(season:str) -> None:
    """ This function loads the database with actual data from the api """

    data = fetch_player_game_data(season)
    validated_data = validate_player_game_data(data)

    with Session(engine) as session, session.begin():
        players_added = 0
        game_id_count = set()
        known_ids = set(session.scalars(select(Player.player_id)))
        known_game_ids = set(session.scalars(select(Game.game_id)))
        for player_info in validated_data:
            if player_info.player_id not in known_ids:
                session.merge(to_minimum_player(player_info))
                known_ids.add(player_info.player_id)
                players_added += 1
            if player_info.game_id not in known_game_ids:
                game_id_count.add(player_info.game_id)
                print(game_id_count)
                continue
            session.merge(to_player_game(player_info))
    print(f"Individual Game Focused Player Data SAVED ,missed games : {game_id_count},players added {players_added}")


def to_minimum_player(row:PlayerLogRow) -> Player:
    """ Fills Gaps of Players unsaved"""
    return Player(
        player_id = row.player_id,
        name = row.player_name,
        position = None,
        current_team_id = None,
        current_team_name = None)


if __name__ == "__main__":
    for year in ["2022-23","2023-24","2024-25","2025-26","2026-27"]:
        load_player_game_info(year)
