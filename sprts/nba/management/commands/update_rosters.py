import time
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from halo import Halo

from nba.models import NBAPlayer, NBATeam, NBATeamMembership
from nba.utils.fetch import fetch_roster

DELAY = 1 # time to wait between API requests, in seconds


class Command(BaseCommand):
    help = 'Fetch the latest Team Rosters from NBA API and update'

    NEW_PLAYERS = 0
    PLAYERS_MOVED = 0

    def handle(self, *args, **options):
        # set all players to inactive. Activate them when they are found on a roster
        NBAPlayer.objects.update(is_active=False)


        print("Updating rosters...")

        for team in NBATeam.objects.all():
            spinner = Halo(text=str(team), spinner='dots')

            spinner.start()
            self.update_roster(team)
            spinner.succeed()

            time.sleep(DELAY)

        print("Done.")
        print(f"{self.NEW_PLAYERS} new player" + ("s" if self.NEW_PLAYERS != 1 else "") + "found.")
        print(f"{self.PLAYERS_MOVED} player" + ("s" if self.PLAYERS_MOVED != 1 else "") + " moved to new teams.")


    def update_roster(self, team):
        roster = fetch_roster(team)

        for raw_player in roster:
            nba_api_id = raw_player['PLAYER_ID']

            try:
                player = NBAPlayer.objects.get(nba_api_id=nba_api_id)
                #print(f"Found {player}")

            except NBAPlayer.DoesNotExist:
                #print(f"Could not find {raw_player['PLAYER']} [ {raw_player['PLAYER_ID']}]")
                self.NEW_PLAYERS += 1

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
                    self.PLAYERS_MOVED += 1

                NBATeamMembership.objects.create(
                    player=player,
                    team=team
                )

            player.save()
