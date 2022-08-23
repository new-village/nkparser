''' helper.py
'''
import json
import os
import re

import requests
from bs4 import Tag

import nkparser


def load_html(url):
    """ load netkeiba HTML
    :param url: target url
    :return str
    """
    response = requests.get(url)
    response.encoding = response.apparent_encoding

    # Response Status Confirmation
    if response.status_code not in [200]:
        # HTTP Response is not 200 (Normal)
        raise SystemExit(f"Request to {url} has been failure: {response.status_code}")

    return response.text

def load_json(url):
    """ load netkeiba JSON
    :param url: target url
    :return str
    """
    race_id = re.findall(r"\d{12}", url)[0]
    text = json.loads(load_html(url))

    # Confirme Data Format
    if text['status'] == 'middle':
        # HTTP Response is not 200 (Normal)
        raise SystemExit(f"There is no odds data: {race_id}")

    text.update({'race_id': race_id})
    return json.dumps(text)

def create_url(base_url, entity_id):
    """ repleace entity id from base_url
    :param base_url: base url for replace target
    :param entity_id: replace item for {ID} string
    :return str
    """
    return base_url.replace('{ID}', entity_id)


def formatter(reg, target:str, type_string:str):
    '''
    Convert string to defined type
    Example
    --------
    >>> formatter(r'\d+', '3,000', 'integer')
        3000
    '''
    # Extract target variables
    fmt = re.compile(reg)
    val = fmt.findall(target)[0] if target is not None and fmt.search(target) else None

    # # Redact comma from numerical values
    if type_string == "integer" or type_string == "real":
        if val is None:
            val = 0
        else:
            val = re.sub(",", "", val)

    # Convert type
    if type_string == "integer":
        value = int(val) if val is not None else 0
    elif type_string == "real":
        value = float(val) if val is not None else 0
    elif type_string == "text":
        value = str(val) if val is not None else ""
    else:
        value = val

    return value

def time_to_seconds(arg) -> str:
    """
    Convert string time that type 1:36.3 in Netkeiba.com data to seconds
    Example
    --------
    >>> time_to_seconds('1:23.4')
        83.4
    """
    time_list = arg.text.split(':')
    if len(time_list) == 2:
        return str(float(time_list[0]) * 60 + float(time_list[1]))
    else:
        return arg

def zero_suppress(arg:str) -> str:
    """
    Suppress zero from string numbers
    Example
    --------
    >>> zero_suppress('03')
        3
    """
    return str(int(arg))

def get_title(soup:Tag) -> str:
    """ description
    """
    return soup.get("title") if soup is not None else None

def get_url(soup:Tag) -> str:
    """ description
    """
    return soup.get("href") if soup is not None else None

def create_uid(value:tuple) -> str:
    """ Concatinating entry_id and 2 digits horse_number
    :param value: Tuple object includes Entity ID of str and Horse Number of int.
    :return: Str object
    """
    return value[0] + str(value[1]).zfill(2)

def set_prize(soup:Tag, run:list) -> list:
    """ description
    """
    # Add prize
    prize_text = formatter(r'本賞金:(.+)万円', soup.select_one('.RaceData02').text, 'str').split(',')
    prize = [int(p) for p in prize_text] + [0] * (len(run) - len(prize_text))
    return [{**r, **p} for r, p in zip(run, [{"prize": p} for p in prize])]

def load_config(data_type:str) -> str:
    """ The function loads configuration file from config directory
    :param data_type: Category is identifier of data types such as ENTRY, ODDS, RACE and RESULT.
    """
    try:
        dir_location = os.path.dirname(nkparser.__file__) + '/config/'
        with open(dir_location + data_type + '.json', 'r', encoding='UTF-8') as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        raise SystemExit(f'Config file decode error: {exc}') from exc
    except FileNotFoundError as exc:
        raise SystemExit(f'Config file not found: {exc}') from exc
