import unittest
from nkparser import parse
from nkparser import load

class TestNkParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load class
        cls.parser = parse.NkParser()
        # Load sample data
        _loader = load.NkLoader()
        cls.normal = _loader.load('ENTRY', "201206050810")
        cls.error = _loader.load('ENTRY', "201206050899")

    def test_entry_normal(self):
        # Load Arima Kinen page
        entry = self.parser.parse('ENTRY', self.normal)
        # [(print(e)) for e in entry]
        # Compare result
        self.assertEqual(len(entry), 16)

    def test_entry_nonexistent_id(self):
        # Load Hakodate Kinen page
        with self.assertRaises(SystemExit):
            self.parser.parse('ENTRY', self.error)

    def test_race_normal(self):
        # Load Arima Kinen page
        race = self.parser.parse('RACE', self.normal)
        [(print(r)) for r in race]
        # Compare result
        self.assertEqual(len(race), 1)

if __name__ == '__main__':
    unittest.main