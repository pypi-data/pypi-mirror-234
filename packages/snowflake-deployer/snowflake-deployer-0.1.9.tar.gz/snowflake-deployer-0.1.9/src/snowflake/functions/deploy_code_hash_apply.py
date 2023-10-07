def deploy_code_hash_apply(self,object_name:str, file_hash:str, object_type:str, deploy_db_name:str):
    cur = self._conn.cursor()
    query = ''
    try:
        full_tag_name = deploy_db_name + '.TAG.DEPLOY_CODE_HASH'
        # NOTE: object_name cannot be an identifier as not all objects will support this
        query = 'ALTER ' + object_type + ' ' + object_name + ' SET TAG identifier(%s) = %s;'
        cur.execute(query,(full_tag_name,file_hash))
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
