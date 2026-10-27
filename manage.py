from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  class Role(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    ADMIN = "ADMIN", "Admin"
    REPORTER = "REPORTER", "Reporter"

  email = models.EmailField(unique=True, max_length=254)
  role = models.CharField(
      max_length=12, choices=Role.choices, default=Role.REPORTER
  )
  sport_id = models.ForeignKey(
      "sports.Sport",
      on_delete=models.PROTECT,
      null=True,
      blank=True,
      related_name="users",
  )
  is_active = models.BooleanField(default=True)
  last_login = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = "accounts_user"
    constraints = [
        models.CheckConstraint(
            check=(
                models.Q(role="SUPER_ADMIN", sport_id__isnull=True)
                | models.Q(
                    role__in=["ADMIN", "REPORTER"], sport_id__isnull=False
                )
            ),
            name="user_role_sport_check",
        )
    ]