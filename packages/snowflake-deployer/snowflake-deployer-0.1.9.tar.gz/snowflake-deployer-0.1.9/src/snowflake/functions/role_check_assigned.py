def role_check_assigned(self,role_name:str)->bool:
    cur = self._conn.cursor()
    query = '''
        SELECT is_role_in_session(%s) as ROLE_AVAILABLE;
    '''
    try:
        res = cur.execute(query,(role_name)).fetchall()
        role_available = res[0][0]
        #role_available = True if role_available_str.upper() == 'TRUE' else False
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return role_available
