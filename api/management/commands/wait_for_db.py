import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **kwargs):
        db_connect = None
        while not db_connect:
            try:
                db_connect = connections["default"]
            except OperationalError:
                self.stdout.write("DB unavailable, waiting 1 second ...")
                time.sleep(1)
