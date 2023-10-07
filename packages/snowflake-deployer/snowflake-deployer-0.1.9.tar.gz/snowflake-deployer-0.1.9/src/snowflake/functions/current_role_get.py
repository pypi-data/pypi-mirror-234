def current_role_get(self)->str:
    cur = self._conn.cursor()
    query = '''
        SELECT CURRENT_ROLE() as CURRENT_ROLE;
    '''
    try:
        res = cur.execute(query).fetchall()
        current_role = res[0][0]
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return current_role
