from src.util.util import remove_prefix
def wrangle_task(self, database_name:str, schema_name:str, env_database_prefix:str, env_role_prefix:str, deploy_db_name:str, ignore_roles_list:str, deploy_tag_list:list[str], current_role:str, available_roles:list[str], handle_ownership)->dict:
    if env_database_prefix is None:
        env_database_prefix = ''
    if env_role_prefix is None:
        env_role_prefix = ''

    tasks = self._sf.tasks_get(database_name, schema_name)  
    
    data = []
    for d in tasks:

        # Currently there's no way to get USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE from the db. So assume a value if no warehouse exists which would indicate a serverless task
        if (d['WAREHOUSE'] is None or d['WAREHOUSE'] == ''):
            d['USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE'] = 'XSMALL'

        full_task_name = database_name + '.' + schema_name + '.' + d['TASK_NAME']
        d['OWNER'] = self._handle_ownership(handle_ownership, d['OWNER'], 'task', full_task_name, current_role, available_roles)

        if d['OWNER'] not in ignore_roles_list: # if role managed by deployer (not out of the box) then add the jinja reference
            d['OWNER'] = self.create_jinja_role_instance(d['OWNER'])
        
        tags = []
        tags_raw = self._sf.tag_references_get(database_name, full_task_name, 'task') #task tag references live within Snowflake db
        for t in tags_raw:
            if not (t['TAG_DATABASE'] == deploy_db_name and t['TAG_SCHEMA'] == 'TAG' and t['TAG_NAME'] in deploy_tag_list):
                tv = {}
                db_name = remove_prefix(t['TAG_DATABASE'],env_database_prefix)
                #tv['name'] = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                #tv['value'] = t['TAG_VALUE']
                tag_name = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                tv[tag_name] = t['TAG_VALUE']
                tags.append(tv)
        d['TAGS'] = tags
        
        grants_raw = self._sf.grants_get(full_task_name, 'task')
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
        d['GRANTS'] = grants_combined
        
        data.append(d)
    
    return data   
