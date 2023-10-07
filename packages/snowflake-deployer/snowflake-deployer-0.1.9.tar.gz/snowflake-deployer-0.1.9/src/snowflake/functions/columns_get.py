from snowflake.connector import DictCursor

def columns_get(self,database_name:str, schema_name:str, object_name:str)->dict:
    cur = self._conn.cursor(DictCursor)
    object_with_db_schema = database_name + '.' + schema_name + '.' + object_name
    
    query = """
        SELECT c.COLUMN_NAME, a.TAG_LIST
        FROM """ + database_name + """.INFORMATION_SCHEMA.COLUMNS c
            left join 
                (SELECT COLUMN_NAME
                    , ARRAY_AGG(object_construct('TAG_DATABASE',TAG_DATABASE,'TAG_SCHEMA',TAG_SCHEMA,'TAG_NAME',TAG_NAME,'TAG_VALUE',TAG_VALUE)) as TAG_LIST
                FROM table(""" + database_name + """.information_schema.tag_references_all_columns(%s, 'table'))
                WHERE LEVEL = 'COLUMN'
                GROUP BY COLUMN_NAME
                ) a
                on c.COLUMN_NAME = a.COLUMN_NAME
        WHERE c.table_catalog = %s
            and c.table_schema = %s
            and c.table_name = %s
        ;
    """
    data=[]
    try:
        cur.execute(query,(object_with_db_schema,database_name,schema_name,object_name))
        for rec in cur:
            nw = {}
            nw['NAME'] = rec['COLUMN_NAME']
            nw['TAG_LIST'] = rec['TAG_LIST']
                     
            data.append(nw)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data