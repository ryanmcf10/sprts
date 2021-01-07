import json
from datetime import datetime

from django.db import models

from nba_api.stats.endpoints import CommonPlayerInfo

from shared.models import BasePlayer


class NBAPlayer(BasePlayer):
    """A player in the NBA"""
    nba_api_id = models.CharField(max_length=12, unique=True, editable=False)
    is_active = models.BooleanField(default=True)

    number = models.CharField(max_length=2, blank=True)
    position_1 = models.CharField(max_length=2, blank=True)
    position_2 = models.CharField(max_length=2, blank=True)

    school = models.TextField(blank=True)
    country = models.TextField(blank=True)

    height = models.PositiveSmallIntegerField(null=True)
    weight = models.PositiveSmallIntegerField(null=True)

    def fetch_and_update_player_info(self):
        json_data = json.loads(
            CommonPlayerInfo(player_id=self.nba_api_id).nba_response.get_json()
        )

        data = dict(
            zip(
                json_data['resultSets'][0]['headers'],
                json_data['resultSets'][0]['rowSet'][0]
            )
        )

        self.first_name = data['FIRST_NAME']
        self.last_name = data['LAST_NAME']

        self.height = self.convert_height_to_inches(data['HEIGHT'])
        self.weight =  int(data['WEIGHT'])

        self.birth_date = datetime.strptime(
            data['BIRTHDATE'].split('T')[0],
            '%Y-%m-%d'
        )

    def convert_height_to_inches(self, height):
        feet, inches = height.split("-")

        height = 12*int(feet) + int(inches)

        return height
