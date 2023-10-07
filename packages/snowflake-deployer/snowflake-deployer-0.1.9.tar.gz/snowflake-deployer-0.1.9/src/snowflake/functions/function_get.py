from snowflake.connector import DictCursor
def function_get(self,function_name: str, function_signature:str)->bool:
    cur = self._conn.cursor(DictCursor)
    
    function_database = function_name.split('.')[0]
    function_schema = function_name.split('.')[1]
    function_name_only = function_name.split('.')[2]
    function_name_with_signature = function_name_only + function_signature
    function_full_name = function_name + function_signature
    info_schema = function_database + '.INFORMATION_SCHEMA.FUNCTIONS'
    try:
        query = "DESC FUNCTION " + function_full_name + ";"
        cur.execute(query)
        info_schema_signature = ''
        for rec in cur:
            if rec['property'] == 'signature':
                info_schema_signature = rec['value']
        if info_schema_signature == '':
            raise Exception("Cannot find function")
        
        query = '''
            SELECT * 
            FROM identifier(%s) 
            WHERE FUNCTION_CATALOG = %s 
                and FUNCTION_SCHEMA = %s
                and FUNCTION_NAME = %s
                and ARGUMENT_SIGNATURE = %s
        '''
        
        cur.execute(query, (info_schema, function_database, function_schema, function_name_only, info_schema_signature))
    
        data = {}
        cnt = 0
        for rec in cur:
            cnt += 1
            data['owner'] = rec["FUNCTION_OWNER"]
            
        if cnt > 1:
            raise Exception("Multiple Functions Found")
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data