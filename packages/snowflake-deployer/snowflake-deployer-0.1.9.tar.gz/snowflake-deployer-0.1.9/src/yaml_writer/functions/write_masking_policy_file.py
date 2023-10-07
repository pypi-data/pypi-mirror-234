from pathlib import Path
import yaml
#import ruamel.yaml
import src.common.processing_vars as var
def write_masking_policy_file(self, database_name_sans_env:str, schema_name:str, d:dict):
    base_path = 'snowflake/data/' + database_name_sans_env + '/' + schema_name + '/MASKING_POLICIES/' + database_name_sans_env + '__' + schema_name + '__' + d['MASKING_POLICY_NAME']
    yml_path = base_path + '.yml'

    ext = 'sql'
    body_path = base_path + '.' + ext
    
    data = self.create_parent_load_data(yml_path)

    data['SIGNATURE'] = self.choose_value_list_of_objects(data, 'SIGNATURE', d,'SIGNATURE', var.EMPTY_LIST)
    data['RETURN_TYPE'] = self.choose_value_string(data, 'RETURN_TYPE', d, 'RETURN_TYPE', var.EMPTY_STRING)
    data['EXEMPT_OTHER_POLICIES'] = self.choose_value_string(data, 'EXEMPT_OTHER_POLICIES', d, 'EXEMPT_OTHER_POLICIES', var.EMPTY_STRING)
    data['OWNER'] = self.choose_value_string(data, 'OWNER', d, 'OWNER', var.EMPTY_STRING)
    data['COMMENT'] = self.choose_value_string(data, 'COMMENT', d, 'COMMENT', var.EMPTY_STRING)
    #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    #print(data['TAGS'])
    #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    #print(d['TAGS'])
    #print('#################################################')
    body = d['BODY']
    if d['TAGS'] != []:
        if 'TAGS' in data:
            data['TAGS'] = self.choose_list_objects(d['TAGS'], data['TAGS'])
        else:
            data['TAGS'] = d['TAGS']
    else:
        data['TAGS']=var.EMPTY_STRING

    if d['GRANTS'] != []:
        if 'GRANTS' in data:
            data['GRANTS'] = self.choose_list_objects(d['GRANTS'], data['GRANTS'])
        else:
            data['GRANTS'] = d['GRANTS']
    else:
        data['GRANTS']=var.EMPTY_STRING

    #ryaml = ruamel.yaml.YAML(typ=['rt', 'string'])
    #yaml_string = ryaml.dump_to_string(data)
    yaml_string = yaml.dump(data, sort_keys=False)
    
    #yaml_string_converted = self.replace_jinja_ref_string(yaml_string)
    #yaml_string_converted = self.replace_jinja_list(yaml_string_converted)
    #yaml_string_converted = yaml_string_converted.replace("'"+var.EMPTY_STRING+"'",'')
    yaml_string_converted = self.convert_special_characters_back_in_file(yaml_string)
    
    # write YAML path
    with open(yml_path, "w+") as fl:
        fl.write(yaml_string_converted)

    # write body path 
    with open(body_path, "w+") as fb:
        fb.write(body)
