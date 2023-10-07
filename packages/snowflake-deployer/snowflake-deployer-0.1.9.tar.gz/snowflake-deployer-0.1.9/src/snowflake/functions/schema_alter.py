def schema_alter(self,schema_name:str, data_retention_time_in_days:int, comment:str, owner:str, tags:list, grants:list):
    cur = self._conn.cursor()
    query = ''
    try:
        query = 'ALTER SCHEMA identifier(%s) SET '
        params = [schema_name]
        if data_retention_time_in_days is not None:
            query += ' DATA_RETENTION_TIME_IN_DAYS = %s'
            params.append(data_retention_time_in_days)
        if comment is not None:
            query += ' COMMENT = %s'
            params.append(comment)
        if len(params) > 1: # something to execute
            cur.execute(query, params)

        if tags is not None and tags != []:
            for t in tags:
                tag_key = list(t)[0]
                tag_val = t[tag_key]
                query = 'ALTER SCHEMA identifier(%s) SET TAG identifier(%s) = %s;'
                params = (schema_name,tag_key,tag_val)
                cur.execute(query,params)

        if owner is not None:
            query = '''
                GRANT OWNERSHIP ON SCHEMA identifier(%s) TO ROLE identifier(%s) COPY CURRENT GRANTS;
            '''
            cur.execute(query,(schema_name, owner))

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
#ALTER SCHEMA [ IF EXISTS ] <name> RENAME TO <new_schema_name>
#
#ALTER SCHEMA [ IF EXISTS ] <name> SWAP WITH <target_schema_name>
#
#ALTER SCHEMA [ IF EXISTS ] <name> SET {
#                                      [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
#                                      [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
#                                      [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
#                                      [ COMMENT = '<string_literal>' ]
#                                      }
#
#ALTER SCHEMA [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
#
#ALTER SCHEMA [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
#
#ALTER SCHEMA [ IF EXISTS ] <name> UNSET {
#                                        DATA_RETENTION_TIME_IN_DAYS         |
#                                        MAX_DATA_EXTENSION_TIME_IN_DAYS     |
#                                        DEFAULT_DDL_COLLATION               |
#                                        COMMENT
#                                        }
#                                        [ , ... ]
#
#ALTER SCHEMA [ IF EXISTS ] <name> { ENABLE | DISABLE } MANAGED ACCESS