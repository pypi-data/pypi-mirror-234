from snowflake.connector import DictCursor
def procedure_get(self,procedure_name: str, procedure_signature:str)->bool:
    cur = self._conn.cursor(DictCursor)

    procedure_database = procedure_name.split('.')[0]
    procedure_schema = procedure_name.split('.')[1]
    #procedure_db_schema = procedure_database + '.' + procedure_schema
    procedure_name_only = procedure_name.split('.')[2]
    procedure_name_with_signature = procedure_name_only + procedure_signature
    procedure_full_name = procedure_name + procedure_signature
    info_schema = procedure_database + '.INFORMATION_SCHEMA.PROCEDURES'
    try:
        query = "DESC PROCEDURE " + procedure_full_name + ";"
        cur.execute(query)
        info_schema_signature = ''
        for rec in cur:
            if rec['property'] == 'signature':
                info_schema_signature = rec['value']
        if info_schema_signature == '':
            raise Exception("Cannot find procedure")
        
        query = '''
            SELECT * 
            FROM identifier(%s) 
            WHERE PROCEDURE_CATALOG = %s 
                and PROCEDURE_SCHEMA = %s
                and PROCEDURE_NAME = %s
                and ARGUMENT_SIGNATURE = %s
        '''
        
        cur.execute(query, (info_schema, procedure_database, procedure_schema, procedure_name_only, info_schema_signature))
    
        data = {}
        cnt = 0
        for rec in cur:
            cnt += 1
            data['owner'] = rec["PROCEDURE_OWNER"]
            
        if cnt > 1:
            raise Exception("Multiple Functions Found")
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data