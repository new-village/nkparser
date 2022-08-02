import re

def formatter(reg, target, type):
    # Extract target variables
    fmt = re.compile(reg)
    val = fmt.findall(target)[0] if target is not None and fmt.search(target) else None

    # # Redact comma from numerical values
    if type == "int" or type == "float":
        if val is None:
            val = 0
        else:
            val = re.sub(",", "", val)

    # Convert type
    if type == "int":
        value = int(val) if val is not None else 0
    elif type == "float":
        value = float(val) if val is not None else 0
    elif type == "str":
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
