import json
import logging
from abc import ABCMeta, abstractmethod

from .helper import formatter

# Set Logger
logger = logging.getLogger('NkParser')

class NkParser():
    def parse(self, data_type, soup):
        # Parse HTML file
        parser = self._create_parser(data_type)
        return parser.execute(soup)

    def _create_parser(self, data_type):
        if data_type == "ENTRY":
            return EntryParser(data_type)
        elif data_type == "ODDS":
            return OddsParser(data_type)
        elif data_type == "HORSE":
            return HorseParser(data_type)
        else:
            # Raise error and abort script
            logger.error('Unexpected data type: %s' % (data_type))
            raise SystemExit()

class BaseParser(metaclass=ABCMeta):
    def __init__(self, data_type):
        # Load JSON file
        self.config_json = self._load_config(data_type)
        self.keys = self.config_json.keys()

    def execute(self, soup):
        try:
            area = soup.select(self._css_selector())
        except AttributeError:
            logger.error('There is not "%s" in HTML' % self._css_selector())
            raise SystemExit()

        # Extract HTML from target area
        entry = [self._parse_data(row) for row in area[2:]]
        # Extract Value from HTML
        entry = [{key: self._conv_var_type(key, horse[key]) for key in self.keys} for horse in entry]
        # Formatting Value
        entry = [{key: self._conv_format(key, horse[key]) for key in self.keys} for horse in entry]
        return entry

    def _load_config(self, data_type):
        try:
            with open('nkparser/config/' + data_type + '.json', 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            # Raise error and abort script
            logger.error('Config file decode error:', e)
            raise SystemExit()
        except FileNotFoundError as e:
            logger.error('Config file not found:', e)
            raise SystemExit()
       
    def _parse_data(self, row):
        return {key: row.select_one(self.config_json[key]['selector']) for key in self.keys}

    def _conv_var_type(self, key, val):
        if val is not None:
            if self.config_json[key]['var_type'] == 'name':
                val = val.a.get("title")
            elif self.config_json[key]['var_type'] == 'url':
                val = val.a.get("href")
            else:
                val = val.text
        return val

    def _conv_format(self, key, val):
        if 'reg' in self.config_json[key]:
            val = formatter(self.config_json[key]['reg'], val, self.config_json[key]['var_type'])
        return val

    @abstractmethod
    def _css_selector(self):
        pass

class EntryParser(BaseParser):
    def _css_selector(self):
        return 'table.ShutubaTable tr'
    
class OddsParser():
    def __init__(self) -> None:
        pass

class HorseParser():
    def __init__(self) -> None:
        pass


