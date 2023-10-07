"""
Django command to wait for the db to bne avilaible
"""

import time

from psycopg2 import OperationalError as Psycopg2OperationalError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        """Entry point for command"""
        self.stdout.write('Waiting for database...')
        db_up = False
        while not db_up:
            try:
                # This will try to connect to the database
                # If the database is not available it will throw an error
                # If the database is available it will return True
                # We are using the default database
                self.check(databases=['default'])
                db_up = True
            except Psycopg2OperationalError:
                # If the database is not available we will wait for 1 second
                # and then try to connect again
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
            except OperationalError:
                # If the database is not available we will wait for 1 second
                # and then try to connect again
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
