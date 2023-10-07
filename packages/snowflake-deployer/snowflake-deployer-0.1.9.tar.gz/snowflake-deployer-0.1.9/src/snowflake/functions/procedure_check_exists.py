from snowflake.connector import DictCursor
def procedure_check_exists(self,procedure_name: str, procedure_signature:str)->bool:
    # procedure_name: 
    cur = self._conn.cursor(DictCursor)

    procedure_db_schema = procedure_name.split('.')[0] + '.' + procedure_name.split('.')[1]
    procedure_name_only = procedure_name.split('.')[2]
    procedure_name_with_signature = procedure_name_only + procedure_signature
    query = '''
        SHOW PROCEDURES LIKE %s IN SCHEMA identifier(%s);
    '''
    try:
        cur.execute(query, (procedure_name_only, procedure_db_schema))
        exists = False
        #owner = None
        for rec in cur:
            #print(rec)
            db_name_with_signature = rec['arguments'].split('RETURN')[0].strip().replace(' ','')
            if db_name_with_signature == procedure_name_with_signature:
                exists = True
            #owner = rec["owner"]
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return exists