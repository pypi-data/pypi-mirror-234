from pathlib import Path
import yaml
#import ruamel.yaml
import src.common.processing_vars as var
def write_object_file(self,database_name:str, schema_name:str, d: dict, object_metadata_only: bool):
    yml_path = 'snowflake/data/' + database_name + '/' + schema_name + '/OBJECTS/' + database_name + '__' + schema_name + '__' + d['OBJECT_NAME'] + '.yml'
    
    data = self.create_parent_load_data(yml_path)

    data['OBJECT_TYPE']=self.choose_value_string(data, 'OBJECT_TYPE', d,'OBJECT_TYPE', var.EMPTY_STRING)
    data['COMMENT']=self.choose_value_string(data, 'COMMENT', d,'COMMENT', var.EMPTY_STRING)
    data['OWNER']=self.choose_value_string(data, 'OWNER', d,'OWNER', var.EMPTY_STRING)
    data['RETENTION_TIME_IN_DAYS'] = self.choose_value_string(data, 'RETENTION_TIME_IN_DAYS', d,'RETENTION_TIME_IN_DAYS', var.EMPTY_STRING)
    
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

    data['COLUMNS'] = d['COLUMNS']
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

    


