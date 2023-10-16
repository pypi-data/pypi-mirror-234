from functools import lru_cache
import typing


def rough_check_drill_string(string :str):
    if "{" not in string:
        return False
    
    if "}" not in string:
        return False
    
    if ":" not in string:
        return False

    return True

@lru_cache
def prune_drill_string(string :str):
    # remove all bracketed parts
    newstring = ""
    bracketed = False

    for c in string:
        if c == "{":
            bracketed = True
        elif c == "}":
            bracketed = False
        elif not bracketed:
            newstring += c

    return newstring

@lru_cache
def get_drill_vars(string : str):
    var_details : dict = {}
    raw_string = ""
    
    temp_key  =""
    temp_value = ""
    pass_colon = False
    bracket_open = False
    for c in string:
        match c:
            case "{" if bracket_open:
                return -2, None, None
            case "}" if not bracket_open:
                return -2, None, None
            case "{":
                bracket_open = True
                raw_string += c
            case "}" if not pass_colon:
                return -3, None, None
            case "}":
                bracket_open = False
                var_details[temp_key] = temp_value
                temp_key = ""
                temp_value = ""
                pass_colon = False
            case ":":
                pass_colon = True
                raw_string += temp_key + "}"    
            case str(c) if not pass_colon and bracket_open:
                temp_key += c
            case str(c) if pass_colon and bracket_open:
                temp_value += c
            case _:
                raw_string += c

    return 1, var_details, raw_string

def parse_string(string : str, drills : typing.List[str]) -> typing.Tuple[str, int]:
    if not rough_check_drill_string(string):
        return string, 0
    
    if not any([drill in string for drill in drills]):
        return prune_drill_string(string), 2
    
    status, details, raw_string = get_drill_vars(string)
    if status != 1:
        return None, status

    filtered_details = {}
    for k, v in details.items():
        if k in drills:
            filtered_details[k] = v
        else:
            filtered_details[k] = ""

    return raw_string.format(**filtered_details), 1