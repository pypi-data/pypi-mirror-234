from pathlib import Path
import yaml
import os
import json
#import ruamel.yaml
import src.common.processing_vars as var
class yaml_writer:
    #def __init__(self):
        
    from .functions.write_database_file import write_database_file
    from .functions.write_function_file import write_function_file
    from .functions.write_masking_policy_file import write_masking_policy_file
    from .functions.write_object_file import write_object_file
    from .functions.write_procedure_file import write_procedure_file
    from .functions.write_role_file import write_role_file
    from .functions.write_row_access_policy_file import write_row_access_policy_file
    from .functions.write_schema_file import write_schema_file
    from .functions.write_tag_file import write_tag_file
    from .functions.write_task_file import write_task_file
    from .functions.write_warehouse_file import write_warehouse_file

    def create_parent_load_data(self,yml_path: str)->dict:
        db_file_exists = os.path.isfile(yml_path)
        db_output_file = Path(yml_path)

        # Create directory if not exists
        if not db_file_exists:
            db_output_file.parent.mkdir(exist_ok=True, parents=True)
            data = {}
        # Else read current config to baseline from current file
        else:
            #yaml = ruamel.yaml.YAML(typ='safe')
            #ryaml = ruamel.yaml.YAML()
            #ryaml = ruamel_yaml.YAML()
            with open(yml_path, "r") as yamlfile:
                #data_raw = yamlfile.read().replace('{{', '<~<~').replace('}}', '~>~>') #.replace("'", "!!|!!")
                #data = dict(ryaml.load(data_raw))
                #data = dict(ryaml.load(yamlfile))
                
                #data = dict(yaml.safe_load(yamlfile))
                #print(data)
                #data = yaml.load(yamlfile, Loader=yaml.FullLoader)
                data_raw = yamlfile.read().replace('{{', var.DOUBLE_LEFT_BRACKETS).replace('}}', var.DOUBLE_RIGHT_BRACKETS).replace('#',var.HASH_TAG)#.replace("'",var.SINGLE_QUOTE)
            data = dict(yaml.load(data_raw, Loader=yaml.FullLoader))  
            #print('############ ^^ ################')
            #print(yml_path)
            #print(data_raw)
            #print(data)
            #print('############ end ############')
        return data

    #def replace_jinja_ref_string(self, yaml_string:str):
    #    # I believe this is no longer used now?
    #    output = yaml_string.replace("'!!{{!!","{{")
    #    output = output.replace("!!}}!!'", "}}")
    #    output = output.replace("<~<~","{{")
    #    output = output.replace("~>~>","}}")
    #    output = output.replace("!!|!!","'")
    #    return output
    
    #def replace_jinja_multiline_string(self, yaml_string:str):
    #    output = yaml_string.replace("'||$$",'|\n')
    #    output = output.replace("$$||'","")
    #    output = output.replace('"||$$','|\n')
    #    output = output.replace('$$||"',"")
    #    output = output.replace('\"','"')
    #    return output
    
    #def replace_jinja_list(self, yaml_string:str):
    #    # Don't think this one is used either
    #    output = yaml_string.replace("'[","[")
    #    output = output.replace("]'","]")
    #    output = output.replace("''","'")
    #    return output

    def create_jinja_var(self, var_name:str):
        #return "!!{{!!" + var_name + "!!}}!!"
        return "<~<~" + var_name + "~>~>"
    
    def convert_for_yaml_write(self, obj)->str:
        str_val = str(obj)
        converted = str_val.replace('{{', var.DOUBLE_LEFT_BRACKETS)
        converted = converted.replace('}}', var.DOUBLE_RIGHT_BRACKETS)
        converted = converted.replace('#',var.HASH_TAG)
        converted = converted.replace("'",var.SINGLE_QUOTE)
        return converted

    def convert_special_characters_back_in_file(self, file_text:str)->str:
        converted = file_text.replace(var.DOUBLE_LEFT_BRACKETS,'{{')
        converted = converted.replace(var.DOUBLE_RIGHT_BRACKETS,'}}')
        converted = converted.replace(var.EMPTY_STRING,'')
        converted = converted.replace(": ''",': ')
        converted = converted.replace(var.HASH_TAG,'#')
        converted = converted.replace(var.SINGLE_QUOTE,"'")
        converted = converted.replace("'[]'",'')
        converted = converted.replace("[]",'')
        converted = converted.replace(var.VALUE_QUALIFIER,'')
        return converted
    
    def choose_value_string(self, file_data, field_name, db_data, db_field_name, default_value)-> str:
        use_file_data = False

        if db_field_name not in db_data:
            db_value_exists = False
        #elif db_data[db_field_name] is None or db_value == []: # commenting this out as a blank value from the db can mean it was removed in the db
        #    db_value_exists = False
        else:
            db_value_exists = True
            
        if field_name in file_data and file_data[field_name] is not None:
            field_value = str(file_data[field_name])

            #if "{ordereddict([('" in field_value:
            if "<~<~" in field_value:
                #return_value_raw = field_value.replace("{ordereddict([('", "").replace("', None)]): None}", "")
                #return_value = self.create_jinja_var(return_value_raw)
                #return_value = field_value.replace('<~<~','{{').replace('~>~>','}}')
                return_value = field_value
                use_file_data = True
            if not use_file_data and not db_value_exists: # if there's no jinja value, but there's also no db value, then also use the file value
                return_value = field_value
                use_file_data = True

        if not use_file_data and db_value_exists:
            if db_data[db_field_name] is None or db_data[db_field_name] == '':
                return_value = default_value
            else:
                return_value = db_data[db_field_name]
        elif not use_file_data:
            return_value = default_value
        #return_value_converted = return_value.replace('{{', var.DOUBLE_LEFT_BRACKETS).replace('}}', var.DOUBLE_RIGHT_BRACKETS).replace('#',var.HASH_TAG)
        return_value_converted = var.VALUE_QUALIFIER + self.convert_for_yaml_write(return_value) + var.VALUE_QUALIFIER
        return return_value_converted

    
            
    def choose_value_list(self, file_data, field_name, db_data, db_field_name, default_value)->list:
        use_file_data = False
        
        #print('###### file_data ########')   
        #print(file_data)
        #print('###### field_name ########')
        #print(field_name)
        #print('###### db_data ########')
        #print(db_data)
        #print('###### db_field_name ########')
        #print(db_field_name)
        #d['ALLOWED_VALUES'] if (tag['ALLOWED_VALUES'] is not None and tag['ALLOWED_VALUES'] != []) else var.EMPTY_STRING

        # Check if db value returned
        if db_field_name not in db_data:
            db_value_exists = False
        #elif db_data[db_field_name] is None or db_value == []: # commenting this out as a blank value from the db can mean it was removed in the db
        #    db_value_exists = False
        else:
            db_value_exists = True
            #print('^^^^^^^^^^^^^^^^^^^^^^^^^^')
            #print(type(db_data[db_field_name]))
            if( type(db_data[db_field_name]) == list ):
                db_value_list = db_data[db_field_name]
            else:
                if db_data[db_field_name] is None or db_data[db_field_name] == '' or db_data[db_field_name] == [] or db_data[db_field_name] == var.EMPTY_STRING:
                    db_value_list = []
                else:
                    db_value_list = json.loads(db_data[db_field_name].replace("'",'"'))

        #print('### TESTING ###')
        #print(db_data)
        #print(db_data[db_field_name])
        #print(db_value_list)
        #print('##e done e##')
        # Check if file value exists and whether the list contains jinja
        file_contains_jinja = False
        if field_name in file_data and file_data[field_name] is not None:
            file_value_exists = True
            if( type(file_data[field_name]) == list ):
                field_value_list = file_data[field_name]
            else:
                if file_data[field_name] is None or file_data[field_name] == '' or file_data[field_name] == [] or file_data[field_name] == var.EMPTY_STRING:
                    field_value_list = []
                else:
                    field_value_list = json.loads(file_data[field_name].replace("'",'"'))



            for field_value in field_value_list:
                if "<~<~" in field_value or '{{' in field_value: 
                    file_contains_jinja = True
        else:
            file_value_exists = False
        
        # Choose value from file or db depending on which exists and if there's jinja involved
        if file_value_exists and file_contains_jinja:
            # Jinja in file trumps first
            return_value_list = field_value_list
        elif db_value_exists and (db_value_list is None or db_value_list == []):
            return_value_list = default_value
        elif db_value_exists:
            return_value_list = db_value_list
        elif file_value_exists:
            return_value_list = field_value_list
        else:
            return_value_list = default_value
        #print('^^^^^^^^^^^^ return value list^^^^^^^^^^^^^')
        #print(return_value_list)
        #print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        converted_list = []
        for rtn_val in return_value_list:
            converted_list.append(self.convert_for_yaml_write(rtn_val))
        
        #print('^^^^^^^^^^^^ converted_list^^^^^^^^^^^^^')
        #print(converted_list)
        #print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        return converted_list
#####
        # if field_name in file_data and file_data[field_name] is not None:
        #     field_value_list = list(file_data[field_name])
                
        #     for field_value in field_value_list:
        #         #if "{ordereddict([('" in field_value:
        #         if "<~<~" in field_value:
        #             #return_value_raw = field_value.replace(var.DOUBLE_LEFT_BRACKETS, "").replace(var.DOUBLE_RIGHT_BRACKETS, "").replace()
        #             #return_value = self.create_jinja_var(return_value_raw)
        #             return_value = field_value
        #             use_file_data = True
        #     if not use_file_data and not db_value_exists: # if there's no jinja value, but there's also no db value, then also use the file value
        #         return_value = field_value
        #         use_file_data = True

        # if not use_file_data and db_value_exists:
        #     if db_data[db_field_name] is None or db_data[db_field_name] == []:
        #         return_value = default_value
        #     else:
        #         return_value = db_data[db_field_name]
        # else:
        #     return_value = default_value

        # return_value_converted = self.convert_for_yaml_write(str(return_value))
        # return return_value_converted
    
    def create_jinja_ref_string(self, yaml_string:str):
        output = yaml_string.replace("{{", "'!!{{!!")
        output = output.replace("<~<~","'!!{{!!")
        output = output.replace("}}", "!!}}!!'")
        output = output.replace("~>~>", "!!}}!!'")
        output = output.replace("'","!!|!!")
        return output
    
    def choose_value_list_of_objects(self, file_data, field_name, db_data, db_field_name, default_value)->list:
        use_file_data = False

        # Check if db value exists
        db_dict = {}
        db_value_exists = False
        if db_field_name in db_data:
            db_value_exists = True
            if( type(db_data[db_field_name]) == list ):
                db_value_list = db_data[db_field_name]
            else:
                if db_data[db_field_name] is None or db_data[db_field_name] == '' or db_data[db_field_name] == [] or db_data[db_field_name] == var.EMPTY_STRING:
                    db_value_list = []
                else:
                    db_value_list = json.loads(db_data[db_field_name].replace("'",'"'))
            for db_obj in db_value_list:
                for k in db_obj.keys():
                    db_dict[k] = db_obj[k]

        # Check if file value exists 
        file_dict = {}
        file_value_exists = False
        if field_name in file_data and file_data[field_name] is not None:
            file_value_exists = True
            if( type(file_data[field_name]) == list ):
                field_value_list = file_data[field_name]
            else:
                if file_data[field_name] is None or file_data[field_name] == '' or file_data[field_name] == [] or file_data[field_name] == var.EMPTY_STRING:
                    field_value_list = []
                else:
                    field_value_list = json.loads(file_data[field_name].replace("'",'"'))

            # Convert file list of dicts into single dict
            #print('#####################################')
            #print(field_value_list)
            for file_obj in field_value_list:
                #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                #print(file_obj)
                for k in file_obj.keys():
                    file_dict[k] = file_obj[k]

        if db_value_exists and (db_value_list is None or db_value_list == []):
            return_value_list = default_value
        elif db_value_exists:
            
            return_value_list = []
            db_keys = db_dict.keys()
            for db_key in db_keys:
                new_item = {}
                db_key_converted = self.convert_for_yaml_write(db_key)
                if db_key in file_dict.keys():
                    if '<~<~' in file_dict[db_key]: # file value exists and contains jinja --> use file version
                        new_item[db_key_converted] = self.convert_for_yaml_write(file_dict[db_key])
                    else: # file valuel exists but does NOT contain jinja --> use db value to override
                        new_item[db_key_converted] = self.convert_for_yaml_write(db_dict[db_key])
                else: # value only exists in db (file is blank) --> take db value
                    new_item[db_key_converted] = self.convert_for_yaml_write(db_dict[db_key])
                new_item[db_key_converted] = var.VALUE_QUALIFIER + new_item[db_key_converted] + var.VALUE_QUALIFIER
            
                return_value_list.append(new_item)

        elif file_value_exists:
            return_value_list = field_value_list
        else:
            return_value_list = default_value



        
        return return_value_list
    


        #for field_value in field_value_list:
        #    if "<~<~" in field_value or '{{' in field_value: 
        #        file_contains_jinja = True
        
        
        
#[{"<~<~ref('CONTROL__GOVERNANCE__ENV')~>~>": '<~<~env~>~>'}]
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#[{'!!{{!!ref(!!|!!CONTROL__GOVERNANCE__ENV!!|!!)!!}}!!': 'DEV'}]
    def choose_list_objects(self, db_list, file_list)->list:
        new_list = []
        # convert list of dicts to a single dict (to search dict later)
        db_dict = {}
        for db_obj in db_list:
            for k in db_obj.keys():
                db_dict[k] = db_obj[k]
            
        file_dict = {}
        for file_obj in file_list:
            for k in file_obj.keys():
                file_dict[k] = file_obj[k]

        db_keys = db_dict.keys()
        for db_key in db_keys:
            new_item = {}
            db_key_converted = self.convert_for_yaml_write(db_key)
            if db_key in file_dict.keys():
                if '<~<~' in file_dict[db_key]: # file value exists and contains jinja --> use file version
                    new_item[db_key_converted] = self.convert_for_yaml_write(file_dict[db_key])
                else: # file valuel exists but does NOT contain jinja --> use db value to override
                    new_item[db_key_converted] = self.convert_for_yaml_write(db_dict[db_key])
            else: # value only exists in db (file is blank) --> take db value
                new_item[db_key_converted] = self.convert_for_yaml_write(db_dict[db_key])
            new_item[db_key_converted] = var.VALUE_QUALIFIER + new_item[db_key_converted] + var.VALUE_QUALIFIER
        
            new_list.append(new_item)
        return new_list
    

            
    def choose_value_list_delete(self, file_data, field_name, db_data, db_field_name, default_value)->list:
        use_file_data = False
        
        print('###### file_data ########')   
        print(file_data)
        print('###### field_name ########')
        print(field_name)
        print('###### db_data ########')
        print(db_data)
        print('###### db_field_name ########')
        print(db_field_name)
        #d['ALLOWED_VALUES'] if (tag['ALLOWED_VALUES'] is not None and tag['ALLOWED_VALUES'] != []) else var.EMPTY_STRING

        if db_field_name not in db_data:
            db_value_exists = False
        #elif db_data[db_field_name] is None or db_value == []: # commenting this out as a blank value from the db can mean it was removed in the db
        #    db_value_exists = False
        else:
            db_value_exists = True
            
        if field_name in file_data and file_data[field_name] is not None:
            field_value_list = list(file_data[field_name])
                
            for field_value in field_value_list:
                #if "{ordereddict([('" in field_value:
                if "<~<~" in field_value:
                    #return_value_raw = field_value.replace(var.DOUBLE_LEFT_BRACKETS, "").replace(var.DOUBLE_RIGHT_BRACKETS, "").replace()
                    #return_value = self.create_jinja_var(return_value_raw)
                    return_value = field_value
                    use_file_data = True
            if not use_file_data and not db_value_exists: # if there's no jinja value, but there's also no db value, then also use the file value
                return_value = field_value
                use_file_data = True

        if not use_file_data and db_value_exists:
            if db_data[db_field_name] is None or db_data[db_field_name] == []:
                return_value = default_value
            else:
                return_value = db_data[db_field_name]
        else:
            return_value = default_value

        return_value_converted = self.convert_for_yaml_write(str(return_value))
        return return_value_converted