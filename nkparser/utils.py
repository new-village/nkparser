''' utilities
'''
import logging
from nkparser.help import load_config

# Set Logger
logger = logging.getLogger('NkParser')

def create_table_sql(data_type=None):
    ''' Create Tables Strings
    The function generate create table SQL strings based on SQLite3 by config file.

    Args:
        data_type (str): Data Type is identifier of data types such as ENTRY, ODDS, RACE and RESULT.
    '''
    # Validating Arguments
    if data_type is None:
        logger.error('There is no race_id in HTML')
        raise SystemExit

    # load config file
    keys = [key for key in load_config(data_type).keys()]
    types = [val['var_type'] for val in load_config(data_type).values()]
    # Convert non-support data type to text
    types = ['text' if t in ['url', 'name'] else t for t in types]
    # Create comma separated strings
    cols = [k + ' ' + v for k, v in zip(keys, types)]
    cols = ", ".join(cols)

    return f"CREATE TABLE IF NOT EXISTS {data_type} ({cols});"
