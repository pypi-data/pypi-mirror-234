def schema_create(self,schema_name:str, data_retention_time_in_days:int, comment:str, owner:str, tags:list, grants:list, deploy_role:str):
    cur = self._conn.cursor()
    query = ''
    try:
        query = 'CREATE SCHEMA identifier(%s)'
        params = [schema_name]
        if data_retention_time_in_days is not None:
            query += ' DATA_RETENTION_TIME_IN_DAYS = %s'
            params.append(data_retention_time_in_days)
        
        if comment is not None:
            query += ' COMMENT = %s'
            params.append(comment)

        if tags is not None and tags != []:
            query += ' TAG(' 
            for t in tags:
                tag_key = list(t)[0]
                tag_val = t[tag_key]
                tag_name = '"' + '"."'.join(tag_key.split('.')) + '"'
                query += ' ' + tag_name + ' = %s,'
                params.append(tag_val)
            query = query[:-1] # remove last column from tag list append
            query += ') '      
        #print('params:' + schema_name + ', ' + str(data_retention_time_in_days) + ', ' + comment)
        #print(query)
        cur.execute(query, params)

        if owner is not None and owner != deploy_role: #if owner is deploy role, no need to run this
            query = 'GRANT OWNERSHIP ON SCHEMA identifier(%s) TO ROLE "' + owner + '" COPY CURRENT GRANTS;'
            cur.execute(query,(schema_name))

        if grants is not None:
            for grant in grants:
                grant_keys = grant.keys()
                grant_option = grant['GRANT_OPTION'] if 'GRANT_OPTION' in grant_keys else False
                role = ''
                permission = ''
                for key in grant_keys:
                    if key != 'GRANT_OPTION':
                        role = key
                        permission = grant[key]
                if role != '' and permission != '':
                    query = "GRANT " + permission + " ON SCHEMA identifier(%s) TO ROLE " + role + ";"
                    cur.execute(query,(schema_name))
                else:
                    raise Exception('Invalid grants for warehouse: ' + schema_name)
            
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()

# CREATE [ OR REPLACE ] [ TRANSIENT ] SCHEMA [ IF NOT EXISTS ] <name>
#   [ CLONE <source_schema>
#         [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ] ]
#   [ WITH MANAGED ACCESS ]
#   [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
#   [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
#   [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
#   [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
#   [ COMMENT = '<string_literal>' ]