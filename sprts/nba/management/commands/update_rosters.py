import time
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from nba.models import NBAPlayer, NBATeam, NBATeamMembership
from nba.utils.fetch import fetch_roster

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
        roster = fetch_roster(team)

        for raw_player in roster:
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
                    player_current_team_membership.end_date = date.today() - timedelta(days=1)
                    player_current_team_membership.save()

                NBATeamMembership.objects.create(
                    player=player,
                    team=team
                )

            player.save()
