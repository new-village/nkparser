""" test_load_result.py
"""
import unittest
import nkparser

class TestHorseNkLoader(unittest.TestCase):
    """ Test NkLoader with Horse arguments
    """
    @classmethod
    def setUpClass(cls):
        # Load Staygload who has overseas race history and abort race history
        cls.success_case = nkparser.load("horse", "1994108729")
        # Load Unexist horse ID
        cls.error_case = nkparser.load("horse", "9999102739")

    def test_success_case_count(self):
        """ testing success case counts
        """
        self.assertEqual(len(self.success_case.info), 1)
        self.assertEqual(len(self.success_case.table), 50)

    def test_error_case_count(self):
        """ testing error case counts
        """
        self.assertEqual(len(self.error_case.info), 0)
        self.assertEqual(len(self.error_case.table), 0)

    def test_jra_race_parsing(self):
        """ testing success case which is overseas run history
        """
        expect = {
            'id': '20010505081008',
            'horse_id': '1994108729',
            'race_date': '2001-11-25',
            'place': '東京',
            'round': 5,
            'days': 8,
            'weather': '晴',
            'race_number': 10,
            'race_id': '200105050810',
            'race_name': 'ジャパンC(G1)',
            'head_count': 15,
            'bracket': 5,
            'horse_number': 8,
            'win_odds': 8.1,
            'popularity': 4,
            'rank': 4,
            'jockey_id': '00666',
            'jockey_name': '武豊',
            'burden': 57.0,
            'type': '芝',
            'length': 2400,
            'length_class': 'Long',
            'course': '東京芝2400',
            'condition': '良',
            'rap_time': 144.5,
            'passage_rank': '7-6-8-6',
            'last_3f': 35.8,
            'weight': 428,
            'weight_diff': 0,
            'prize': 3800.0
        }
        self.assertDictEqual(self.success_case.table[1], expect)

    def test_overseas_race_parsing(self):
        """ testing success case which is overseas run history
        """
        expect = {
            'id': '2001G012160509',
            'horse_id': '1994108729',
            'race_date': '2001-12-16',
            'place': '香港',
            'round': None,
            'days': None,
            'weather': '',
            'race_number': 5,
            'race_id': '2001G0121605',
            'race_name': '香港ヴァーズ(G1)',
            'head_count': 14,
            'bracket': None,
            'horse_number': 9,
            'win_odds': None,
            'popularity': None,
            'rank': 1,
            'jockey_id': '00666',
            'jockey_name': '武豊',
            'burden': 57.1,
            'type': '芝',
            'length': 2400,
            'length_class': 'Long',
            'course': '香港芝2400',
            'condition': '良',
            'rap_time': 147.8,
            'passage_rank': '',
            'last_3f': None,
            'weight': None,
            'weight_diff': None,
            'prize': 0.0
        }
        self.assertDictEqual(self.success_case.table[0], expect)

if __name__ == '__main__':
    unittest.main()
