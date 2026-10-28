from django.conf import settings
from django.db import models
from sports.models import Sport, MatchRulesMixin
from competitions.models import Competition, CompetitionStage, StageGroup, KnockoutTie

class Venue(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    photo = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Match(MatchRulesMixin):
    class Status(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        LIVE = 'LIVE', 'Live'
        FINISHED = 'FINISHED', 'Finished'
        POSTPONED = 'POSTPONED', 'Postponed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    sport = models.ForeignKey(Sport, on_delete=models.PROTECT, related_name='matches')
    competition = models.ForeignKey(Competition, on_delete=models.PROTECT, null=True, blank=True, related_name='matches')
    
    # v3.0 Stage structure references (replaces old free-text stage_label)
    stage = models.ForeignKey(CompetitionStage, on_delete=models.PROTECT, null=True, blank=True, related_name='matches')
    group = models.ForeignKey(StageGroup, on_delete=models.PROTECT, null=True, blank=True, related_name='matches')
    knockout_tie = models.ForeignKey(KnockoutTie, on_delete=models.PROTECT, null=True, blank=True, related_name='matches')
    leg_number = models.SmallIntegerField(null=True, blank=True, choices=[(1, '1'), (2, '2')])

    home_team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='home_matches')
    away_team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='away_matches')
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='matches')
    
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SCHEDULED)
    
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    home_shootout_score = models.IntegerField(null=True, blank=True)
    away_shootout_score = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Matches'
        constraints = [
            # v3.0 Addendum check: exactly one of group_id/knockout_tie_id set whenever stage_id is set; 
            # both NULL when stage_id is NULL
            models.CheckConstraint(
                condition=(
                    models.Q(stage__isnull=True, group__isnull=True, knockout_tie__isnull=True) |
                    models.Q(stage__isnull=False, group__isnull=False, knockout_tie__isnull=True) |
                    models.Q(stage__isnull=False, group__isnull=True, knockout_tie__isnull=False)
                ),
                name="match_stage_group_tie_mutually_exclusive",
            )
        ]

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.scheduled_at.strftime('%Y-%m-%d %H:%M')})"


class MatchClock(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='clock')
    period_label = models.CharField(max_length=50, default='1st Half')
    clock_seconds = models.IntegerField(default=0)
    is_running = models.BooleanField(default=False)
    stoppage_seconds = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Clock for Match #{self.match.id} - {self.period_label} ({self.clock_seconds}s)"


class MatchReporter(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='reporters')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_matches')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('match', 'user')

    def __str__(self):
        return f"{self.user.username} on Match #{self.match.id}"


class LineupEntry(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='lineups')
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='lineup_entries')
    player = models.ForeignKey('teams.Player', on_delete=models.CASCADE, related_name='match_appearances')
    position = models.ForeignKey('sports.Position', on_delete=models.PROTECT)
    jersey_number = models.PositiveIntegerField()
    is_starter = models.BooleanField(default=True)

    class Meta:
        unique_together = ('match', 'player')

    def __str__(self):
        role = "Starter" if self.is_starter else "Substitute"
        return f"{self.player} ({self.team}) - {role}"


class MatchEvent(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='events')
    event_type = models.ForeignKey('sports.EventType', on_delete=models.PROTECT)
    team = models.ForeignKey('teams.Team', on_delete=models.PROTECT)
    player = models.ForeignKey('teams.Player', on_delete=models.PROTECT, related_name='events_against')
    related_player = models.ForeignKey('teams.Player', on_delete=models.PROTECT, null=True, blank=True, related_name='events_assisted')
    
    period = models.CharField(max_length=50)
    clock_seconds = models.IntegerField()
    stoppage_offset_seconds = models.IntegerField(default=0)
    is_voided = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "[VOIDED] " if self.is_voided else ""
        return f"{status}{self.event_type.name} by {self.player} at {self.clock_seconds}s"