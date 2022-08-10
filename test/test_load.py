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
        self.assertEqual(len(nkdata.race), 1)
        self.assertEqual(len(nkdata.table), 16)

    def test_odds(self):
        """ test methond
        """
        nkdata = nkparser.load("ODDS", "201206050810")
        self.assertEqual(len(nkdata.table), 16)

    def test_result(self):
        """ test methond
        """
        nkdata = nkparser.load("RESULT", "201206050810")
        self.assertEqual(len(nkdata.race), 1)
        self.assertEqual(len(nkdata.table), 16)

if __name__ == '__main__':
    unittest.main()
