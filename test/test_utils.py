''' test_utilities.py
'''
import unittest

from nkparser.utils import create_table_sql

class TestUtilities(unittest.TestCase):
    """ TestNkParser
    """
    def test_create_table_sql(self):
        """ test_create_table_sql
        """
        for data_type in ['ENTRY', 'ODDS', 'RACE', 'RESULT']:
            sql_strings = create_table_sql(data_type)
            print(sql_strings)

            # Compare result
            with self.subTest(dt=data_type):
                self.assertIn('CREATE TABLE IF NOT EXISTS '+ data_type, sql_strings)
