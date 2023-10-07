import json

def get_sf_database_name(name:str, prefix:str):
    if prefix is None:
        rtn = name 
    else:
        rtn = prefix + name
    return rtn

def get_sf_role_name(name:str, prefix:str):
    if prefix is None:
        rtn = name 
    else:
        rtn = prefix + name
    return rtn

def get_sf_warehouse_name(name:str, prefix:str):
    if prefix is None:
        rtn = name 
    else:
        rtn = prefix + name
    return rtn 

def hash_yml_data(yml_data):
    return hash(json.dumps(yml_data))
