from snowflake.connector import DictCursor
from snowflake.connector.errors import DatabaseError, ProgrammingError

def tag_references_get(self,tag_database_name:str, object_name:str, object_type:str)->dict:
    cur = self._conn.cursor(DictCursor)
    query = "select * from table(" + tag_database_name + ".information_schema.tag_references(%s, %s));"

    data=[]
    try:
        cur.execute(query,(object_name, object_type))
        for rec in cur:
            tag = {}
            tag['TAG_DATABASE'] = rec['TAG_DATABASE']
            tag['TAG_SCHEMA'] = rec['TAG_SCHEMA']
            tag['TAG_NAME'] = rec['TAG_NAME']
            tag['TAG_VALUE'] = rec['TAG_VALUE']
            data.append(tag)
    except DatabaseError as db_ex:
        if db_ex.errno == 2003:
            msg = 'MetaOps Error: ' + 'Deployer role does not have access to ' + object_type + ' ' + object_name + '. There is a MetaOps configuration to handle this scenario called HANDLE_OWNERSHIP.  The default value is set to ERROR which gives this error.  This can be set to GRANT in order for the deployer to automatically give itself access.  See docs for more details.'
        else:
            msg = ''
        msg += 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(db_ex) + '\n\n'
        raise Exception(msg)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data