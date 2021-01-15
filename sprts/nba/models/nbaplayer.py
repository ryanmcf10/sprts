from datetime import date, datetime

from django.db import models
from django.db.models import Q

from nba.models.managers import NBAPlayerManager
from nba.utils.fetch import fetch_player_info
from shared.models import BasePlayer
from shared.utils.string import xstr
from shared.utils.conversions import string_height_to_inches, inches_to_string_height


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

    objects = NBAPlayerManager

    class Meta:
        verbose_name = 'NBA Player'
        verbose_name_plural = 'NBA Players'

    @property
    def string_height(self):
        return inches_to_string_height(self.height) if self.height else None

    def get_team_on_date(self, date):
        """
        Return this player's NBATeam on the given 'date', if any.
        :param date:
        :return:
        """
        team_membership = self.team_memberships.select_related('team').filter(start_date__lte=date)

        if team_membership.count() == 0:
            return None
        else:
            return team_membership.get(
                Q(end_date__isnull=True) |
                Q(end_date__gte=date)
            ).team

    def get_current_team(self):
        """
        Return this player's current NBATeam, if any.
        :return:
        """
        return self.get_team_on_date(date.today())

    def fetch_info(self):
        data = fetch_player_info(self)

        self.first_name = xstr(data['FIRST_NAME'])
        self.last_name = xstr(data['LAST_NAME'])

        self.height = string_height_to_inches(data['HEIGHT'])
        self.weight = int(data['WEIGHT'])

        self.birth_date = datetime.strptime(
            data['BIRTHDATE'].split('T')[0],
            '%Y-%m-%d'
        )

        self.number = xstr(data['JERSEY'])

        self.position_1, self.position_2 = get_standardized_positions(data['POSITION'])

        self.country = xstr(data['COUNTRY'])
        self.school = xstr(data['SCHOOL'])


def get_standardized_positions(position_string):
    positions = position_string.split("-")

    standardized_positions = {
        'Center': 'C',
        'Forward': 'F',
        'Guard': 'G'
    }

    position_1 = standardized_positions[positions[0]]
    position_2 = standardized_positions[positions[1]] if len(positions) > 1 else ''

    return position_1, position_2
