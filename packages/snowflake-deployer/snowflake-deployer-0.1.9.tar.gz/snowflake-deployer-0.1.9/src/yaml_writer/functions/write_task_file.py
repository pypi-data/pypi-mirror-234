from pathlib import Path
import yaml
#import ruamel.yaml
import src.common.processing_vars as var
def write_task_file(self, database_name_sans_env:str, schema_name:str, d:dict):
    base_path = 'snowflake/data/' + database_name_sans_env + '/' + schema_name + '/TASKS/' + database_name_sans_env + '__' + schema_name + '__' + d['TASK_NAME']
    yml_path = base_path + '.yml'

    ext = 'sql'
    body_path = base_path + '.' + ext
    
    data = self.create_parent_load_data(yml_path)
    data['WAREHOUSE'] = self.choose_value_string(data, 'WAREHOUSE', d,'WAREHOUSE', var.EMPTY_STRING)
    data['SCHEDULE'] = self.choose_value_string(data, 'SCHEDULE', d,'SCHEDULE', var.EMPTY_STRING)
    data['ALLOW_OVERLAPPING_EXECUTION'] = self.choose_value_string(data, 'ALLOW_OVERLAPPING_EXECUTION', d,'ALLOW_OVERLAPPING_EXECUTION', var.EMPTY_STRING)
    data['PREDECESSORS'] = self.choose_value_list(data, 'PREDECESSORS', d,'PREDECESSORS', var.EMPTY_LIST)
    data['ERROR_INTEGRATION'] = self.choose_value_string(data, 'ERROR_INTEGRATION', d,'ERROR_INTEGRATION', var.EMPTY_STRING)
    data['OWNER'] = self.choose_value_string(data, 'OWNER', d,'OWNER', var.EMPTY_STRING)
    data['COMMENT'] = self.choose_value_string(data, 'COMMENT', d,'COMMENT', var.EMPTY_STRING)
    data['ENABLED'] = self.choose_value_string(data, 'ENABLED', d,'ENABLED', var.EMPTY_STRING)
    data['CONDITION'] = self.choose_value_string(data, 'CONDITION', d,'CONDITION', var.EMPTY_STRING)
    data['USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE'] = self.choose_value_string(data, 'USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE', d,'USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE', var.EMPTY_STRING)
    data['USER_TASK_TIMEOUT_MS'] = self.choose_value_string(data, 'USER_TASK_TIMEOUT_MS', d,'USER_TASK_TIMEOUT_MS', var.EMPTY_STRING)
    data['SUSPEND_TASK_AFTER_NUM_FAILURES'] = self.choose_value_string(data, 'SUSPEND_TASK_AFTER_NUM_FAILURES', d,'SUSPEND_TASK_AFTER_NUM_FAILURES', var.EMPTY_STRING)
    data['ENABLED'] = self.choose_value_string(data, 'ENABLED', d,'ENABLED', var.EMPTY_STRING)

    body = d['DEFINITION']
    
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
