def deploy_db_check_installed(self,deploy_db_name: str)->bool:
    cur = self._conn.cursor()

    query = '''
        SHOW DATABASES LIKE %s;
    '''
    try:
        res = cur.execute(query, (deploy_db_name))
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return (res.rowcount>0)