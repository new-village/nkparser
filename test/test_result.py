""" test_load_result.py
"""
import unittest
import nkparser

class TestResultNkLoader(unittest.TestCase):
    """ Test NkLoader with result arguments
    """
    @classmethod
    def setUpClass(cls):
        # Load normal result case includes suspension entry
        cls.success_case = nkparser.load("result", "200108040211")
        # Load charset corruption case if requests use apparent_encoding option
        cls.euc_charset_case = nkparser.load("result", "202209020804")
        # Load non-exist result case
        cls.error_case = nkparser.load("result", "201206050812")

    def test_success_case_count(self):
        """ testing success case counts
        """
        self.assertEqual(len(self.success_case.info), 1)
        self.assertEqual(len(self.success_case.table), 7)
        self.assertEqual(len(self.euc_charset_case.info), 1)
        self.assertEqual(len(self.euc_charset_case.table), 18)

    def test_error_case_count(self):
        """ testing error case counts
        """
        self.assertEqual(len(self.error_case.info), 0)
        self.assertEqual(len(self.error_case.table), 0)

    def test_race_parse(self):
        """ testing race data compalison
        """
        expect = {
            'id': '200108040211',
            'race_number': 11,
            'race_name': '第36回京都大賞典(G2)',
            'race_date': '2001-08-04',
            'race_time': '15:45',
            'type': '芝',
            'length': 2400,
            'length_class': 'Long',
            'handed': '右',
            'weather': '晴',
            'condition': '良',
            'place': '京都',
            'course': '京都芝2400',
            'round': 4,
            'days': 2,
            'head_count': 7,
            'max_prize': 6449.0
        }
        self.assertDictEqual(self.success_case.info[0], expect)

    def test_charset_corruption_race_parse(self):
        """ testing race data compalison
        """
        expect = {
            'id': '202209020804',
            'race_number': 4,
            'race_name': '3歳未勝利',
            'race_date': '2022-09-02',
            'race_time': '11:20',
            'type': '芝',
            'length': 2200,
            'length_class': 'Long',
            'handed': '右',
            'weather': '晴',
            'condition': '良',
            'place': '阪神',
            'course': '阪神芝2200',
            'round': 2,
            'days': 8,
            'head_count': 18,
            'max_prize': 520.0
        }
        self.assertDictEqual(self.euc_charset_case.info[0], expect)

    def test_result_parse(self):
        """ testing race data compalison
        """
        expect = {
            'id': '20010804021105',
            'race_id': '200108040211',
            'rank': 1,
            'bracket': 5,
            'horse_number': 5,
            'horse_id': '1996100292',
            'horse_name': 'テイエムオペラオー',
            'gender': '牡',
            'age': 5,
            'burden': 59.0,
            'jockey_id': '01018',
            'jackey_name': '和田竜二',
            'rap_time': 145.0,
            'diff_time': 0,
            'passage_rank': '2-2-2-3',
            'last_3f': 34.1,
            'weight': 478,
            'weight_diff': 4,
            'trainer_id': '00397',
            'trainer_name': '岩元市三',
            'prize': 6449.0
        }
        self.assertDictEqual(self.success_case.table[0], expect)

    def test_suspension_result_parse(self):
        """ testing race data compalison
        """
        expect = {
            'id': '20010804021104',
            'race_id': '200108040211',
            'rank': None,
            'bracket': 4,
            'horse_number': 4,
            'horse_id': '1996102442',
            'horse_name': 'ナリタトップロード',
            'gender': '牡',
            'age': 5,
            'burden': 59.0,
            'jockey_id': '00734',
            'jackey_name': '渡辺薫彦',
            'rap_time': None,
            'diff_time': None,
            'passage_rank': '4-4-2-2',
            'last_3f': None,
            'weight': 492,
            'weight_diff': 4,
            'trainer_id': '00378',
            'trainer_name': '沖芳夫',
            'prize': 0.0
        }
        self.assertDictEqual(self.success_case.table[5], expect)

if __name__ == '__main__':
    unittest.main()
