from snowflake.connector import DictCursor
def task_check_exists(self,task_full_name:str)->bool:
    # function_name: 
    cur = self._conn.cursor(DictCursor)
    schema_full_name = task_full_name.split('.')[0] + '.' + task_full_name.split('.')[1]
    task_name = task_full_name.split('.')[2]

    query = '''
        SHOW TASKS LIKE %s IN SCHEMA identifier(%s);
    '''
    try:
        cur.execute(query, (task_name, schema_full_name))
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

