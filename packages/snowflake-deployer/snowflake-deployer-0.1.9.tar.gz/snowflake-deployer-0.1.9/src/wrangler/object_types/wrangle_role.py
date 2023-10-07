from src.util.util import remove_prefix
def wrangle_role(self, env_role_prefix:str, env_database_prefix:str, deploy_db_name:str, ignore_roles_list:str, deploy_tag_list:list[str], current_role:str, available_roles:list[str], handle_ownership)->dict:
    if env_database_prefix is None:
        env_database_prefix = ''
    if env_role_prefix is None:
        env_role_prefix = ''

    roles = self._sf.roles_get(env_role_prefix)  
    
    data = []
    for r in roles:
        if r['ROLE_NAME'] not in ignore_roles_list:
            r['ROLE_NAME_SANS_ENV'] = remove_prefix(r['ROLE_NAME'],env_role_prefix)
            
            r['OWNER'] = self._handle_ownership(handle_ownership, r['OWNER'], 'role', r['ROLE_NAME'], current_role, available_roles)

            if r['OWNER'] not in ignore_roles_list: # if role managed by deployer (not out of the box) then add the jinja reference
                r['OWNER'] = self.create_jinja_role_instance(r['OWNER'])
            
            parent_grants = []
            parent_grants_raw = self._sf.role_parent_grants_get(r['ROLE_NAME'])
            for parent_grant_raw in parent_grants_raw:
                parent_grant_sans_prefix = remove_prefix(parent_grant_raw, env_role_prefix)
                if parent_grant_sans_prefix not in ignore_roles_list:
                    parent_grant = self.create_jinja_role_instance(parent_grant_sans_prefix)
                else:
                    parent_grant = parent_grant_sans_prefix
                parent_grants.append(parent_grant)

            r['PARENT_GRANTS'] = parent_grants
            tags = []
            tags_raw = self._sf.tag_references_get('SNOWFLAKE', r['ROLE_NAME'], 'role') #warehouse tag references live within Snowflake db
            for t in tags_raw:
                if not (t['TAG_DATABASE'] == deploy_db_name and t['TAG_SCHEMA'] == 'TAG' and t['TAG_NAME'] in deploy_tag_list):
                    tv = {}
                    db_name = remove_prefix(t['TAG_DATABASE'],env_database_prefix)
                    #tv['name'] = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                    #tv['value'] = t['TAG_VALUE']
                    tag_name = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                    tv[tag_name] = t['TAG_VALUE']
                    tags.append(tv)
            r['TAGS'] = tags
            
            data.append(r)
        
    return data   
