from pathlib import Path
import yaml
#import ruamel.yaml
import src.common.processing_vars as var
def write_tag_file(self,database_name:str, schema_name:str, d: dict):
    yml_path = 'snowflake/data/' + database_name + '/' + schema_name + '/TAGS/' + database_name + '__' + schema_name + '__' + d['TAG_NAME'] + '.yml'
    #print('@@@@@@@@ WRITE TAG @@@@@@@@@@@@@@@@@')
    #print(d)
    
    data = self.create_parent_load_data(yml_path)

    data['COMMENT'] = self.choose_value_string(data, 'COMMENT', d,'COMMENT', var.EMPTY_STRING)
    data['OWNER'] = self.choose_value_string(data, 'OWNER', d,'OWNER', var.EMPTY_STRING)
    data['ALLOWED_VALUES']=self.choose_value_list(data, 'ALLOWED_VALUES', d,'ALLOWED_VALUES', var.EMPTY_LIST)
    data['MASKING_POLICIES']=self.choose_value_list(data, 'MASKING_POLICIES', d,'MASKING_POLICIES', var.EMPTY_LIST)
    
    #print(data)
    #print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    #if tag['ALLOWED_VALUES'] != []:
    #    data['ALLOWED_VALUES']=tag['ALLOWED_VALUES'] 
    #else:
    #    if 'ALLOWED_VALUES' in data:
    #        del data['ALLOWED_VALUES']
    #if 'RENAME' in data:
    #    del data['RENAME']

    #ryaml = ruamel.yaml.YAML(typ=['rt', 'string'])
    #yaml_string = ryaml.dump_to_string(data)
    yaml_string = yaml.dump(data, sort_keys=False)
    #yaml_string_converted = self.replace_jinja_ref_string(yaml_string)
    #yaml_string_converted = yaml_string_converted.replace("'"+var.EMPTY_STRING+"'",'')
    yaml_string_converted = self.convert_special_characters_back_in_file(yaml_string)
    
    with open(yml_path, "w+") as f:
        f.write(yaml_string_converted)

    #with Path(yml_path).open("w", encoding="utf-8") as f:
    #    yaml.dump(data,f,default_style=None,default_flow_style=False, sort_keys=False)
    #    #f.write('#RENAME: #uncomment with new name to rename')

    


