""" test_load_result.py
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

if __name__ == '__main__':
    unittest.main()
