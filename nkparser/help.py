''' helper.py
'''
import json
import os
import re

from bs4 import Tag
from datetime import datetime as dt

import nkparser

RAP_TIME = 0.0

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
            val = re.sub(",", "", val) if val is not None else None

    # Convert type
    if type_string == "integer":
        value = int(val) if val is not None else None
    elif type_string == "real":
        value = float(val) if val is not None else None
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
    if len(time_list) == 1:
        return time_list[0]
    else:
        return arg.text

def zero_suppress(arg:str) -> str:
    """
    Suppress zero from string numbers
    Example
    --------
    >>> zero_suppress('03')
        3
    """
    return str(int(arg))

def zero_fill(value:float) -> float:
    """
    Convert None to Zero Integer
    Example
    --------
    >>> zero_fill(None)
        0
    """
    return value if value is not None else 0.0

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

def set_diff_time(value:tuple) -> float:
    """ diff rap time from rank 1 time
    :param value: Tuple object includes RANK and RAP TIME.
    :return:
    """
    if value[0] == 1 and value[1] is not None:
        global RAP_TIME
        RAP_TIME = value[1]
        diff_time = 0
    elif value[0] != 1 and value[1] is not None:
        diff_time = round(value[1] - RAP_TIME, 1)
    else:
        diff_time = None

    return diff_time

def classify_length(length:int) -> str:
    """ description
    """
    if length < 1400:
        classification = "Sprint"
    elif 1400 <= length < 1800:
        classification = "Mile"
    elif 1800 <= length < 2200:
        classification = "Intermediate"
    elif 2200 <= length < 2800:
        classification = "Long"
    elif length >= 2800:
        classification = "Extended"

    return classification

def concatinate(value:tuple) -> str:
    """ Concatinate arguments
    :param value: Tuple of strings to be concatinated.
    :return: Str object
    """
    return "".join(map(str, value))

def fmt_date(dt_str:str) -> str:
    """ Convert YYYYMMDD date string to YYYY-MM-DD string
    :param fmt_date: YYYYMMDD date string
    :return: Str object
    """
    return dt.strptime(dt_str, "%Y%m%d").strftime('%Y-%m-%d')

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
