from django.db import models


class MatchRulesMixin(models.Model):
  class CoverageTier(models.TextChoices):
    FULL_LIVE = "FULL_LIVE", "Full Live"
    SCORE_ONLY = "SCORE_ONLY", "Score Only"
    RESULTS_ONLY = "RESULTS_ONLY", "Results Only"

  coverage_tier = models.CharField(
      max_length=12,
      choices=CoverageTier.choices,
      default=CoverageTier.FULL_LIVE,
  )
  period_count = models.SmallIntegerField(default=2)
  period_length_seconds = models.IntegerField(default=2700)
  has_stoppage_time = models.BooleanField(default=False)
  extra_time_enabled = models.BooleanField(default=False)
  extra_time_period_length_seconds = models.IntegerField(
      null=True, blank=True
  )
  extra_time_max_periods = models.SmallIntegerField(null=True, blank=True)
  shootout_enabled = models.BooleanField(default=False)

  class Meta:
    abstract = True


class Sport(MatchRulesMixin):
  class ClockDirection(models.TextChoices):
    UP = "UP", "Up"
    DOWN = "DOWN", "Down"

  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=60, unique=True)
  clock_direction = models.CharField(
      max_length=4, choices=ClockDirection.choices, default=ClockDirection.UP
  )
  period_label = models.CharField(max_length=20, default="Half")
  starters_count = models.SmallIntegerField(default=11)
  points_for_win = models.SmallIntegerField(default=3)
  points_for_draw = models.SmallIntegerField(null=True, blank=True, default=1)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.name


class Position(models.Model):
  sport = models.ForeignKey(
      Sport, on_delete=models.PROTECT, related_name="positions"
  )
  code = models.CharField(max_length=10)
  name = models.CharField(max_length=50)

  class Meta:
    unique_together = ("sport", "code")

  def __str__(self):
    return f"{self.sport.name} - {self.name} ({self.code})"


class EventType(models.Model):
  class RelatedPlayerRole(models.TextChoices):
    NONE = "NONE", "None"
    ASSIST = "ASSIST", "Assist"
    PLAYER_IN = "PLAYER_IN", "Player In"

  sport = models.ForeignKey(
      Sport, on_delete=models.PROTECT, related_name="event_types"
  )
  code = models.CharField(max_length=30)
  name = models.CharField(max_length=50)
  points = models.SmallIntegerField(default=0)
  credits_opponent = models.BooleanField(
      default=False
  )  # True = Own Goal, points go to opposing team
  is_shootout = models.BooleanField(default=False)
  related_player_role = models.CharField(
      max_length=10,
      choices=RelatedPlayerRole.choices,
      default=RelatedPlayerRole.NONE,
  )
  is_active = models.BooleanField(default=True)

  class Meta:
    unique_together = ("sport", "code")

  def __str__(self):
    return f"{self.sport.name} - {self.name}"