from django.db import models
from sports.models import MatchRulesMixin, Sport


class Competition(MatchRulesMixin):
    class CompetitionType(models.TextChoices):
        LEAGUE = "LEAGUE", "League"
        CUP = "CUP", "Cup"

    class Status(models.TextChoices):
        UPCOMING = "UPCOMING", "Upcoming"
        ONGOING = "ONGOING", "Ongoing"
        COMPLETED = "COMPLETED", "Completed"

    sport = models.ForeignKey(
        Sport, on_delete=models.PROTECT, related_name="coompetitions"
    )

    name = models.CharField(max_length=100)
    competition_type = models.CharField(
        max_length=6, choices=CompetitionType.choices, default=CompetitionType.LEAGUE
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=9, choices=Status.choices, default=Status.UPCOMING
    )

    points_for_the_win = models.SmallIntegerField(default=3)
    points_for_the_draw = models.SmallIntegerField(default=1)
    points_for_the_loss = models.SmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sport", "name"], name="unique_sport_competition"
            )
        ]

    def __str__(self):
        return f"{self.name}({self.sport.name})"


class CompetitionTeam(models.Model):
    competiton = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name="competitoin_teams"
    )
    team = models.ForeignKey(
        "team.Team", on_delete=models.PROTECT, related_name="competition_name"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["competition", "team"], name="unique_team_competition"
            )
        ]


class RankingRules(models.Model):
    class Criterion(models.TextChoices):
        POINTS = "POINTS", "Points"
        WINS = "WINS", "Wins"
        SCORE_DIFFERENCE = "SCORE_DIFFERENCE", "Score Difference"
        SCORE_FOR = "SCORE_FOR", "Score For"
        SCORE_AGAINST = "SCORE_AGAINST", "Score Against"
        HEAD_TO_HEAD_POINTS = "HEAD_TO_HEAD_POINTS", "Head-to-Head Points"
        HEAD_TO_HEAD_SCORE_DIFFERENCE = (
            "HEAD_TO_HEAD_SCORE_DIFFERENCE",
            "Head-to-Head Score Difference",
        )
        HEAD_TO_HEAD_SCORE_FOR = "HEAD_TO_HEAD_SCORE_FOR", "Head-to-Head Score For"

    sport = models.ForeignKey(
        Sport,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ranking_rules",
    )

    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ranking_rules",
    )

    priority = models.SmallIntegerField()
    criterion = models.CharField(max_length=40, choices=Criterion.choices)

    class Meta:
        constaints = [
            models.CheckConstraint(
                check=(
                    models.Q(sport__isnull=False, competition__sinull=True)
                    | models.Q(sport_isnull=True, competition_isnull=False)
                ),
                name="ranking_rule_exclusive_parent",
            )
        ]
