from django.core.management import call_command
from django.core.management.base import BaseCommand

from ...models import Queue


class Command(BaseCommand):
    help = "Command queue processing"

    def handle(self, *args, **options):
        for queue in Queue.objects.all():
            try:
                call_command(queue.name)
            finally:
                Queue.objects.filter(id=queue.id).delete()
