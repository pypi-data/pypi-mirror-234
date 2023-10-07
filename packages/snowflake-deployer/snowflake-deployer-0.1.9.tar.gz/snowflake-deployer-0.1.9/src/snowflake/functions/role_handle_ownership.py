from snowflake.connector import ProgrammingError

# this whole thing should be deleted ... once ported over to new functions
def role_handle_ownership(self, object_owner:str, object_type:str, object_name:str, current_role:str, available_roles:list)->str:
    cur = self._conn.cursor()
    try:
        rtn = object_owner
        if object_owner not in available_roles:
            role_available = self.role_check_assigned(object_owner)
            if not role_available:
                owner_query = 'GRANT ROLE "' + object_owner + '" TO ROLE ' + current_role + ';'
                try:
                    cur.execute(owner_query) 
                    available_roles.append(object_owner)
                except ProgrammingError as db_ex:
                    if db_ex.errno == 3010:
                        self.ownership_transfer(object_type,object_name,current_role)
                        rtn = current_role
                    else:
                        raise
    
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return rtn



                
                