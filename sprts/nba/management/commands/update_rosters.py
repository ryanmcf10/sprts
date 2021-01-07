import json, time
from datetime import date

from django.core.management.base import BaseCommand

from nba_api.stats.endpoints import CommonTeamRoster

from nba.models import NBAPlayer, NBATeam, NBATeamMembership

DELAY = 1 # time to wait between API requests, in seconds


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

        for raw_player in players:
            nba_api_id = raw_player['PLAYER_ID']

            try:
                player = NBAPlayer.objects.get(nba_api_id=nba_api_id)
                print(f"Found {player}")

            except NBAPlayer.DoesNotExist:
                print(f"Could not find {raw_player['PLAYER']} [ {raw_player['PLAYER_ID']}]")

                player = NBAPlayer.objects.create(
                    nba_api_id=nba_api_id
                )

                time.sleep(DELAY)

                player.fetch_and_update_player_info()

            player.is_active = True
            player_current_team = player.get_current_team()

            # check if the player's current team matches this team
            # if it does not match, end their current team membership (if any), and create a new one
            if player_current_team is None or player_current_team != team:
                player_current_team_membership = player.get_current_team_membership()

                if player_current_team_membership is not None:
                    player_current_team_membership.end_date = date.today()
                    player_current_team_membership.save()

                NBATeamMembership.objects.create(
                    player=player,
                    team=team
                )

            player.save()


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