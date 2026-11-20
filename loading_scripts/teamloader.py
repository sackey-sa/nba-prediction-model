""" This file loads the team objects into the database from API data """
from typing import Any
from sqlalchemy.orm import Session
from nba_api.stats.endpoints import leaguestandings #type: ignore[import-untyped]
from nba_api.stats.static import teams #type: ignore[import-untyped]
from data_access.database import engine
from data_access.dataschema import StaticTeam,StandingsTeam
from data_access.models import Team



## Request FOR NBA TEAMS FIRST, INCLUDING FUNCTION TO TEAM

SEASON = "2026-27"

def fetch_teams()-> tuple[list[dict[str,Any]],dict[str,Any]]:
    """ Request both sources and return the raw rows"""
    static_teams = teams.get_teams()
    standings_data = leaguestandings.LeagueStandings(season=SEASON,season_type="Regular Season",
                                                        timeout=30).get_normalized_dict()
    return static_teams,standings_data



def validate_teams(static_teams:list[dict[str,Any]],
                   standings_data:dict[str,Any]) -> tuple[list[StaticTeam],
                                                          dict[int,StandingsTeam]]:
    """ This function essentially takes the raw dict data
    and creates instances of our validated Pydantic Models"""
    static_valid = [StaticTeam.model_validate(team) for team in static_teams]
    standings_rows = standings_data["Standings"]
    standings_valid = [StandingsTeam.model_validate(r) for r in standings_rows]
    standings_by_id = {s.team_id:s for s in standings_valid}

    return static_valid,standings_by_id



def to_team(static:StaticTeam , standing:StandingsTeam) -> Team:
    """ Function Creates a team object from API information, 
    combined static and standings info(Division,Conference)"""
    return Team(
            team_id = static.id,
            name = static.full_name,
            abbreviation = static.abbreviation,
            conference = standing.conference,
            division = standing.division
       )

def load_teams()-> None:
    """ This function takes completes the databse loading in one function. 
    From API call to Validation to Saving"""

    data = fetch_teams()
    static_team_data = data[0]
    standing_team_data = data[1]

    validated_data = validate_teams(static_team_data,standing_team_data)
    static_valid = validated_data[0]
    standing_by_id = validated_data[1]

    with Session(engine) as session,session.begin():
        for static in static_valid:
            standing = standing_by_id.get(static.id)
            if standing is None:
                raise ValueError(f"No conference INFO found for {static.full_name}")
            session.merge(to_team(static=static,standing=standing))

    print("Teams Saved")


if __name__ == "__main__":
    load_teams()
