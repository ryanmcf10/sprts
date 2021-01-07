import json
from datetime import datetime

from django.db import models

from nba_api.stats.endpoints import CommonPlayerInfo

from shared.models import BasePlayer
from shared.utils.string import xstr


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

    def get_current_team_membership(self):
        """
        Return this player's current NBATeamMembership, if any
        :return:
        """
        if self.team_memberships.count() == 0:
            return None

        return self.team_memberships.get(end_date=None)

    def get_current_team(self):
        """
        Return this player's current NBATeam, if any
        :return:
        """
        current_team_membership = self.get_current_team_membership()

        return current_team_membership.team if current_team_membership is not None else None

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

        self.first_name = xstr(data['FIRST_NAME'])
        self.last_name = xstr(data['LAST_NAME'])

        self.height = self.convert_height_to_inches(data['HEIGHT'])
        self.weight = int(data['WEIGHT'])

        self.birth_date = datetime.strptime(
            data['BIRTHDATE'].split('T')[0],
            '%Y-%m-%d'
        )

        self.number = xstr(data['JERSEY'])

        self.position_1, self.position_2 = self.get_standardized_positions(data['POSITION'])

        self.country = xstr(data['COUNTRY'])
        self.school = xstr(data['SCHOOL'])

    def convert_height_to_inches(self, height):
        feet, inches = height.split("-")

        height = 12 * int(feet) + int(inches)

        return height

    def get_standardized_positions(self, position_string):
        positions = position_string.split("-")

        standardized_positions = {
            'Center': 'C',
            'Forward': 'F',
            'Guard': 'G'
        }

        position_1 = standardized_positions[positions[0]]
        position_2 = standardized_positions[positions[1]] if len(positions) > 1 else ''

        return position_1, position_2
