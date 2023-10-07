def column_alter(self,object_name:str, column_name:str, tags:list):
    cur = self._conn.cursor()
    query = ''
    try:
        if tags is not None and tags != []:
            for t in tags:
                tag_key = list(t)[0]
                tag_val = t[tag_key]
                query = 'ALTER TABLE identifier(%s) ALTER COLUMN "' + column_name + '" SET TAG identifier(%s) = %s;'
                params = (object_name,tag_key,tag_val)
                cur.execute(query,params)

    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
