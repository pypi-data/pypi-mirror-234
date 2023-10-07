from snowflake.connector import DictCursor

def grants_get(self,object_name:str, object_type:str)->dict:
    cur = self._conn.cursor(DictCursor)
    query = 'SHOW GRANTS ON ' + object_type + ' ' + object_name + ';'

    data=[]
    try:
        cur.execute(query)
        for rec in cur:
            #if rec['privilege'] !== 'OWNERSHIP':
            grant = {}
            #grantee_name, privilege ('OWNERSHIP'), granted_to == 'ROLE', 

            grant['GRANTEE_NAME'] = rec['grantee_name']
            grant['PRIVILEGE'] = rec['privilege']
            grant['GRANT_TYPE'] = rec['granted_to']
            grant['GRANT_OPTION'] = rec['grant_option']
            data.append(grant)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data