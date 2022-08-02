''' test_load.py
'''
import json
import unittest

from bs4 import BeautifulSoup
from nkparser import load


class TestNkLoader(unittest.TestCase):
    ''' TestNkLoader
    '''
    def setUp(self):
        self.loader = load.NkLoader()

    def _load_title(self, race_id):
        text = self.loader.load('ENTRY', race_id)
        soup = BeautifulSoup(text, 'html.parser')
        return soup.select_one('div.RaceName')

    def test_entry_normal(self):
        ''' test_entry_normal
        '''
        # Load Arima Kinen page
        soup = self._load_title('201206050810')
        self.assertEqual(soup.get_text().strip(), '有馬記念')

    def test_entry_nonexistent_id(self):
        ''' test_entry_nonexistent_id
        '''
        # Load non-existent page
        soup = self._load_title('201206050899')
        self.assertIsNone(soup)

    def _load_odds(self, race_id):
        text = self.loader.load('ODDS', race_id)
        return json.loads(text)['status']

    def test_odds_normal(self):
        ''' test_odds_normal
        '''
        # Load Arima Kinen page
        status = self._load_odds('201206050810')
        self.assertEqual(status, 'result')

    def test_odds_nonexistent_id(self):
        ''' test_odds_nonexistent_id
        '''
        # Load non-existent page
        status = self._load_odds('201206050899')
        self.assertEqual(status, 'NG')

    def _load_horse(self, horse_id):
        text = self.loader.load('HORSE', horse_id)
        soup = BeautifulSoup(text, 'html.parser')
        return soup.select_one('div.horse_title > h1')

    def test_horse_normal(self):
        ''' test_horse_normal
        '''
        # Load Deep Impact page
        soup = self._load_horse('2002100816')
        self.assertEqual(soup.get_text().strip(), 'ディープインパクト')

    def test_horse_nonexistent_id(self):
        ''' test_horse_nonexistent_id
        '''
        # Load non-exist horse page
        soup = self._load_horse('2002100000')
        self.assertIsNone(soup)


if __name__ == '__main__':
    unittest.main()
