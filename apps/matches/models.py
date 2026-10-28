from django.conf import settings
from django.db import models
from competitions.models import Competition
from sports.models import EventType, MatchRulesMixin, Position, Sport
from teams.models import Player, Team


class Venue(models.Model):
  name = models.CharField(max_length=100, unique=True)
  slug = models.SlugField(max_length=120, unique=True)
  description = models.TextField(null=True, blank=True)
  capacity = models.IntegerField(null=True, blank=True)
  photo = models.CharField(max_length=255, null=True, blank=True)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.name


class Match(MatchRulesMixin):
  class Status(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    LIVE = "LIVE", "Live"
    FINISHED = "FINISHED", "Finished"
    POSTPONED = "POSTPONED", "Postponed"
    CANCELLED = "CANCELLED", "Cancelled"

  sport = models.ForeignKey(
      Sport, on_delete=models.PROTECT, related_name="matches"
  )
  competition = models.ForeignKey(
      Competition,
      on_delete=models.PROTECT,
      null=True,
      blank=True,
      related_name="matches",
  )  # NULL = friendly
  stage_label = models.CharField(max_length=50, null=True, blank=True)
  home_team = models.ForeignKey(
      Team, on_delete=models.PROTECT, related_name="home_matches"
  )
  away_team = models.ForeignKey(
      Team, on_delete=models.PROTECT, related_name="away_matches"
  )
  venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name="matches")
  scheduled_at = models.DateTimeField()
  status = models.CharField(
      max_length=10, choices=Status.choices, default=Status.SCHEDULED
  )
  started_at = models.DateTimeField(null=True, blank=True)
  finished_at = models.DateTimeField(null=True, blank=True)
  home_score = models.SmallIntegerField(default=0)
  away_score = models.SmallIntegerField(default=0)
  home_shootout_score = models.SmallIntegerField(null=True, blank=True)
  away_shootout_score = models.SmallIntegerField(null=True, blank=True)
  created_by = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.PROTECT
  )

  class Meta:
    constraints = [
        models.CheckConstraint(
            check=~models.Q(home_team=models.F("away_team")),
            name="match_different_teams",
        ),
        models.CheckConstraint(
            check=~models.Q(status="FINISHED")
            | models.Q(finished_at__isnull=False),
            name="match_finished_at_required",
        ),
    ]

  def __str__(self):
    return f"{self.home_team} vs {self.away_team} ({self.scheduled_at})"


class MatchClock(models.Model):
  match = models.OneToOneField(
      Match, on_delete=models.CASCADE, primary_key=True, related_name="clock"
  )
  current_period = models.SmallIntegerField(default=1)
  is_running = models.BooleanField(default=False)
  accumulated_seconds = models.IntegerField(default=0)
  last_started_at = models.DateTimeField(null=True, blank=True)
  added_time_seconds = models.IntegerField(default=0)
  updated_by = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.PROTECT
  )
  updated_at = models.DateTimeField(auto_now=True)


class MatchReporter(models.Model):
  match = models.ForeignKey(
      Match, on_delete=models.CASCADE, related_name="match_reporters"
  )
  user = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="match_assignments"
  )
  assigned_by = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.PROTECT,
      related_name="reporter_assignments_made",
  )
  assigned_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ("match", "user")


class LineupEntry(models.Model):
  match = models.ForeignKey(
      Match, on_delete=models.CASCADE, related_name="lineups"
  )
  team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="lineups")
  player = models.ForeignKey(
      Player, on_delete=models.PROTECT, related_name="lineups"
  )
  position = models.ForeignKey(
      Position, on_delete=models.PROTECT, null=True, blank=True
  )
  jersey_number = models.SmallIntegerField(null=True, blank=True)
  is_starter = models.BooleanField()

  class Meta:
    unique_together = ("match", "player")


class MatchEvent(models.Model):
  match = models.ForeignKey(
      Match, on_delete=models.CASCADE, related_name="events"
  )
  event_type = models.ForeignKey(EventType, on_delete=models.PROTECT)
  team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="events")
  player = models.ForeignKey(
      Player,
      on_delete=models.PROTECT,
      null=True,
      blank=True,
      related_name="events",
  )
  related_player = models.ForeignKey(
      Player,
      on_delete=models.PROTECT,
      null=True,
      blank=True,
      related_name="related_events",
  )
  period = models.SmallIntegerField(null=True, blank=True)
  clock_seconds = models.IntegerField(null=True, blank=True)
  created_by = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.PROTECT
  )
  created_at = models.DateTimeField(auto_now_add=True)
  is_voided = models.BooleanField(default=False)
  voided_by = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.PROTECT,
      null=True,
      blank=True,
      related_name="voided_events",
  )
  voided_at = models.DateTimeField(null=True, blank=True)
