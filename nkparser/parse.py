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
        if data_type == "RACE":
            return RaceParser(data_type)
        elif data_type == "ENTRY":
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

    def _run_parser_job(self, soup, css_selector):
        try:
            area = soup.select(css_selector)
        except AttributeError as e:
            logger.error('There is not "%s" in HTML' % css_selector)
            raise SystemExit(e)

        # Extract HTML from target area
        rec = [self._parse_data(row) for row in area]
        # Extract Value from HTML
        rec = [{key: self._conv_var_type(key, line[key]) for key in self.keys} for line in rec]
        # Formatting Value
        rec = [{key: self._conv_format(key, line[key]) for key in self.keys} for line in rec]

        return rec

    def _get_race_id(self, soup):
        try:
            target_selector = 'li.Active'
            race_id = formatter(r'\d+', soup.select_one(target_selector).a.get("href"), 'url')
        except AttributeError as e:
            logger.error('Race ID is not found in %s selector area' % target_selector)
            raise SystemExit(e)
 
        return race_id


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
    def execute(self):
        pass

class EntryParser(BaseParser):
    def execute(self, soup):
        # Parse Entry Data
        entry = self._run_parser_job(soup, 'tr.HorseList')
        # Add race_id
        race_id = self._get_race_id(soup)
        [e.update({'race_id': race_id}) for e in entry]

        return entry

    
class RaceParser(BaseParser):    
    def execute(self, soup):
        # Parse Entry Data
        race = self._run_parser_job(soup, 'div.RaceMainColumn')
        return race


class OddsParser(BaseParser):
    def execute(self, soup):
        pass

class HorseParser(BaseParser):
    def execute(self, soup):
        pass


