from pathlib import Path
import yaml
#import ruamel.yaml
import src.common.processing_vars as var
def write_procedure_file(self, database_name_sans_env:str, schema_name:str, d:dict):
    base_path = 'snowflake/data/' + database_name_sans_env + '/' + schema_name + '/PROCEDURES/' + database_name_sans_env + '__' + schema_name + '__' + d['PROCEDURE_NAME_SANS_ENV'] + '__' + d['PROCEDURE_SIGNATURE_TYPES']
    yml_path = base_path + '.yml'
    
    if d['LANGUAGE'].upper() == 'PYTHON':
        ext = 'py'
    if d['LANGUAGE'].upper() == 'JAVASCRIPT':
        ext = 'js'
    elif d['LANGUAGE'].upper() == 'SQL':
        ext = 'sql'
    elif d['LANGUAGE'].upper() == 'JAVA':
        ext = 'java'
    elif d['LANGUAGE'].upper() == 'SCALA':
        ext = 'scala'
    
    body_path = base_path + '.' + ext
    
    data = self.create_parent_load_data(yml_path)

    #data['SIGNATURE'] = p['SIGNATURE']
    data['INPUT_ARGS'] = self.choose_value_list_of_objects(data, 'INPUT_ARGS', d,'INPUT_ARGS', var.EMPTY_LIST)
    #data['INPUT_ARGS'] = self.choose_list_objects(d['RETURNS'], data['RETURNS'])
    data['RETURNS'] = self.choose_value_string(data, 'RETURNS', d,'RETURNS', var.EMPTY_STRING)
    data['LANGUAGE'] = self.choose_value_string(data, 'LANGUAGE', d,'LANGUAGE', var.EMPTY_STRING)
    #data['NULL_HANDLING'] = p['NULL HANDLING']
    data['EXECUTE_AS'] = self.choose_value_string(data, 'EXECUTE_AS', d,'EXECUTE AS', var.EMPTY_STRING)
    data['OWNER'] = self.choose_value_string(data, 'OWNER', d,'OWNER', var.EMPTY_STRING)
    data['COMMENT'] = self.choose_value_string(data, 'COMMENT', d,'COMMENT', var.EMPTY_STRING)
    data['IS_SECURE'] = True if d['IS_SECURE'] == 'Y' else False

    if data['LANGUAGE'] == 'PYTHON':
        data['IMPORTS'] = self.choose_value_list(data, 'IMPORTS', d,'IMPORTS', var.EMPTY_LIST)
        data['HANDLER'] = self.choose_value_string(data, 'HANDLER', d,'HANDLER', var.EMPTY_STRING)
        data['RUNTIME_VERSION'] = self.choose_value_string(data, 'RUNTIME_VERSION', d,'RUNTIME_VERSION', var.EMPTY_STRING)
        data['PACKAGES'] = self.choose_value_list(data, 'PACKAGES', d,'PACKAGES', var.EMPTY_LIST)
        #data['INSTALLED_PACKAGES'] = p['INSTALLED_PACKAGES'] if 'INSTALLED_PACKAGES' in p else None
    #data['BODY'] = '||$$' + p['BODY'] + '$$||'
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
    #yaml_string_converted = self.replace_jinja_multiline_string(yaml_string_converted)
    #yaml_string_converted = self.replace_jinja_list(yaml_string_converted)
    #yaml_string_converted = yaml_string_converted.replace("'"+var.EMPTY_STRING+"'",'')
    yaml_string_converted = self.convert_special_characters_back_in_file(yaml_string)
    
    #yaml_string_converted = yaml_string_converted.replace("'||REPLACE_BODY||'",'|\n'+p['BODY'])
    #if data['LANGUAGE'] == 'PYTHON':
    #    print(yaml_string_converted)
    #    print('#######################################')
    #if data['LANGUAGE'] == 'PYTHON':
    #    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    #    print(yaml_string_converted)
    #    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    
    # write YAML path
    with open(yml_path, "w+") as f:
        f.write(yaml_string_converted)

    # write body path 
    with open(body_path, "w+") as fb:
        fb.write(body)
# Javascript
# CREATE [ OR REPLACE ] [ SECURE ] PROCEDURE <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
#   [ COPY GRANTS ]
#   RETURNS <result_data_type> [ NOT NULL ]
#   LANGUAGE JAVASCRIPT
#   [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
#   [ VOLATILE | IMMUTABLE ] -- Note: VOLATILE and IMMUTABLE are deprecated.
#   [ COMMENT = '<string_literal>' ]
#   [ EXECUTE AS { CALLER | OWNER } ]
#   AS '<procedure_definition>'

# Python
# CREATE [ OR REPLACE ] [ SECURE ] PROCEDURE <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
#   [ COPY GRANTS ]
#   RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
#   LANGUAGE PYTHON
#   RUNTIME_VERSION = '<python_version>'
#   PACKAGES = ( 'snowflake-snowpark-python[==<version>]'[, '<package_name>[==<version>]` ... ])
#   [ IMPORTS = ( '<stage_path_and_file_name_to_read>' [, '<stage_path_and_file_name_to_read>' ...] ) ]
#   HANDLER = '<function_name>'
#   [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
#   [ VOLATILE | IMMUTABLE ] -- Note: VOLATILE and IMMUTABLE are deprecated.
#   [ COMMENT = '<string_literal>' ]
#   [ EXECUTE AS { CALLER | OWNER } ]
#   AS '<procedure_definition>'

# CREATE [ OR REPLACE ] PROCEDURE <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
#   [ COPY GRANTS ]
#   RETURNS { <result_data_type> | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
#   [ NOT NULL ]
#   LANGUAGE SQL
#   [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
#   [ VOLATILE | IMMUTABLE ] -- Note: VOLATILE and IMMUTABLE are deprecated.
#   [ COMMENT = '<string_literal>' ]
#   [ EXECUTE AS { CALLER | OWNER } ]
#   AS <procedure_definition>