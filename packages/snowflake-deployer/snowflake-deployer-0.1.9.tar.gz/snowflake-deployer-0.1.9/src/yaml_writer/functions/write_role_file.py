from pathlib import Path
import yaml
#from ruamel.yaml import YAML as RUAMEL_YAML
#import ruamel.yaml
import src.common.processing_vars as var
def write_role_file(self, d:dict):
    yml_path = 'snowflake/account/roles/' + d['ROLE_NAME_SANS_ENV'] + '.yml'
    
    data = self.create_parent_load_data(yml_path)

    data['OWNER'] = self.choose_value_string(data, 'OWNER', d,'OWNER', var.EMPTY_STRING)
    data['COMMENT'] = self.choose_value_string(data, 'COMMENT', d, 'COMMENT', var.EMPTY_STRING)
    data['PARENT_ROLES'] = self.choose_value_string(data, 'PARENT_ROLES', d, 'PARENT_ROLES', var.EMPTY_STRING)
    
    if d['TAGS'] != []:
        if 'TAGS' in data:
            data['TAGS'] = self.choose_list_objects(d['TAGS'], data['TAGS'])
        else:
            data['TAGS'] = d['TAGS'] 
    else:
        data['TAGS']=var.EMPTY_STRING

    #ryaml = ruamel.yaml.YAML(typ=['rt', 'string'])
    #ryaml = RUAMEL_YAML(typ=['rt', 'string'])
    #yaml_string = ryaml.dump_to_string(data)
    yaml_string = yaml.dump(data, sort_keys=False)
    #yaml_string_converted = self.replace_jinja_ref_string(yaml_string)
    #yaml_string_converted = yaml_string_converted.replace("'"+var.EMPTY_STRING+"'",'')
    yaml_string_converted = self.convert_special_characters_back_in_file(yaml_string)
    with open(yml_path, "w+") as f:
        f.write(yaml_string_converted)
