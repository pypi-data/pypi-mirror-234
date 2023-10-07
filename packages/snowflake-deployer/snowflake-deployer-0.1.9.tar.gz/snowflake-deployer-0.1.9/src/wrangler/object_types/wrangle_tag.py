from src.util.util import remove_prefix
def wrangle_tag(self, database_name:str, schema_name:str, env_database_prefix:str, deploy_db_name:str, ignore_roles_list:str, deploy_tag_list:list[str], current_role:str, available_roles:list[str], handle_ownership)->dict:
    if env_database_prefix is None:
        env_database_prefix = ''

    tags_all = self._sf.tags_get(database_name, schema_name)  
    #print('^^^^^^^^^^ SF TAGS GET ^^^^^^^^^^^^^^^^^')
    #print(tags_all)
    #print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    data = []
    for t in tags_all:
        full_tag_name = database_name + '.' + schema_name + '.' + t['TAG_NAME']
        
        t['OWNER'] = self._handle_ownership(handle_ownership, t['OWNER'], 'tag', full_tag_name, current_role, available_roles)

        if t['OWNER'] not in ignore_roles_list: # if role managed by deployer (not out of the box) then add the jinja reference
            t['OWNER'] = self.create_jinja_role_instance(t['OWNER'])
        
        masking_policy_references_raw = self._sf.tag_masking_policy_reference(full_tag_name)
        
        masking_policy_references = []
        #print(masking_policy_references_raw)
        for masking_policy_reference in masking_policy_references_raw:
            #print('#####################################')
            #print(masking_policy_reference)
            #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            masking_policy_arr = masking_policy_reference.split('.')
            masking_policy_db_name = remove_prefix(masking_policy_arr[0], env_database_prefix)
            masking_policy_jinja = self.create_jinja_ref(masking_policy_db_name,masking_policy_arr[1],masking_policy_arr[2])
            masking_policy_references.append(masking_policy_jinja)
        t['MASKING_POLICIES'] = masking_policy_references
        data.append(t)
    
    return data   
