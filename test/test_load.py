import unittest
from nkparser import load

class TestNkLoader(unittest.TestCase):
    def setUp(self):
        self.loader = load.NkLoader()

    def test_entry_normal(self):
        # Load Hakodate Kinen page
        soup = self.loader.load('ENTRY', "202202011211")
        # Compare result
        title = soup.select_one('div.RaceName').get_text().strip()
        self.assertEqual(title, '函館記念')

    def test_entry_nonexistent_id(self):
        # Load non-existent page
        soup = self.loader.load('ENTRY', "202202011299")
        # Compare result
        self.assertIsNone(soup)

    def test_odds_normal(self):
        # Load Hayayako-odds page
        soup = self.loader.load('ODDS', "202202011211")
        # Compare result
        horse_name = soup.select_one('td.Horse_Name').get_text().strip()
        self.assertEqual(horse_name, 'ハヤヤッコ')

    def test_odds_nonexistent_id(self):
        # Load Hayayako-odds page
        soup = self.loader.load('ODDS', "202202011299")
        # Compare result
        self.assertIsNone(soup)

    def test_horse_normal(self):
        # Load Deep Impact page
        soup = self.loader.load('HORSE', '2002100816')
        # Compare result
        horse_name = soup.select_one('div.horse_title > h1').get_text().strip()
        self.assertEqual(horse_name, 'ディープインパクト')

    def test_horse_nonexistent_id(self):
        # Load non-exist horse page
        soup = self.loader.load('HORSE', '2002100000')
        # Compare result
        self.assertIsNone(soup)


if __name__ == '__main__':
    unittest.main