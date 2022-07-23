import unittest
from nkparser import parse
from nkparser import load

class TestNkParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load class
        cls.parser = parse.NkParser()
        # Load sample data
        cls.loader = load.NkLoader()
        
    def test_entry_normal(self):
        # Load Arima Kinen page
        raw = self.loader.load('ENTRY', "201206050810")
        entry = self.parser.parse('ENTRY', raw)
        #[(print(e)) for e in entry]
        # Compare result
        self.assertEqual(len(entry), 16)

    def test_entry_nonexistent_id(self):
        # Load Hakodate Kinen page
        raw = self.loader.load('ENTRY', "201206050899")
        with self.assertRaises(SystemExit):
            self.parser.parse('ENTRY', raw)

if __name__ == '__main__':
    unittest.main