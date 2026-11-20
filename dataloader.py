""" This file creates the tables we defined in models """
from nba_api.stats.endpoints import playerindex,leaguestandings
from nba_api.stats.static import teams
from dataschema import StaticTeam,StandingsTeam
from models import Team
from sqlalchemy.orm import Session
from database import engine


## Request FOR NBA TEAMS FIRST, INCLUDING FUNCTION TO TEAM

SEASON = "2026-27"


static_teams = teams.get_teams()
standings_data = leaguestandings.LeagueStandings(season=SEASON,season_type="Regular Season",
                                                        timeout=30).get_normalized_dict()

## Since the API already handles the raw request and the sending of said request through an object, 
# its best we use that in this instance


static_valid = [StaticTeam.model_validate(t) for t in static_teams]
standings_rows = standings_data["Standings"]
standings_valid = [StandingsTeam.model_validate(r) for r in standings_rows]

standings_by_id = {s.team_id: s for s in standings_valid}



def to_team(static:StaticTeam,standing:StandingsTeam) -> Team:
    """ Function Creates a team object from API information, combined static and endpoint"""
    return Team(
        team_id = static.id,
        name = static.full_name,
        abbreviation = static.abbreviation,
        conference = standing.conference,
        division = standing.division,
    )


def load_teams()-> None:
    " Fetch,validate,convert, and save.The function to call "

    with Session(engine) as session,session.begin():
        for static in static_valid:
            standing = standings_by_id.get(static.id)
            if standing is None:
                raise ValueError(f"No standings found for {static.full_name}")
        session.merge(to_team(static,standing))
        
    print("Teams saved.")