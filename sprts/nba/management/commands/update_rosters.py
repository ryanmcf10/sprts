import json, time
from datetime import date

from django.core.management.base import BaseCommand

from nba_api.stats.endpoints import commonteamroster

from nba.models import NBAPlayer, NBATeam


class Command(BaseCommand):
    help = 'Fetch the latest Team Rosters from NBA API and update'

    def handle(self, *args, **options):
        for team in NBATeam.objects.all():
            print(f"{time.strftime('%X')}: {team}")
            self.update_roster(team)
            time.sleep(2)

    def update_roster(self, team):
        json_roster = self.fetch_json_roster(team)
        roster_data = self.parse_json_roster(json_roster)

        players = roster_data['CommonTeamRoster']
        self.update_players(players)

    def update_players(self, players):
        for raw_player in players:
            nba_api_id = raw_player['PLAYER_ID']

            try:
                player = NBAPlayer.objects.get(nba_api_id=nba_api_id)
                print(f"Found {player}")

            except NBAPlayer.DoesNotExist:
                print(f"Could not find {raw_player['PLAYER']}")
                player = NBAPlayer(nba_api_id=nba_api_id)
                player.fetch_player_info()

    def fetch_json_roster(self, team):
        """
        Request today's roster using NBA API and return it as 'messy' JSON.
        :param team: NBATeam
        :return:
        """
        raw_roster = commonteamroster.CommonTeamRoster(team.nba_api_id)

        json_roster = json.loads(raw_roster.nba_response.get_json())

        return json_roster


    def parse_json_roster(self, json_roster):
        """
        Clean up the 'messy' JSON returned from NBA API using some crazy list/dict comprehensions to get something more
        usable like:

        {
            'CommonTeamRoster': [
                { player_1 dictionary},
                { player_2 dictionary},
                ...
                { player_n dictionary},

            'Coaches': [
                { coach_1 dictionary},
                { coach_2 dictionary},
                ...
                { coach_n dictionary},
            ]
        }
        """

        return {
                    x['name']: [{
                            x['headers'][i]: player[i] for i in range(len(x['headers']))
                        } for player in x['rowSet']
                    ] for x in json_roster['resultSets']
                }

    def parse_player(self, player_dict):
        nba_api_id = player_dict['PLAYER_ID']
        team_nba_api_id = player_dict['TEAM_ID']
        name = player_dict['PLAYER']
        number = player_dict['NUM']
        position = player_dict['POSITION']
        height = player_dict['HEIGHT']
        weight = player_dict['WEIGHT']
        birth_date = player_dict['BIRTH_DATE']
