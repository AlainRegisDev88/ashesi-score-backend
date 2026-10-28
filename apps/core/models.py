from django.conf import settings
from django.db import models


class AuditLog(models.Model):
  class Action(models.TextChoices):
    CREATE = "CREATE", "Create"
    UPDATE = "UPDATE", "Update"
    DELETE = "DELETE", "Delete"
    VOID = "VOID", "Void"

  user = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="audit_logs"
  )
  action = models.CharField(max_length=10, choices=Action.choices)
  entity_type = models.CharField(max_length=50)
  entity_id = models.BigIntegerField()
  changes = models.JSONField()  # Postgres jsonb
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = "core_audit_log"