''' parse.py
'''
import itertools
import json

import jq
from bs4 import BeautifulSoup, Tag

from nkparser.help import *

def parse_text(data_type, text, entity_id=None):
    """ HTML parser by config file
    :param data_type: data type of target such as ENTRY, RESULT, ODDS and HORSE
    :param entity_id: entity id of target such as race id or horse id
    :return: :class:`Response <Response>` object
    """
    if data_type in ["RACE"]:
        parser = TextParser(data_type, text, entity_id, "div.RaceMainColumn")
    elif data_type in ["ENTRY", "RESULT"]:
        parser = TextParser(data_type, text, entity_id, "tr.HorseList")
    elif data_type in ["CAL"]:
        parser = TextParser(data_type, text, entity_id, "table.scheLs tr")
    else:
        raise ValueError(f"Unexpected data type: {data_type}")

    return parser.exec()

def parse_json(data_type, text, entity_id=None):
    """ JSON parser by config file
    """
    parser = JsonParser(data_type, text, entity_id, "div.RaceMainColumn")
    return parser.exec()

class Parser():
    """ base class of Loaders """
    def __init__(self, data_type, text, entity_id, selector):
        self.data_type = data_type
        self.entity_id = entity_id
        self.soup = BeautifulSoup(text, "html.parser")
        self.text = text
        self.selector = selector
        self.conf = load_config(data_type)
        self.keys = self.conf.keys()

    def _apply_func(self, key, val):
        if 'func' in self.conf[key] and val is not None:
            val = globals()[self.conf[key]['func']](val)
        return val

    def _apply_format(self, key, val):
        if 'reg' in self.conf[key] and val is not None:
            val = formatter(self.conf[key]['reg'], val, self.conf[key]['var_type'])
        return val

    def _add_entity_id(self, line:dict):
        for key in line.keys():
            if key in ["race_id"]:
                line[key] = self.entity_id
            elif key in ["entry_id", "result_id", "odds_id"]:
                if line['horse_number'] is not None:
                    line[key] = self.entity_id + line['horse_number'].zfill(2)
                else:
                    line[key] = None
        return line

class TextParser(Parser):
    """ base class of Loaders """
    def exec(self):
        """ execute Job
        """
        # extract data
        work = [self._parse_data(row) for row in self._base_data()]
        # apply function
        work = [{key: self._apply_func(key, row[key]) for key in self.keys} for row in work]
        # convert bs4 to string
        work = [{key: self._to_string(row[key]) for key in self.keys} for row in work]
        # apply format
        work = [{key: self._apply_format(key, row[key]) for key in self.keys} for row in work]
        # special data processing for ENTRY and RESULT
        if self.data_type in ["ENTRY", "RESULT"]:
            work = [self._add_entity_id(row) for row in work]
        if self.data_type in ["RESULT"]:
            work = set_prize(self.soup, work) if len(work) != 0 else work
        # remove blank race data
        if self.data_type in ["RACE"]:
            work = work if work[0][f"{self.data_type.lower()}_id"] is not None else []
        # specific process for CAL
        if self.data_type in ["CAL"]:
            # remove blank data
            work = [row["race_id"] for row in work if row["race_id"] is not None and row["race_id"] != ""]
            work = sum([['20' + row + str(i + 1).zfill(2) for i in range(12)] for row in work], [])

        return work

    def _base_data(self):
        try:
            area = self.soup.select(self.selector)
        except AttributeError:
            area = []
        return area

    def _parse_data(self, row):
        return {key: row.select_one(self.conf[key]['selector']) for key in self.keys}

    def _to_string(self, val):
        if isinstance(val, Tag):
            val = val.text
        return val

class JsonParser(Parser):
    """ base class of Loaders """
    def exec(self):
        """ execute Job
        """
        # Parse Odds Data from JSON string
        work = json.loads(self.text)
        work = [self._add_header(record_tuple) for record_tuple in self._create_matrix(work)]
        # apply function
        work = [{key: self._apply_func(key, row[key]) for key in self.keys} for row in work]
        # Formatting Value
        work = [{key: self._apply_format(key, line[key]) for key in self.keys} for line in work]
        # Add race_id
        if self.data_type in ["ODDS"]:
            work = [self._add_entity_id(row) for row in work]
            # remove blank data
            work = work if work[0][f"{self.data_type.lower()}_id"] is not None else []

        return work

    def _create_matrix(self, data):
        tmx = [self._parse_json(key, data) for key in self.keys]
        return list(itertools.zip_longest(*tmx))

    def _parse_json(self, key, data):
        try:
            return jq.compile(self.conf[key]['selector']).input(data).all()
        except ValueError:
            return []

    def _add_header(self, record):
        return {key: val for key, val in zip(self.keys, record)}
