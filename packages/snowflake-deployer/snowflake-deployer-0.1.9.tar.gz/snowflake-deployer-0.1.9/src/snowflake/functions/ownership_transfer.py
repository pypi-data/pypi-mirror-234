def ownership_transfer(self,transfer_object_type:str, transfer_object_name:str, new_role:str):
    cur = self._conn.cursor()
    query = "GRANT OWNERSHIP ON " + transfer_object_type + " identifier(%s) TO ROLE " + new_role + " COPY CURRENT GRANTS;"
    try:
        cur.execute(query,(transfer_object_name))
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
