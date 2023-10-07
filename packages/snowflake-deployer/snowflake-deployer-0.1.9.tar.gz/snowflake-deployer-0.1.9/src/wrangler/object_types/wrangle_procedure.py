from src.util.util import remove_prefix
def wrangle_procedure(self, database_name:str, schema_name:str, env_procedure_prefix:str, env_database_prefix:str, env_role_prefix:str, deploy_db_name:str, ignore_roles_list:str, deploy_tag_list:list[str], current_role:str, available_roles:list[str], handle_ownership)->dict:
    if env_database_prefix is None:
        env_database_prefix = ''
    if env_procedure_prefix is None:
        env_procedure_prefix = ''
    if env_role_prefix is None:
        env_role_prefix = ''

    procs = self._sf.procedures_get(database_name, schema_name)  
    
    data = []
    for p in procs:

        proc_full_name = database_name + '.' + schema_name + '.' + p['ARGUMENT_SIGNATURE_TO_MATCH']

        p['PROCEDURE_NAME_SANS_ENV'] = remove_prefix(p['PROCEDURE_NAME'],env_procedure_prefix)
        
        p['OWNER'] = self._handle_ownership(handle_ownership, p['OWNER'], 'procedure', proc_full_name, current_role, available_roles)

        if p['OWNER'] not in ignore_roles_list: # if role managed by deployer (not out of the box) then add the jinja reference
            p['OWNER'] = self.create_jinja_role_instance(p['OWNER'])
        
        tags = []
        
        tags_raw = self._sf.tag_references_get(database_name, proc_full_name, 'procedure') #warehouse tag references live within Snowflake db
        for t in tags_raw:
            if not (t['TAG_DATABASE'] == deploy_db_name and t['TAG_SCHEMA'] == 'TAG' and t['TAG_NAME'] in deploy_tag_list):
                tv = {}
                db_name = remove_prefix(t['TAG_DATABASE'],env_database_prefix)
                #tv['name'] = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                #tv['value'] = t['TAG_VALUE']
                tag_name = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                tv[tag_name] = t['TAG_VALUE']
                tags.append(tv)
        p['TAGS'] = tags

        grants_raw = self._sf.grants_get(proc_full_name, 'procedure')
        grants = []
        for g in grants_raw:
            if g['PRIVILEGE'] != 'OWNERSHIP' and g['GRANTEE_NAME'] != current_role and g['GRANT_TYPE'] == 'ROLE':
                grant = {}
                role_name = remove_prefix(g['GRANTEE_NAME'],env_role_prefix)
                grant_to = self.create_jinja_role_instance(role_name) if role_name not in ignore_roles_list else role_name
                grant[grant_to] = g['PRIVILEGE']
                if g['GRANT_OPTION'] is True:
                    grant['GRANT_OPTION'] = True
                grants.append(grant)
        grants_combined = self._combine_grants(grants)
        p['GRANTS'] = grants_combined
        
        p.pop('ARGUMENT_SIGNATURE_TO_MATCH')
        data.append(p)
    
    return data   
