from src.util.util import remove_prefix
def wrangle_database(self, env_database_prefix:str, env_role_prefix:str, excluded_databases:list[str], deploy_db_name:str, ignore_roles_list:str, deploy_tag_list:list[str], current_role:str, available_roles:list[str], handle_ownership, import_databases:list[str])->dict:
    if env_database_prefix is None:
        env_database_prefix = ''
    if env_role_prefix is None:
        env_role_prefix = ''
        
    dbs = self._sf.databases_get(env_database_prefix)  
    
    data = []
    for db in dbs:
        if db['DATABASE_NAME'] not in excluded_databases and db['DATABASE_NAME'] != deploy_db_name:
            if import_databases == [] or db['DATABASE_NAME'] in import_databases:
                db['DATABASE_NAME_SANS_ENV'] = remove_prefix(db['DATABASE_NAME'],env_database_prefix)   
                
                db['OWNER'] = self._handle_ownership(handle_ownership, db['OWNER'], 'database', db['DATABASE_NAME'], current_role, available_roles)

                if db['OWNER'] not in ignore_roles_list: # if role managed by deployer (not out of the box) then add the jinja reference
                    db['OWNER'] = self.create_jinja_role_instance(db['OWNER'])
                
                tags = []
                tags_raw = self._sf.tag_references_get(db['DATABASE_NAME'], db['DATABASE_NAME'], 'database')
                for t in tags_raw:
                    if not (t['TAG_DATABASE'] == deploy_db_name and t['TAG_SCHEMA'] == 'TAG' and t['TAG_NAME'] in deploy_tag_list):
                        tv = {}
                        db_name = remove_prefix(t['TAG_DATABASE'],env_database_prefix)
                        #tv['name'] = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                        #tv['value'] = t['TAG_VALUE']
                        tag_name = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                        tv[tag_name] = t['TAG_VALUE']
                        tags.append(tv)
                db['TAGS'] = tags
                
                grants_raw = self._sf.grants_get(db['DATABASE_NAME'], 'database')
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
                db['GRANTS'] = grants_combined

                data.append(db)      

    return data   
