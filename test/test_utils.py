''' test_utilities.py
'''
import unittest

from nkparser.utils import create_table_sql, race_list

class TestUtilities(unittest.TestCase):
    """ TestNkParser
    """
    def test_create_table_sql(self):
        """ test_create_table_sql
        """
        for data_type in ['ENTRY', 'ODDS', 'RACE', 'RESULT']:
            sql_strings = create_table_sql(data_type)

            # Compare result
            with self.subTest(dt=data_type):
                self.assertIn('CREATE TABLE IF NOT EXISTS '+ data_type, sql_strings)

    def test_race_list(self):
        """ test_create_list
        """
        races = race_list(2022, 7)
        self.assertEqual(len(races), 336)