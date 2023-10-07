from snowflake.connector import DictCursor

def objects_get(self,database_name:str, schema_name:str)->dict:
    cur = self._conn.cursor(DictCursor)
    schema_with_db = database_name + '.' + schema_name
    query = "SHOW OBJECTS IN SCHEMA identifier(%s);"
    data=[]
    try:
        cur.execute(query,(schema_with_db))
        for rec in cur:
            if rec['schema_name'] not in ['INFORMATION_SCHEMA']:
                nw = {}
                nw['OBJECT_NAME'] = rec['name']
                nw['OBJECT_TYPE'] = rec['kind']
                nw['COMMENT'] = rec['comment']
                nw['OWNER'] = rec['owner']
                nw['RETENTION_TIME_IN_DAYS'] = int(rec['retention_time'])
                data.append(nw)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data