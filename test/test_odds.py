""" test_load_result.py
"""
import unittest
import nkparser

class TestOddsNkLoader(unittest.TestCase):
    """ Test NkLoader with odds argument
    """
    @classmethod
    def setUpClass(cls):
        # Load Staygload who has overseas race history and abort race history
        cls.success_case = nkparser.load("odds", "202210040602")
        # Load Unexist horse ID
        cls.error_case = nkparser.load("odds", "201206050812")

    def test_odds(self):
        """ test methond
        """
        self.assertEqual(len(self.success_case.table), 16)

    def test_odds_not_exist(self):
        """ The Load method with not existing race_id expect to return Zero length list.
        """
        self.assertEqual(len(self.error_case.table), 0)

    def test_odds_parse(self):
        """ testing race data compalison
        """
        expect = {
            'id': '20221004060201',
            'race_id': '202210040602',
            'horse_number': 1,
            'win': 19.4,
            'show_min': 3.9,
            'show_max': 7.4
        }
        self.assertDictEqual(self.success_case.table[0], expect)

if __name__ == '__main__':
    unittest.main()
