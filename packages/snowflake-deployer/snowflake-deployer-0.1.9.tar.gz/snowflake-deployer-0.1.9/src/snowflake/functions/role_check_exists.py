from snowflake.connector import DictCursor
def role_check_exists(self,role_name: str)->bool:
    cur = self._conn.cursor(DictCursor)

    query = '''
        SHOW ROLES LIKE %s;
    '''
    try:
        cur.execute(query, (role_name))
        rowcount = 0
        owner = None
        for rec in cur:
            if rowcount == 0:
                rowcount+=1
                owner = rec["owner"]
        exists = True if rowcount > 0 else False 
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return exists, owner