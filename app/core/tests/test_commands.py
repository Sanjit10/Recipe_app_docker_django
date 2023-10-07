"""
Test custom Django commands
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OperationalError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# The BaseCommand class has a method check and
# that is what we will be mocking in the code below
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

# Since we are patching the check method a extra parameter will
# be passed that will mock the check ...patched_check
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db when db is available"""

        # We are mocking the check method and setting it to return True i.e
        # every time check method is called it will return True
        patched_check.return_value = True

        # Call_command is a django helper function that allows us to call
        # the command we want to test

        # It will execute the handle method in the command we are testing
        # It will also check if the command is actually called
        call_command('wait_for_db')

        # assert_called_once_with is a mock method that will check if
        # the method is called once with the specified parameters
        patched_check.assert_called_once_with(databases=['default'])

    # the BaseCommand class has a method called sleep that is called after
    # everytime a database is called
    # But this will only increase the time of the test so we will mock it

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):

        """Test waiting for db when gettin operational error"""

        # Here we are mocking check method, and returning some
        # exception or operation error

        # For the first 2 times we call it we are returning
        # Psycopg2OperationalError and for the next 3 times
        # we are returning OperationalError

        # Psycopg2OperationalError is the error that django will
        # throw when Postgress hasnt even started and is not
        # available

        # OperationalError is the error that django will throw when
        # the database is not available but Postgress has started

        patched_check.side_effect = [Psycopg2OperationalError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
