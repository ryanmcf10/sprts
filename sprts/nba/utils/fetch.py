import json
from datetime import date, datetime

from nba_api.stats.endpoints import CommonTeamRoster, CommonPlayerInfo, TeamGameLog, PlayerGameLog, PlayByPlayV2


def fetch_team_gamelog(game, team):
    """
    Fetch the gamelog for a specific 'team' and a specific 'game'.
    :param game:
    :param team:
    :return:
    """
    if game.date >= date.today():
        raise Exception(f"Cannot fetch gamelog for a future game. Game is scheduled for {str(game.date)}.")

    data = json.loads(
        TeamGameLog(
            season='2020-21',
            season_type_all_star='Regular Season',
            team_id=team.nba_api_id,
            date_from_nullable=datetime.strftime(game.date, '%m/%d/%Y'),
            date_to_nullable=datetime.strftime(game.date, '%m/%d/%Y')
        ).get_json()
    )['resultSets'][0]

    return dictzip(data)


def fetch_player_info(player):
    """
    Fetch biographical info for the given 'player'.
    :param player:
    :return:
    """
    data = json.loads(
        CommonPlayerInfo(player_id=player.nba_api_id).get_json()
    )['resultSets'][0]

    return dictzip(data)


def fetch_player_gamelog(game, player):
    """
    Fetch the gamelog for a specific 'player' and a specific 'game'.
    :param game:
    :param player:
    :return:
    """
    data = json.loads(
        PlayerGameLog(
            season='2020-21',
            season_type_all_star='Regular Season',
            player_id=player.nba_api_id,
            date_from_nullable=datetime.strftime(game.date, '%m/%d/%Y'),
            date_to_nullable=datetime.strftime(game.date, '%m/%d/%Y')
        ).get_json()
    )['resultSets'][0]

    return dictzip(data)


def fetch_roster(team):
    """
    Fetch current roster for given 'team'.
    :param team:
    :return:
    """
    data = json.loads(
        CommonTeamRoster(
            team.nba_api_id
        ).get_json()
    )['resultSets'][0]

    return dictzip(data)

def fetch_play_by_play(game):
    """
    Fetch the play-by-play data for the given 'game'.
    :param game:
    :return:
    """
    data = json.loads(
        PlayByPlayV2(
            game_id=game.nba_api_id,
            start_period=1,
            end_period=10
        ).get_json()
    )['resultSets'][0]

    return dictzip(data)


def dictzip(data):
    """
    Take the messy data return from nba_api and attempt to return it as either a dictionary like:

    {
        header_1: value_1,
        header_2: value_2,
        ...
        header_n: value_n
    }

    or a list of such dictionaries.

    :param data:
    :return:
    """
    result = None

    if len(data['rowSet']) == 0:
        raise Exception("No data found.")

    if len(data['rowSet']) == 1:
        result = dict(
            zip(
                data['headers'],
                data['rowSet'][0]
            )
        )

    elif len(data['rowSet']) > 1:
        result = [
            dict(
                zip(
                    data['headers'],
                    data['rowSet'][i]
                )
            ) for i in range(len(data['rowSet']))
        ]

    return result
