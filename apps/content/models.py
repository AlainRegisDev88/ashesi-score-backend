from django.conf import settings
from django.db import models
from competitions.models import Competition
from matches.models import Match
from sports.models import Sport
from teams.models import Player, Team


class NewsArticle(models.Model):
  class Status(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"

  sport = models.ForeignKey(
      Sport,
      on_delete=models.PROTECT,
      null=True,
      blank=True,
      related_name="news",
  )  # NULL = general news
  author = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="articles"
  )
  title = models.CharField(max_length=200)
  slug = models.SlugField(max_length=220, unique=True)
  body = models.TextField()
  cover_image = models.CharField(max_length=255, null=True, blank=True)
  status = models.CharField(
      max_length=9, choices=Status.choices, default=Status.DRAFT
  )
  published_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    constraints = [
        models.CheckConstraint(
            condition=~models.Q(status="PUBLISHED")
            | models.Q(published_at__isnull=False),
            name="news_published_at_required",
        )
    ]


class Award(models.Model):
  class AwardType(models.TextChoices):
    COMPETITION = "COMPETITION", "Competition"
    MATCH = "MATCH", "Match"

  title = models.CharField(max_length=100)
  award_type = models.CharField(max_length=11, choices=AwardType.choices)
  competition = models.ForeignKey(
      Competition, on_delete=models.PROTECT, null=True, blank=True
  )
  match = models.ForeignKey(Match, on_delete=models.PROTECT, null=True, blank=True)
  player = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, blank=True)
  team = models.ForeignKey(Team, on_delete=models.PROTECT, null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  awarded_by = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.PROTECT
  )
  created_at = models.DateTimeField(auto_now_add=True)
