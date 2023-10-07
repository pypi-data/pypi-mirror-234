from snowflake.connector import DictCursor
import json

def tags_get(self,database_name:str, schema_name:str)->dict:
    cur = self._conn.cursor(DictCursor)
    schema_with_db = database_name + '.' + schema_name
    query = "SHOW TAGS IN SCHEMA identifier(%s);"
    data=[]
    try:
        cur.execute(query, (schema_with_db))
        for rec in cur:
            nw = {}
            nw['TAG_NAME'] = rec['name']
            nw['COMMENT'] = rec['comment']
            nw['OWNER'] = rec['owner']
            if rec['allowed_values'] is not None:
                nw['ALLOWED_VALUES'] = json.loads(rec['allowed_values'])
            else:
                nw['ALLOWED_VALUES'] = []

            data.append(nw)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data

    