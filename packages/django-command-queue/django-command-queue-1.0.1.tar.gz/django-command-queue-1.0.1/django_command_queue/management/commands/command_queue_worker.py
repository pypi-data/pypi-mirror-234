import time

from django.conf import settings
from django.core.management import call_command, get_commands
from django.core.management.base import BaseCommand

COMMAND_NAME_LIST = list(map(lambda c: c.name for c in get_commands.items()))
COMMAND_WORKER_RESTART = getattr(settings, "COMMAND_WORKER_RESTART", 0)
COMMAND_WORKER_SLEEP = getattr(settings, "COMMAND_WORKER_SLEEP", 0.1)


class Command(BaseCommand):
    help = "Command queue worker"

    def handle(self, *args, **options):
        while True:
            if COMMAND_WORKER_RESTART and time.time() > COMMAND_WORKER_RESTART:
                return
            call_command("command_queue")
            # command_worker_sleep.py or time.sleep(settings.COMMAND_WORKER_SLEEP)
            if "command_queue_sleep" in COMMAND_NAME_LIST:
                call_command("command_queue_sleep")
            else:
                time.sleep(COMMAND_WORKER_SLEEP)
