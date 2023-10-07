from snowflake.connector import DictCursor

def schemas_get(self,database_name:str)->dict:
    cur = self._conn.cursor(DictCursor)
    query = "SHOW SCHEMAS IN DATABASE identifier(%s);"
    data=[]
    try:
        cur.execute(query,(database_name))
        for rec in cur:
            nw = {}
            nw['SCHEMA_NAME'] = rec['name']
            nw['COMMENT'] = rec['comment']
            nw['DATA_RETENTION_TIME_IN_DAYS'] = int(rec['retention_time'])
            nw['OWNER'] = rec['owner']
            data.append(nw)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data