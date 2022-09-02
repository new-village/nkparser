""" test_load.py
"""
import unittest
import nkparser

class TestEntryNkLoader(unittest.TestCase):
    """ Test NkLoader with Entry arguments
    """
    @classmethod
    def setUpClass(cls):
        # Load Staygload who has overseas race history and abort race history
        cls.success_case = nkparser.load("entry", "202210040211")
        # Load Unexist horse ID
        cls.error_case = nkparser.load("entry", "201206050812")

    def test_success_case_count(self):
        """ testing success case counts
        """
        self.assertEqual(len(self.success_case.info), 1)
        self.assertEqual(len(self.success_case.table), 16)

    def test_error_case_count(self):
        """ testing error case counts
        """
        self.assertEqual(len(self.error_case.info), 0)
        self.assertEqual(len(self.error_case.table), 0)

    def test_race_parse(self):
        """ testing race data compalison
        """
        expect = {
            'id': '202210040211',
            'race_number': 11,
            'race_name': '小倉記念',
            'race_date': '2022-08-14',
            'race_time': '15:35',
            'type': '芝',
            'length': 2000,
            'length_class': 'Intermediate',
            'handed': '右',
            'weather': '晴',
            'condition': '良',
            'place': '小倉',
            'course': '小倉芝2000',
            'round': 4,
            'days': 2,
            'head_count': 16,
            'max_prize': 4300.0
        }
        self.assertDictEqual(self.success_case.info[0], expect)

    def test_entry_parse(self):
        """ testing race data compalison
        """
        expect = {
            'id': '20221004021102',
            'race_id': '202210040211',
            'bracket': 1,
            'horse_number': 2,
            'horse_id': '2018100927',
            'horse_name': 'マリアエレーナ',
            'gender': '牝',
            'age': 4,
            'burden': 54.0,
            'jockey_id': '01126',
            'jackey_name': '松山',
            'trainer_id': '01101',
            'trainer_name': '吉田',
            'weight': 424,
            'weight_diff': -2
        }
        self.assertDictEqual(self.success_case.table[1], expect)

    def test_suspension_entry_parse(self):
        """ testing race data compalison
        """
        expect = {
            'id': '20221004021108',
            'race_id': '202210040211',
            'bracket': 4,
            'horse_number': 8,
            'horse_id': '2017105106',
            'horse_name': 'プリマヴィスタ',
            'gender': '牡',
            'age': 5,
            'burden': 53.0,
            'jockey_id': '01130',
            'jackey_name': '高倉',
            'trainer_id': '01075',
            'trainer_name': '矢作',
            'weight': None,
            'weight_diff': None
        }
        self.assertDictEqual(self.success_case.table[7], expect)

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

class TestResultNkLoader(unittest.TestCase):
    """ Test NkLoader with result arguments
    """
    @classmethod
    def setUpClass(cls):
        # Load Staygload who has overseas race history and abort race history
        cls.success_case = nkparser.load("result", "200108040211")
        # Load Unexist horse ID
        cls.error_case = nkparser.load("result", "201206050812")

    def test_success_case_count(self):
        """ testing success case counts
        """
        self.assertEqual(len(self.success_case.table), 7)

    def test_error_case_count(self):
        """ testing error case counts
        """
        self.assertEqual(len(self.error_case.table), 0)

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
