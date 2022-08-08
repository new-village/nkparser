''' test_utilities.py
'''
import unittest

from nkparser import utilities


class TestUtilities(unittest.TestCase):
    ''' TestNkParser
    '''
    def test_create_table_strings_normal(self):
        ''' test_create_table_strings_normal
        '''
        for data_type in ['ENTRY', 'ODDS', 'RACE', 'ENTRY']:
            sql_strings = utilities.create_table_sql(data_type)

            # Compare result
            with self.subTest(dt=data_type):
                self.assertIn('CREATE TABLE IF NOT EXISTS '+ data_type, sql_strings)
