from snowflake.connector import DictCursor
def function_check_exists(self,function_name: str, function_signature:str)->bool:
    # function_name: 
    cur = self._conn.cursor(DictCursor)

    procedure_db_schema = function_name.split('.')[0] + '.' + function_name.split('.')[1]
    function_name_only = function_name.split('.')[2]
    function_name_with_signature = function_name_only + function_signature
    query = '''
        SHOW FUNCTIONS LIKE %s IN SCHEMA identifier(%s);
    '''
    try:
        cur.execute(query, (function_name_only, procedure_db_schema))
        exists = False
        for rec in cur:
            #print(rec)
            db_name_with_signature = rec['arguments'].split('RETURN')[0].strip().replace(' ','')
            if db_name_with_signature == function_name_with_signature:
                exists = True
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return exists