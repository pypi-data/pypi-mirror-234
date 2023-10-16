__all__ = [
    "Queue",
]

from django.db import models


class Queue(models.Model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = "django_command_queue"
