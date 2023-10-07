from snowflake.connector import DictCursor
def masking_policy_check_exists(self,policy_full_name: str)->bool:
    cur = self._conn.cursor(DictCursor)
    schema_name = policy_full_name.split('.')[1]
    database_name = policy_full_name.split('.')[0]
    schema_with_db_name = database_name + '.' + schema_name
    policy_name = policy_full_name.split('.')[2]
    query = '''
        SHOW MASKING POLICIES LIKE %s in schema identifier(%s);
    '''
    try:
        cur.execute(query, (policy_name,schema_with_db_name))
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
