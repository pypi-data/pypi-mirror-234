from snowflake.connector import DictCursor

def roles_get(self,env_role_prefix:str)->dict:
    cur = self._conn.cursor(DictCursor)
    query = "SHOW ROLES like '" + env_role_prefix + "%';"
    data=[]
    try:
        cur.execute(query)
        for rec in cur:
            nw = {}
            nw['ROLE_NAME'] = rec['name']
            nw['OWNER'] = rec['owner']
            nw['COMMENT'] = rec['comment']
            data.append(nw)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data