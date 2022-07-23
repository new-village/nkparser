import re

def formatter(reg, target, type):
    # Extract target variables
    fmt = re.compile(reg)
    val = fmt.findall(target)[0] if target is not None and fmt.search(target) else None

    # # Redact comma from numerical values
    # if type == "int" or type == "float":
    #     if val is None:
    #         val = 0
    #     else:
    #         val = re.sub(",", "", val)
    
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