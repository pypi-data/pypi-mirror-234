from snowflake.connector import ProgrammingError

def role_grant_to_role(self,role_to_grant:str, grant_to_role:str)->bool:
    cur = self._conn.cursor()
    query = 'GRANT ROLE "' + role_to_grant + '" TO ROLE ' + grant_to_role + ';'
    try:
        cur.execute(query) 
        rtn = True
    except ProgrammingError as db_ex:
        if db_ex.errno == 3010:
            rtn = False
        else:
            raise  
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return rtn
