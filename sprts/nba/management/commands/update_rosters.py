import json, asyncio, time
from datetime import date

from django.core.management.base import BaseCommand

from nba_api.stats.endpoints import commonteamroster

from nba.models import NBAPlayer, NBATeam


class Command(BaseCommand):
    help = 'Fetch the latest Team Rosters from NBA API and update'
    
    def handle(self, *args, **options):
        for team in NBATeam.objects.all():
            print(f"{time.strftime('%X')}: {team}")
            asyncio.run(self.update_roster_with_delay(team))


    async def update_roster_with_delay(self, team, delay=2):
        """
        Update the rosters for the given team, in at most 2 seconds.

        Built-in delay prevents requests to the API from being blocked.
        :param team: NBATeam
        :param delay: minimum number of seconds method should take to complete
        :return:
        """
        await self.update_roster(team)
        await asyncio.sleep(delay)

    async def update_roster(self, team):
        json_roster = self.fetch_json_roster(team)
        roster_data = self.parse_json_roster(json_roster)

        players = roster_data['CommonTeamRoster']

        for player in players:
            print(player['PLAYER'])
        #for k, v in player.items():
        #    print(k, v)

    def fetch_json_roster(self, team):
        raw_roster = commonteamroster.CommonTeamRoster(team.nba_api_id)

        json_roster = json.loads(raw_roster.nba_response.get_json())

        return json_roster


    def parse_json_roster(self, json_roster):
        """
        crazy comprehensions to get a dictionary like:

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
