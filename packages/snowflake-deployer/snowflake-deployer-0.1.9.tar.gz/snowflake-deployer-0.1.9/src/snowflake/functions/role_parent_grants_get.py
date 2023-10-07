from snowflake.connector import DictCursor
import json

def role_parent_grants_get(self,full_role_name:str)->dict:
    cur = self._conn.cursor(DictCursor)

    data = []
    try:
        query = "SHOW GRANTS ON ROLE " + full_role_name + ";"
        cur.execute(query)
        query = '''
            SELECT "grantee_name" as PARENT_ROLE, "grant_option" as GRANT_OPTION FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) WHERE "privilege" = 'USAGE' and "granted_to" = 'ROLE';
        '''
        cur.execute(query)
        #PARENT_GRANTS = []
        for rec in cur:
            data.append(rec['PARENT_ROLE'])
           
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data

    