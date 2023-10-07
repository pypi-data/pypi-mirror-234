def remove_prefix(text:str, prefix:str)->str:
    return text[text.startswith(prefix) and len(prefix):]

def cast_string_to_bool(str_to_cast: str)->bool:
    if str_to_cast.upper() == 'TRUE':
        rtn = True
    elif str_to_cast.upper() == 'FALSE':
        rtn = False
    else:
        rtn = None
    return rtn