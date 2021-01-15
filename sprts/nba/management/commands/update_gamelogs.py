import time
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from halo import Halo

from nba.models import NBAGame

DELAY = 1 # time to wait between API requests, in seconds


class Command(BaseCommand):
    help = 'Fetch the latest Team Rosters from NBA API and update'

    def handle(self, *args, **options):
        print("Updating gamelogs...")

        yesterdays_games = NBAGame.objects.filter(date=date.today() - timedelta(days=1))

        for game in yesterdays_games:
            spinner = Halo(text=str(game), spinner='dots')

            spinner.start()
            try:
                game.create_gamelogs()
                spinner.succeed()
            except Exception as e:
                spinner.fail()
                print(e)

            spinner.stop()

            time.sleep(1)

        print("Done.")