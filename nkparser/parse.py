''' parse.py
'''
import itertools
import os
import json
import logging
from abc import ABCMeta, abstractmethod

import jq
from bs4 import BeautifulSoup

import nkparser
from nkparser.helper import *

# Set Logger
logger = logging.getLogger('NkParser')

class NkParser():
    ''' NkParser
    '''
    def parse(self, data_type, text):
        ''' parse
        '''
        # Parse HTML file
        parser = self._create_parser(data_type)
        return parser.execute(text)

    def _create_parser(self, data_type):
        if data_type == "RACE":
            return RaceParser(data_type)
        elif data_type == "ENTRY":
            return EntryParser(data_type)
        elif data_type == "ODDS":
            return OddsParser(data_type)
        elif data_type == "RESULT":
            return ResultParser(data_type)
        elif data_type == "HORSE":
            return HorseParser(data_type)
        else:
            # Raise error and abort script
            logger.error('Unexpected data type: %s', data_type)
            raise SystemExit()

class BaseParser(metaclass=ABCMeta):
    ''' BaseParser
    '''
    def __init__(self, data_type):
        # Load JSON file
        self.config_json = self._load_config(data_type)
        self.keys = self.config_json.keys()

    def _area_parse(self, soup, css_selector):
        try:
            area = soup.select(css_selector)
        except AttributeError as exp:
            logger.error('There is not "%s" in HTML', css_selector)
            raise SystemExit from exp

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
            return formatter(r'\d+', soup.select_one(target_selector).a.get("href"), 'url')
        except AttributeError as exp:
            logger.error('Race ID is not found in %s selector area', target_selector)
            raise SystemExit from exp

    def _load_config(self, data_type):
        try:
            dir = os.path.dirname(nkparser.__file__) + '/config/'
            with open(dir + data_type + '.json', 'r', encoding='UTF-8') as file:
                return json.load(file)
        except json.JSONDecodeError as exc:
            # Raise error and abort script
            logger.error('Config file decode error: %s', exc)
            raise SystemExit() from exc
        except FileNotFoundError as exc:
            logger.error('Config file not found: %s', exc)
            raise SystemExit() from exc

    def _parse_data(self, row):
        return {key: row.select_one(self.config_json[key]['selector']) for key in self.keys}

    def _conv_var_type(self, key, val):
        if val is not None:
            if self.config_json[key]['var_type'] == 'name':
                val = val.a.get("title") if val.a is not None else None
            elif self.config_json[key]['var_type'] == 'url':
                val = val.a.get("href") if val.a is not None else None
            else:
                val = val.text
        return val

    def _conv_format(self, key, val):
        if 'function' in self.config_json[key]:
            val = globals()[self.config_json[key]['function']](val)
        elif 'reg' in self.config_json[key]:
            val = formatter(self.config_json[key]['reg'], val, self.config_json[key]['var_type'])
        return val

    @abstractmethod
    def execute(self, text):
        ''' execute
        '''

class EntryParser(BaseParser):
    ''' EntryParser
    '''
    def execute(self, text):
        ''' execute
        '''
        # Parse Entry Data
        soup = BeautifulSoup(text, 'html.parser')
        entry = self._area_parse(soup, 'tr.HorseList')
        # Add race_id
        race_id = self._get_race_id(soup)
        [e.update({'race_id': race_id}) for e in entry]
        return entry

class RaceParser(BaseParser):
    ''' RaceParser
    '''
    def execute(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        race = self._area_parse(soup, 'div.RaceMainColumn')
        if race[0]['race_id'] is None:
            logger.error('There is no race_id in HTML')
            raise SystemExit
        return race

class OddsParser(BaseParser):
    ''' OddsParser
    '''
    def execute(self, text):
        # Parse Odds Data from JSON string
        data = json.loads(text)
        odds = [self._add_header(record_tuple) for record_tuple in self._create_matrix(data)]
        # Formatting Value
        odds = [{key: self._conv_format(key, line[key]) for key in self.keys} for line in odds]
        # Add race_id
        race_id = jq.compile('.race_id').input(data).text().replace('"', '')
        [o.update({'race_id': race_id}) for o in odds]
        return odds

    def _create_matrix(self, data):
        tmx = [self._parse_json(key, data) for key in self.keys]
        return list(itertools.zip_longest(*tmx))

    def _parse_json(self, key, data):
        try:
            return jq.compile(self.config_json[key]['selector']).input(data).all()
        except ValueError:
            return []

    def _add_header(self, record):
        return {key: val for key, val in zip(self.keys, record)}

class ResultParser(BaseParser):
    ''' ResultParser
    '''
    def execute(self, text):
        # Parse Entry Data
        soup = BeautifulSoup(text, 'html.parser')
        race = self._area_parse(soup, 'tr.HorseList')

        # Add race_id
        race_id = self._get_race_id(soup)
        [r.update({'race_id': race_id}) for r in race]

        # Add prize
        prize_text = formatter(r'本賞金:(.+)万円', soup.select_one('.RaceData02').text, 'str').split(',')
        prize = [int(p) for p in prize_text] + [0] * (len(race) - len(prize_text))
        [r.update({'prize': p}) for r, p in zip(race, prize)]

        return race

class HorseParser(BaseParser):
    ''' HorseParser
    '''
    def execute(self, text):
        pass
