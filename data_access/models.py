"""Class for defining the classes that define all the data tables and classes for model"""
from typing import Optional
from datetime import date
from sqlalchemy import  FLOAT, ForeignKey,String,SMALLINT
from sqlalchemy import Date
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column, relationship

class Base(DeclarativeBase):
    "Base class for tables, gives access to the methods we need from SQLAlchemy"


class Team(Base):
    " Table Representing NBA Teams and all related info "
    __tablename__ = "team"
    team_id : Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(100))
    abbreviation : Mapped[str] = mapped_column(String(20),unique=True)
    conference :Mapped[str] = mapped_column(String(20))
    division : Mapped[str] = mapped_column(String(30))
    players : Mapped[list["Player"]] = relationship(back_populates="current_team")
    player_game_stats : Mapped[list["PlayerGameStats"]] = relationship(back_populates="team")

class Player(Base):
    "Table representing NBA Players and all related info"
    __tablename__ = "player"
    player_id : Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(100))
    position:Mapped[str | None] = mapped_column(String(50))
    current_team:Mapped["Team"] = relationship(back_populates="players")
    current_team_id :Mapped[int|None] = mapped_column(ForeignKey("team.team_id"))
    current_team_name : Mapped[str | None] = mapped_column(String(100))
    player_stats : Mapped[list["PlayerGameStats"]] = relationship(back_populates="player")

class Game(Base):
    "Table representing Individual NBA Games and all related info"
    __tablename__ = "game"
    game_id: Mapped[str] = mapped_column(String(100),primary_key=True)
    game_date:Mapped[date] = mapped_column(Date)
    season : Mapped[str] = mapped_column(String(30))
    home_team_name : Mapped[str] = mapped_column(String(100))
    home_team_id: Mapped[int] = mapped_column(ForeignKey("team.team_id"))
    away_team_id : Mapped[int] = mapped_column(ForeignKey("team.team_id"))
    away_team_name : Mapped[str] = mapped_column(String(100))
    home_final_score : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    away_final_score : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    game_status : Mapped[str] = mapped_column(String(40))
    player_stats : Mapped[list["PlayerGameStats"]] = relationship(back_populates= "game")
    season_type : Mapped[str] = mapped_column(String(50))

class PlayerGameStats(Base):
    "Class for Individual Team and Game Statistics"
    __tablename__ = "player_single_game_stats"
    player_id : Mapped[int] = mapped_column(ForeignKey("player.player_id"),primary_key=True)
    ##REVIST THIS
    player : Mapped["Player"] = relationship(back_populates="player_stats")
    ##HERE
    team_id : Mapped[int] = mapped_column(ForeignKey("team.team_id"))
    team : Mapped["Team"] = relationship(back_populates="player_game_stats")
    game_id : Mapped[str] = mapped_column(ForeignKey("game.game_id"),primary_key=True)
    game : Mapped["Game"] = relationship(back_populates="player_stats")
    ## STATS START HERE
    points : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    assists : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    total_rebounds : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    field_goals_attempted : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    field_goals_made : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    three_pointers_made : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    three_pointers_attempted : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    minutes : Mapped[Optional[float]] = mapped_column(FLOAT,nullable=True)
    free_throws_made : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    free_throws_attempted : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    steals : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    blocks : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    offensive_rebounds : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    defensive_rebounds : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    turnovers : Mapped[Optional[int]] = mapped_column(SMALLINT,nullable=True)
    ##Small Note
    status: Mapped[str] = mapped_column(String(50))
