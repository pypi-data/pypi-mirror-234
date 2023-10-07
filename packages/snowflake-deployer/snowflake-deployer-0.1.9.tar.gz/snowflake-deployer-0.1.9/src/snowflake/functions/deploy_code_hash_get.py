#from snowflake.connector import DictCursor

def deploy_code_hash_get(self,deploy_db_name:str, object:str, object_type:str)->str:
    cur = self._conn.cursor()
    
    full_tag_name = deploy_db_name + '.TAG.DEPLOY_CODE_HASH'
    query = '''
        SELECT system$get_tag(%s, %s, %s) as TAG_VALUE;
    '''
    data=[]
    try:
        res = cur.execute(query,(full_tag_name, object, object_type)).fetchall()
        tag_value = res[0][0]
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return tag_value
