from src.util.util import remove_prefix
def wrangle_schema(self, database_name:str, env_database_prefix:str, env_role_prefix:str, deploy_db_name:str, ignore_roles_list:str, deploy_tag_list:list[str], current_role:str, available_roles:list[str], handle_ownership)->dict:
    if env_database_prefix is None:
        env_database_prefix = ''
    if env_role_prefix is None:
        env_role_prefix = ''


    schemas = self._sf.schemas_get(database_name)  
    
    data = []
    for s in schemas:
        full_schema_name = database_name + '.' + s['SCHEMA_NAME']
        if s['SCHEMA_NAME'] not in ['INFORMATION_SCHEMA']:    
            s['OWNER'] = self._handle_ownership(handle_ownership, s['OWNER'], 'schema', full_schema_name, current_role, available_roles)

            if s['OWNER'] not in ignore_roles_list: # if role managed by deployer (not out of the box) then add the jinja reference
                s['OWNER'] = self.create_jinja_role_instance(s['OWNER'])
            
            schema_with_db = database_name + '.' + s['SCHEMA_NAME']
            tags = []
            tags_raw = self._sf.tag_references_get(database_name, schema_with_db, 'schema') #warehouse tag references live within Snowflake db
            for t in tags_raw:
                if not (t['TAG_DATABASE'] == deploy_db_name and t['TAG_SCHEMA'] == 'TAG' and t['TAG_NAME'] in deploy_tag_list):
                    tv = {}
                    db_name = remove_prefix(t['TAG_DATABASE'],env_database_prefix)
                    #tv['name'] = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                    #tv['value'] = t['TAG_VALUE']
                    tag_name = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                    tv[tag_name] = t['TAG_VALUE']
                    tags.append(tv)
            s['TAGS'] = tags
            
            grants_raw = self._sf.grants_get(schema_with_db, 'schema')
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
            s['GRANTS'] = grants_combined

            data.append(s)
    
    return data   
