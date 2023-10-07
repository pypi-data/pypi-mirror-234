from snowflake.connector import DictCursor
def schema_check_exists(self,schema_full_name: str)->bool:
    cur = self._conn.cursor(DictCursor)
    schema_name = schema_full_name.split('.')[1]
    database_name = schema_full_name.split('.')[0]
    query = '''
        SHOW SCHEMAS LIKE %s in database identifier(%s);
    '''
    try:
        cur.execute(query, (schema_name,database_name))
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
