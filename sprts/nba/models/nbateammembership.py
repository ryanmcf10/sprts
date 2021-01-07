from django.db import models


class NBATeamMembership(models.Model):
    player = models.ForeignKey('NBAPlayer',
                               on_delete=models.CASCADE,
                               related_name='team_memberships',
                               related_query_name='team_membership')

    team = models.ForeignKey('NBATeam', on_delete=models.PROTECT,
                             related_name='player_memberships',
                             related_query_name='player_membership')

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "NBA Team Membership"
        verbose_name_plural = "NBA Team Memberships"

    def __str__(self):
        result =  f"{self.player} :: {self.team}"

        if self.end_date:
            result += f" [{self.start_date.year}-{self.end_date.year}]"
        else:
            result += f" [{self.start_date.year}-Pres.]"

        return result
