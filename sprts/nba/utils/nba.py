import json
from datetime import date, datetime

from nba_api.stats.endpoints import TeamGameLog


def fetch_team_gamelog(game, team):
    if game.date >= date.today():
        raise Exception(f"Cannot fetch gamelog for a future game. Game is scheduled for {str(game.date)}.")

    data = json.loads(
        TeamGameLog(
            season = '2020-21',
            season_type_all_star='Regular Season',
            team_id = team.nba_api_id,
            date_from_nullable = datetime.strftime(game.date, '%m/%d/%Y'),
            date_to_nullable = datetime.strftime(game.date, '%m/%d/%Y')
        ).get_json()
    )['resultSets'][0]

    try:
        return dict(
            zip(
                data['headers'],
                data['rowSet'][0] # Values, if they exist. If nothing here, no game was played by 'team' on 'game.date'.
            )
        )
    except IndexError:
        raise Exception(f"No gamelog data found for {team} on {game.date}. Was the game postponed?")