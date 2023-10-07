from src.util.util import remove_prefix
def wrangle_warehouse(self, env_warehouse_prefix:str, env_database_prefix:str, env_role_prefix:str, deploy_db_name:str, ignore_roles_list:str, deploy_tag_list:list[str], current_role:str, available_roles:list[str], handle_ownership)->dict:
    if env_database_prefix is None:
        env_database_prefix = ''
    if env_warehouse_prefix is None:
        env_warehouse_prefix = ''
    if env_role_prefix is None:
        env_role_prefix = ''

    whs = self._sf.warehouses_get(env_warehouse_prefix)  
    
    data = []
    for wh in whs:
        wh['WAREHOUSE_NAME_SANS_ENV'] = remove_prefix(wh['WAREHOUSE_NAME'],env_warehouse_prefix)
        wh['WAREHOUSE_SIZE'] = wh['WAREHOUSE_SIZE'].replace('-','').upper()
        wh['OWNER'] = self._handle_ownership(handle_ownership, wh['OWNER'], 'warehouse', wh['WAREHOUSE_NAME'], current_role, available_roles)

        if wh['OWNER'] not in ignore_roles_list: # if role managed by deployer (not out of the box) then add the jinja reference
            wh['OWNER'] = self.create_jinja_role_instance(wh['OWNER'])
        
        tags = []
        tags_raw = self._sf.tag_references_get('SNOWFLAKE', wh['WAREHOUSE_NAME'], 'warehouse') #warehouse tag references live within Snowflake db
        for t in tags_raw:
            if not (t['TAG_DATABASE'] == deploy_db_name and t['TAG_SCHEMA'] == 'TAG' and t['TAG_NAME'] in deploy_tag_list):
                tv = {}
                db_name = remove_prefix(t['TAG_DATABASE'],env_database_prefix)
                #tv['name'] = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                #tv['value'] = t['TAG_VALUE']
                tag_name = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                tv[tag_name] = t['TAG_VALUE']
                tags.append(tv)
        wh['TAGS'] = tags
        
        grants_raw = self._sf.grants_get(wh['WAREHOUSE_NAME'], 'warehouse')
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
        #combine grants with delimiter
        grants_combined = self._combine_grants(grants)
        #grants_combined = []
        #for grant_dict in grants:
        #    key = list(grant_dict.keys())[0]
        #    found = False
        #    #for grants_new in grants_combined:
        #    for i in range(len(grants_combined)):
        #        if key in grants_combined[i].keys():
        #            new_val = grants_combined[i][key] + ', ' + grant_dict[key]
        #            grants_combined[i] = {key:new_val}
        #            found = True
        #    if not found:
        #        grants_combined.append({key: grant_dict[key]})
        #print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        #print(grants)
        #print('--')
        #print(grants_combined)
        #print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        wh['GRANTS'] = grants_combined

        data.append(wh)
    
    return data   
