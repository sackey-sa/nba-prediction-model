# NBA Predictive Model

A personal project for collecting NBA data, building predictive models on it, and eventually exploring the results through a small web app.

> **Status:** Work in progress. The database schema is in place; data loading is underway. Modeling and the web app come next.

## Overview

The project pulls game-level data from the NBA stats API and stores it in a relational database using SQLAlchemy. Stats are stored per player, per game, and aggregates such as points per game, team records, and head-to-head results are computed from that data on demand. This keeps the data accurate as new games are played and allows features to be built from only the games before the one being predicted, avoiding data leakage.

## Tech Stack

- **Python**
- **SQLAlchemy** (ORM) with **SQLite** (MySQL/Postgres supported by changing the connection string)
- **requests** / **nba_api** for data collection
- **pandas** for analysis and feature engineering

## Data Model

| Table | Description |
|---|---|
| `team` | Name, abbreviation, conference, division |
| `player` | Name, position, current team |
| `game` | Date, season, season type, home/away teams, final scores, status |
| `player_single_game_stats` | One row per player per game: points, assists, rebounds, shooting, minutes, and more |

Each player stat row records the team the player was on for that game, so history is preserved across trades.

## Getting Started

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Then create the tables and load data:

```bash
python <create_tables_script>.py
python <load_data_script>.py
```

Data is loaded in dependency order (teams → players → games → player stats). Raw API responses are cached locally so loads can be rerun without re-requesting data.

## Roadmap

- [x] Define database schema
- [ ] Load historical seasons
- [ ] Daily updates for new games
- [ ] Feature engineering (rolling averages, rest days, home/away splits)
- [ ] Train and evaluate predictive models
- [ ] Web app for exploring stats and predictions

## Disclaimer

This is a personal, non-commercial project and is not affiliated with or endorsed by the NBA. Data is retrieved from publicly accessible NBA stats endpoints; please respect their rate limits.
