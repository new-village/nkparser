'''load.py
'''
import json
import re
import time
from random import randrange

import requests

from nkparser.help import load_config
from nkparser.parse import parse_json, parse_text


def load(data_type, entity_id):
    """ Load netkeiba.com data.
    :param data_type: data type of target such as ENTRY, RESULT, ODDS and HORSE
    :param entity_id: entity id of target such as race id or horse id
    :return: :class:`Response <Response>` object
    """
    if data_type == "entry":
        loader = EntryLoader(data_type, entity_id)
    elif data_type == "odds":
        loader = OddsLoader(data_type, entity_id)
    elif data_type == "result":
        loader = ResultLoader(data_type, entity_id)
    elif data_type == "horse":
        loader = HorseLoader(data_type, entity_id)
    else:
        raise ValueError(f"Unexpected data type: {data_type}")

    return loader.exec()

def load_contents(url, mode="html"):
    """ Load contents
    """
    try:
        # Request Contents
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        response = response.text
    except requests.exceptions.RequestException as exp:
        raise SystemExit(f"Request to {url} has been failure") from exp

    return odds_error_check(response, url) if mode == "json" else response

def odds_error_check(response, url):
    """ Check odds json error
    """
    entity_id = re.findall(r"\d{12}", url)[0]

    # Confirme Data Format
    if json.loads(response)['status'] == 'middle':
        # HTTP Response is not 200 (Normal)
        raise SystemExit(f"There is no odds data: {entity_id}")

    return response

def create_url(base_url, entity_id):
    """ repleace entity id from base_url
    :param base_url: base url for replace target
    :param entity_id: replace item for {ID} string
    :return str
    """
    return base_url.replace('{ID}', entity_id)

class NkLoader():
    """ base class of Loaders """
    def __init__(self, data_type, entity_id):
        self.data_type = data_type
        self.entity_id = entity_id
        self.property = load_config(self.data_type)["property"]
        url = create_url(self.property["url"], entity_id)
        self.text = load_contents(url, self.property["mode"])
        self.info = None
        self.table = None
        time.sleep(randrange(3, 6))

class EntryLoader(NkLoader):
    """ Entry data Loader """
    def exec(self):
        """ Description
        """
        self.info = parse_text("race", self.text, self.entity_id)
        self.table = parse_text("entry", self.text, self.entity_id)
        return self

class OddsLoader(NkLoader):
    """ Odds data Loader """
    def exec(self):
        """ Description
        """
        self.table = parse_json("odds", self.text, self.entity_id)
        return self

class ResultLoader(NkLoader):
    """ Result data Loader """
    def exec(self):
        """ Description
        """
        self.table = parse_text("result", self.text, self.entity_id)
        return self

class HorseLoader(NkLoader):
    """ Horse data Loader """
    def exec(self):
        """ Description
        """
        self.info = parse_text("horse", self.text, self.entity_id)
        self.table = parse_text("history", self.text, self.entity_id)
        return self

class CalLoader():
    """ Entry data Loader """
    def __init__(self, year, month):
        url = f"https://keiba.yahoo.co.jp/schedule/list/{year}/?month={month}"
        self.text = load_contents(url)
        self.table = None

    def exec(self):
        """ Description
        """
        self.table = parse_text("cal", self.text)
        return self.table
