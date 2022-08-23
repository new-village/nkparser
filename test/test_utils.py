''' test_utilities.py
'''
import unittest

from nkparser.utils import create_index_sql, create_table_sql, race_list

class TestUtilities(unittest.TestCase):
    """ TestNkParser
    """
    def test_create_table_sql(self):
        """ test_create_table_sql
        """
        for data_type in ["entry", "odds", "race", "result", "horse", "history"]:
            sql_strings = create_table_sql(data_type)

            # Compare result
            with self.subTest(dt=data_type):
                self.assertIn('CREATE TABLE IF NOT EXISTS '+ data_type, sql_strings)

    def test_create_index_sql(self):
        """ test_create_index_sql
        """
        for data_type in ["entry", "result", "history"]:
            sql_strings = create_index_sql(data_type)

            # Compare result
            with self.subTest(dt=data_type):
                self.assertIn('CREATE INDEX IF NOT EXISTS ', sql_strings)

    def test_race_list(self):
        """ test_create_list
        """
        races = race_list(2022, 7)
        self.assertEqual(len(races), 336)
