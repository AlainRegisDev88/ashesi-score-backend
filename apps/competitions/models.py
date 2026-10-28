from django.db import models
from sports.models import Sport

class Competition(models.Model):
    class CompetitionType(models.TextChoices):
        LEAGUE = 'LEAGUE', 'League'
        CUP = 'CUP', 'Cup'

    class Status(models.TextChoices):
        UPCOMING = 'UPCOMING', 'Upcoming'
        ONGOING = 'ONGOING', 'Ongoing'
        COMPLETED = 'COMPLETED', 'Completed'

    name = models.CharField(max_length=150)
    sport = models.ForeignKey(Sport, on_delete=models.PROTECT, related_name='competitions')
    competition_type = models.CharField(max_length=6, choices=CompetitionType.choices, default=CompetitionType.LEAGUE)
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.UPCOMING)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Rules block snapshot settings
    points_for_win = models.IntegerField(default=3)
    points_for_draw = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.sport.name})"


class CompetitionTeam(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='competition_teams')
    team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='registered_competitions')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('competition', 'team')

    def __str__(self):
        return f"{self.team.name} in {self.competition.name}"


class RankingRule(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='ranking_rules')
    priority = models.SmallIntegerField()
    criterion = models.CharField(max_length=50) # e.g., 'POINTS', 'GOAL_DIFFERENCE', 'HEAD_TO_HEAD'

    class Meta:
        ordering = ['priority']
        unique_together = ('competition', 'priority')


class CompetitionStage(models.Model):
    class StageType(models.TextChoices):
        GROUP = "GROUP", "Group"
        KNOCKOUT = "KNOCKOUT", "Knockout"

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="stages")
    name = models.CharField(max_length=50)  # e.g., "Group Stage", "Quarter-final", "Final"
    stage_type = models.CharField(max_length=9, choices=StageType.choices)
    sequence = models.SmallIntegerField()
    two_legged = models.BooleanField(default=False)

    class Meta:
        unique_together = (("competition", "sequence"), ("competition", "name"))
        ordering = ['sequence']

    def __str__(self):
        return f"{self.competition.name} - {self.name}"


class StageGroup(models.Model):
    stage = models.ForeignKey(CompetitionStage, on_delete=models.CASCADE, related_name="groups")
    name = models.CharField(max_length=20)  # e.g., "Group A"

    class Meta:
        unique_together = ("stage", "name")

    def __str__(self):
        return f"{self.stage.name} - {self.name}"


class StageGroupTeam(models.Model):
    group = models.ForeignKey(StageGroup, on_delete=models.CASCADE, related_name="group_teams")
    team = models.ForeignKey("teams.Team", on_delete=models.PROTECT, related_name="group_stages")

    class Meta:
        unique_together = ("group", "team")

    def __str__(self):
        return f"{self.team.name} in {self.group}"


class KnockoutTie(models.Model):
    class AdvancesToSlot(models.TextChoices):
        HOME = "HOME", "Home"
        AWAY = "AWAY", "Away"

    stage = models.ForeignKey(CompetitionStage, on_delete=models.CASCADE, related_name="knockout_ties")
    slot = models.SmallIntegerField()
    home_team = models.ForeignKey("teams.Team", on_delete=models.PROTECT, null=True, blank=True, related_name="knockout_home_ties")
    away_team = models.ForeignKey("teams.Team", on_delete=models.PROTECT, null=True, blank=True, related_name="knockout_away_ties")
    winner_team = models.ForeignKey("teams.Team", on_delete=models.PROTECT, null=True, blank=True, related_name="knockout_wins")
    advances_to_tie = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="previous_ties")
    advances_to_slot = models.CharField(max_length=4, choices=AdvancesToSlot.choices, null=True, blank=True)

    class Meta:
        unique_together = ("stage", "slot")
        constraints = [
            models.CheckConstraint(
                check=models.Q(advances_to_tie__isnull=True) | models.Q(advances_to_slot__isnull=False),
                name="advances_to_slot_required",
            )
        ]

    def __str__(self):
        return f"{self.stage.name} - Tie #{self.slot}"