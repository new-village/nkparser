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
        cls.success_case = nkparser.load("result", "202006030711")
        # Load charset corruption case if requests use apparent_encoding option
        cls.euc_charset_case = nkparser.load("result", "202209020804")
        # Load local race
        cls.local_race_case = nkparser.load("result", "202250030808")
        # Load non-exist result case
        cls.error_case = nkparser.load("result", "201206050812")

    def test_success_case_count(self):
        """ testing success case counts
        """
        self.assertEqual(len(self.success_case.info), 1)
        self.assertEqual(len(self.success_case.table), 11)
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
            'id': '202006030711',
            'race_number': 11,
            'race_name': '第22回中山グランドジャンプ(J.G1)',
            'race_date': '2020-04-18',
            'race_time': '15:40',
            'type': '障害',
            'length': 4250,
            'length_class': 'Extended',
            'handed': '',
            'weather': '雨',
            'condition': '不良',
            'place': '中山',
            'course': '中山障4250',
            'round': 3,
            'days': 7,
            'head_count': 11,
            'max_prize': 6639.2
        }
        self.assertDictEqual(self.success_case.info[0], expect)

    def test_charset_corruption_race_parse(self):
        """ testing race data compalison
        """
        expect = {
            'id': '202209020804',
            'race_number': 4,
            'race_name': '3歳未勝利',
            'race_date': '2022-04-17',
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

    def test_local_race_parse(self):
        """ testing race data compalison
        """
        expect = {
            'id': '202250030808',
            'race_number': 8,
            'race_name': 'C2一',
            'race_date': '2022-03-08',
            'race_time': '16:20',
            'type': 'ダート',
            'length': 1400,
            'length_class': 'Mile',
            'handed': '右',
            'weather': '晴',
            'condition': '良',
            'place': '園田',
            'course': '園田ダ1400',
            'round': 22,
            'days': 4,
            'head_count': 10,
            'max_prize': 60.0
        }
        self.assertDictEqual(self.local_race_case.info[0], expect)

    def test_result_parse(self):
        """ testing race data compalison
        """
        expect = {
            'id': '20200603071106',
            'race_id': '202006030711',
            'rank': 1,
            'bracket': 6,
            'horse_number': 6,
            'horse_id': '2011101125',
            'horse_name': 'オジュウチョウサン',
            'gender': '牡',
            'age': 9,
            'burden': 63.0,
            'jockey_id': '01059',
            'jackey_name': '石神深一',
            'rap_time': 302.9,
            'diff_time': 0,
            'passage_rank': '2-2-1-1',
            'last_3f': 14.3,
            'weight': 510,
            'weight_diff': 0,
            'trainer_id': '01114',
            'trainer_name': '和田正一',
            'prize': 6639.2
        }
        self.assertDictEqual(self.success_case.table[0], expect)

    def test_suspension_result_parse(self):
        """ testing race data compalison
        """
        expect = {
            'id': '20200603071109',
            'race_id': '202006030711',
            'rank': None,
            'bracket': 7,
            'horse_number': 9,
            'horse_id': '2010101798',
            'horse_name': 'セガールフォンテン',
            'gender': '牡',
            'age': 10,
            'burden': 63.0,
            'jockey_id': '01087',
            'jackey_name': '上野翔',
            'rap_time': None,
            'diff_time': None,
            'passage_rank': '',
            'last_3f': None,
            'weight': 498,
            'weight_diff': -10,
            'trainer_id': '00428',
            'trainer_name': '石毛善彦',
            'prize': 0.0
        }
        self.assertDictEqual(self.success_case.table[10], expect)

if __name__ == '__main__':
    unittest.main()
