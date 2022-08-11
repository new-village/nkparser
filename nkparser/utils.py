""" utils
"""
from nkparser.help import load_config
from nkparser.load import CalLoader

def create_table_sql(data_type=None):
    """ The function generate create table SQL strings based on SQLite3 by config file.
    :param data_type: Data Type is identifier of data types such as ENTRY, ODDS, RACE and RESULT.
    """
    # Validating Arguments
    if data_type is None:
        raise SystemExit("There is no race_id in HTML")

    # load config file
    keys = [key for key in load_config(data_type).keys()]
    types = [val['var_type'] for val in load_config(data_type).values()]
    # Create comma separated strings
    cols = [k + ' ' + v for k, v in zip(keys, types)]
    # Add PRIMARY KEY string to first column
    cols[0] = cols[0] + " PRIMARY KEY"
    cols = ", ".join(cols)

    return f"CREATE TABLE IF NOT EXISTS {data_type} ({cols});"

def create_index_sql(data_type=None):
    """ The function generate create index SQL strings based on SQLite3 by config file.
    :param data_type: Data Type is identifier of data types such as ENTRY, ODDS, RACE and RESULT.
    """
    # Validating Arguments
    if data_type == "ENTRY":
        sql = "CREATE INDEX IF NOT EXISTS race_id ON ENTRY (race_id); " \
        "CREATE INDEX IF NOT EXISTS horse_id ON ENTRY (horse_id);"
    elif data_type == "ODDS":
        sql = ""
    elif data_type == "RESULT":
        sql = "CREATE INDEX IF NOT EXISTS race_id ON RESULT (race_id); z" \
        "CREATE INDEX IF NOT EXISTS horse_id ON RESULT (horse_id);"
    elif data_type == "HORSE":
        sql = ""
    else:
        raise ValueError(f"Unexpected data type: {data_type}")

    return sql


def race_list(year:int, month:int) -> list:
    """ collect arguments race id.
    :param year: target year
    :param month: target month
    """
    calc = CalLoader(year, month)
    return calc.exec()