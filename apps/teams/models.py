from django.db import models
from django.conf import settings
from django.db import models
from sports.models import Sport


class Team(models.Model):
  sport = models.ForeignKey(
      Sport, on_delete=models.PROTECT, related_name="teams"
  )
  name = models.CharField(max_length=100)
  short_name = models.CharField(max_length=10)
  slug = models.SlugField(max_length=120, unique=True)
  logo = models.CharField(max_length=255, null=True, blank=True)
  is_active = models.BooleanField(default=True)

  class Meta:
    unique_together = ("sport", "name")

  def __str__(self):
    return self.name


class Manager(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  photo = models.CharField(max_length=255, null=True, blank=True)
  team = models.OneToOneField(
      Team,
      on_delete=models.PROTECT,
      null=True,
      blank=True,
      related_name="manager",
  )
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"


class Player(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  slug = models.SlugField(max_length=120, unique=True)
  photo = models.CharField(max_length=255, null=True, blank=True)
  is_active = models.BooleanField(
      default=True
  )  # False = graduated/retired

  def __str__(self):
    return f"{self.first_name} {self.last_name}"


class SquadMembership(models.Model):
  player = models.ForeignKey(
      Player, on_delete=models.PROTECT, related_name="squad_memberships"
  )
  team = models.ForeignKey(
      Team, on_delete=models.PROTECT, related_name="squad_memberships"
  )
  sport = models.ForeignKey(
      Sport, on_delete=models.PROTECT, related_name="squad_memberships"
  )
  position = models.ForeignKey(
      "sports.Position", on_delete=models.PROTECT, related_name="squad_memberships"
  )
  jersey_number = models.SmallIntegerField(null=True, blank=True)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  created_by = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.PROTECT
  )

  class Meta:
    constraints = [
        models.CheckConstraint(
            check=models.Q(end_date__isnull=True)
            | models.Q(end_date__gt=models.F("start_date")),
            name="membership_end_date_gt_start",
        )
    ]

  def __str__(self):
    return f"{self.player} at {self.team} ({self.start_date} - {self.end_date or 'Present'})"
