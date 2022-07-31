''' test_parser.py
'''
import unittest

from bs4 import BeautifulSoup
from nkparser import load, parse


class TestNkParser(unittest.TestCase):
    ''' TestNkParser
    '''
    @classmethod
    def setUpClass(cls):
        # Load class
        cls.loader = load.NkLoader()
        cls.parser = parse.NkParser()

    def _load_page(self, race_id):
        return self.loader.load('ENTRY', race_id)

    def test_entry_normal(self):
        ''' test_entry_normal
        '''
        # Load Arima Kinen page
        text = self._load_page('201206050810')
        entry = self.parser.parse('ENTRY', text)
        #[(print(e)) for e in entry]
        # Compare result
        self.assertEqual(len(entry), 16)

    def test_entry_nonexistent_id(self):
        ''' test_entry_nonexistent_id
        '''
        # Non-exist pages
        text = self._load_page('201206050899')
        with self.assertRaises(SystemExit):
            self.parser.parse('ENTRY', text)

    def test_race_normal(self):
        ''' test_race_normal
        '''
        # Load Arima Kinen page
        text = self._load_page('201206050810')
        race = self.parser.parse('RACE', text)
        #[(print(e)) for e in race]
        # Compare result
        self.assertEqual(len(race), 1)

    def test_race_nonexistent_id(self):
        ''' test_race_nonexistent_id
        '''
        # Load Arima Kinen page
        text = self._load_page('201206050899')
        with self.assertRaises(SystemExit):
            self.parser.parse('RACE', text)

    # def test_odds_normal(self):
    #     # Load Arima Kinen page
    #     odds = self.parser.parse('ODDS', self.normal)
    #     #[(print(o)) for o in odds]
    #     # Compare result
    #     self.assertEqual(len(odds), 16)

if __name__ == '__main__':
    unittest.main()
