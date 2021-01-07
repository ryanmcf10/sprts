import json, time
from datetime import date

from django.core.management.base import BaseCommand

from nba_api.stats.endpoints import CommonTeamRoster

from nba.models import NBAPlayer, NBATeam

DELAY = 2 # time to wait between API requests, in seconds


class Command(BaseCommand):
    help = 'Fetch the latest Team Rosters from NBA API and update'

    def handle(self, *args, **options):
        # set all players to inactive. Activate them when they are found on a roster
        NBAPlayer.objects.update(is_active=False)

        for team in NBATeam.objects.all():
            print(f"{time.strftime('%X')}: {team}")
            self.update_roster(team)

            time.sleep(DELAY)

    def update_roster(self, team):
        json_roster = self.fetch_json_roster(team)
        roster_data = self.parse_json_roster(json_roster)

        players = roster_data['CommonTeamRoster']
        self.update_players(players, team)

    def update_players(self, players, team):
        for raw_player in players:
            nba_api_id = raw_player['PLAYER_ID']

            try:
                player = NBAPlayer.objects.get(nba_api_id=nba_api_id)
                print(f"Found {player}")

            except NBAPlayer.DoesNotExist:
                print(f"Could not find {raw_player['PLAYER']} [ {raw_player['PLAYER_ID']}]")
                player = NBAPlayer(nba_api_id=nba_api_id)
                time.sleep(DELAY)
                player.fetch_and_update_player_info()

            self.update_player(player, team)

    def update_player(self, player, team):
        # check team matches player current team membership
        # update if need to
        pass

    def fetch_json_roster(self, team):
        """
        Request today's roster using NBA API and return it as 'messy' JSON.
        :param team: NBATeam
        :return:
        """
        raw_roster = CommonTeamRoster(team.nba_api_id)

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