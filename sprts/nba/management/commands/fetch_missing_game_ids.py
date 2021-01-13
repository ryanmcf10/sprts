import json, time

from django.core.management.base import BaseCommand

from nba_api.stats.endpoints import ScoreboardV2

from nba.models import NBAGame

DELAY = 1  # time to wait between API requests, in seconds


class Command(BaseCommand):
    help = "Attempt to find the NBA API Game ID for every games stored in the local database."

    def handle(self, *args, **options):

        for date in NBAGame.objects\
                .filter(nba_api_id='')\
                .order_by('date')\
                .values_list('date', flat=True)\
                .distinct():

            print(str(date))

            raw_game_data = json.loads(ScoreboardV2(
                game_date=str(date),
                day_offset=0,
                league_id='00'
            ).get_json())['resultSets'][0]

            game_data = []

            for raw_game in raw_game_data['rowSet']:
                game_data.append(
                    dict(zip(
                        raw_game_data['headers'],
                        raw_game
                    )),
                )

            for game in game_data:
                game_id = game['GAME_ID']
                home_team_id = str(game['HOME_TEAM_ID'])
                away_team_id = str(game['VISITOR_TEAM_ID'])

                print(date, home_team_id, away_team_id)

                try:
                    nba_game = NBAGame.objects.get(
                        date=date,
                        home_team__nba_api_id=home_team_id,
                        away_team_id__nba_api_id=away_team_id
                    )

                    nba_game.nba_api_id = game_id
                    nba_game.save()

                except NBAGame.DoesNotExist:
                    print("Game does not exist in database.")

            time.sleep(DELAY)
