from django.db import models


"""
class NBATeamMembership(models.Model):
    player = models.ForeignKey('NBAPlayer', on_delete=models.CASCADE, related_name='team_memberships', related_query_name='team_membership')
    team = models.ForeignKey('NBATeam', on_delete=models.PROTECT, related_name='player_memberships', related_query_name='player_membership')

    start_date = models.DateField(default='2020-12-22')
    end_date = models.DateField(blank=True, null=True)

    def clean(self):
        # TODO: implement logic to prevent overlapping dates
"""