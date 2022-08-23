""" test_load.py
"""
import unittest
import nkparser

class TestNkLoader(unittest.TestCase):
    """ TestNkLoader
    """
    def test_entry(self):
        """ test methond
        """
        nkdata = nkparser.load("ENTRY", "201206050810")
        self.assertEqual(len(nkdata.info), 1)
        self.assertEqual(len(nkdata.table), 16)

    def test_entry_include_cancel(self):
        """ test methond
        """
        nkdata = nkparser.load("ENTRY", "202210040211")
        self.assertEqual(len(nkdata.info), 1)
        self.assertEqual(len(nkdata.table), 16)

    def test_entry_not_exist(self):
        """ The Load method with not existing race_id expect to return Zero length list.
        """
        nkdata = nkparser.load("ENTRY", "201206050812")
        self.assertEqual(len(nkdata.info), 0)
        self.assertEqual(len(nkdata.table), 0)

    def test_odds(self):
        """ test methond
        """
        nkdata = nkparser.load("ODDS", "201206050810")
        self.assertEqual(len(nkdata.table), 16)

    def test_odds_not_exist(self):
        """ The Load method with not existing race_id expect to return Zero length list.
        """
        nkdata = nkparser.load("ODDS", "201206050812")
        self.assertEqual(len(nkdata.table), 0)

    def test_result(self):
        """ test methond
        """
        nkdata = nkparser.load("RESULT", "201206050810")
        self.assertEqual(len(nkdata.table), 16)

    def test_result_not_exist(self):
        """ The Load method with not existing race_id expect to return Zero length list.
        """
        nkdata = nkparser.load("RESULT", "201206050812")
        self.assertEqual(len(nkdata.table), 0)

    def test_horse(self):
        """ test methond
        """
        nkdata = nkparser.load("HORSE", "2015100887")
        self.assertEqual(len(nkdata.info), 1)
        self.assertEqual(len(nkdata.table), 40)

    def test_horse_not_exist(self):
        """ The Load method with not existing horse_id expect to return Zero length list.
        """
        nkdata = nkparser.load("HORSE", "9999102739")
        self.assertEqual(len(nkdata.info), 0)
        self.assertEqual(len(nkdata.table), 0)

if __name__ == '__main__':
    unittest.main()
