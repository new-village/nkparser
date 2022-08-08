''' helper.py
'''
import json
import logging
import os
import re
import nkparser

# Set Logger
logger = logging.getLogger('NkParser')

def formatter(reg, target, type_string):
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

def time_to_seconds(arg):
    '''
    Convert string time that type 1:36.3 in Netkeiba.com data to seconds
    Example
    --------
    >>> time_to_seconds('1:23.4')
        83.4
    '''
    time_list = arg.split(':')
    if len(time_list) == 2:
        return float(time_list[0]) * 60 + float(time_list[1])
    elif len(time_list) == 1:
        return float(time_list[1])
    else:
        return arg

def zero_suppress(arg):
    '''
    Suppress zero from string numbers
    Example
    --------
    >>> zero_suppress('03')
        3
    '''
    if isinstance(arg, str):
        return str(int(arg))
    else:
        return arg

def load_config(data_type):
    ''' load_config
    The function loads configuration file from config directory

    Args:
        data_type (str): Category is identifier of data types such as ENTRY, ODDS, RACE and RESULT.
    '''
    try:
        dir_location = os.path.dirname(nkparser.__file__) + '/config/'
        with open(dir_location + data_type + '.json', 'r', encoding='UTF-8') as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        # Raise error and abort script
        logger.error('Config file decode error: %s', exc)
        raise SystemExit() from exc
    except FileNotFoundError as exc:
        logger.error('Config file not found: %s', exc)
        raise SystemExit() from exc