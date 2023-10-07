from pathlib import Path
import yaml
#import ruamel.yaml
import src.common.processing_vars as var
def write_warehouse_file(self, d:dict):
    yml_path = 'snowflake/account/warehouses/' + d['WAREHOUSE_NAME_SANS_ENV'] + '.yml'
    
    data = self.create_parent_load_data(yml_path)
    data['WAREHOUSE_TYPE'] = self.choose_value_string(data, 'WAREHOUSE_TYPE', d,'WAREHOUSE_TYPE', var.EMPTY_STRING)
    data['WAREHOUSE_SIZE'] = self.choose_value_string(data, 'WAREHOUSE_SIZE', d,'WAREHOUSE_SIZE', var.EMPTY_STRING)
    data['MIN_CLUSTER_COUNT'] = self.choose_value_string(data, 'MIN_CLUSTER_COUNT', d,'MIN_CLUSTER_COUNT', var.EMPTY_STRING)
    data['MAX_CLUSTER_COUNT'] = self.choose_value_string(data, 'MAX_CLUSTER_COUNT', d,'MAX_CLUSTER_COUNT', var.EMPTY_STRING)
    data['SCALING_POLICY'] = self.choose_value_string(data, 'SCALING_POLICY', d,'SCALING_POLICY', var.EMPTY_STRING)
    data['AUTO_SUSPEND'] = self.choose_value_string(data, 'AUTO_SUSPEND', d,'AUTO_SUSPEND', var.EMPTY_STRING)
    data['AUTO_RESUME'] = self.choose_value_string(data, 'AUTO_RESUME', d,'AUTO_RESUME', var.EMPTY_STRING)
    #data['RESOURCE_MONITOR'] = wh['RESOURCE_MONITOR']
    data['OWNER'] = self.choose_value_string(data, 'OWNER', d,'OWNER', var.EMPTY_STRING)
    data['COMMENT'] = self.choose_value_string(data, 'COMMENT', d,'COMMENT', var.EMPTY_STRING)
    data['ENABLE_QUERY_ACCELERATION'] = self.choose_value_string(data, 'ENABLE_QUERY_ACCELERATION', d,'ENABLE_QUERY_ACCELERATION', var.EMPTY_STRING)
    data['QUERY_ACCELERATION_MAX_SCALE_FACTOR'] = self.choose_value_string(data, 'QUERY_ACCELERATION_MAX_SCALE_FACTOR', d,'QUERY_ACCELERATION_MAX_SCALE_FACTOR', var.EMPTY_STRING)

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

    
    #grant['GRANT_TO'] = g['GRANTEE_NAME']
    #grant['GRANT_PRIVILEGE'] = g['PRIVILEGE']
    #grant['GRANT_OPTION'] = g['GRANT_OPTION']

    #ryaml = ruamel.yaml.YAML(typ=['rt', 'string'])
    #yaml_string = ryaml.dump_to_string(data)
    yaml_string = yaml.safe_dump(data, sort_keys=False)
    
    #yaml_string_converted = self.replace_jinja_ref_string(yaml_string)
    #yaml_string_converted = yaml_string_converted.replace("'"+var.EMPTY_STRING+"'",'')
    yaml_string_converted = self.convert_special_characters_back_in_file(yaml_string)
    
    with open(yml_path, "w+") as f:
        f.write(yaml_string_converted)
