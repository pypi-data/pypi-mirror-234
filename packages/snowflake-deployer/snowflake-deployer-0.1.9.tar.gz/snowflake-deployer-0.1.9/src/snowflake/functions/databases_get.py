from snowflake.connector import DictCursor

def databases_get(self,env_database_prefix:str)->dict:
    cur = self._conn.cursor(DictCursor)
    query = "SHOW DATABASES like '" + env_database_prefix + "%' in ACCOUNT;"

    data=[]
    try:
        cur.execute(query)
        for rec in cur:
            nw = {}
            nw['DATABASE_NAME'] = rec['name']
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