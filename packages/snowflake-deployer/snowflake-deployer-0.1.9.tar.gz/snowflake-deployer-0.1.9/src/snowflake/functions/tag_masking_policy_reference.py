from snowflake.connector import DictCursor
import json

def tag_masking_policy_reference(self,full_tag_name:str)->dict:
    cur = self._conn.cursor(DictCursor)

    database_name = full_tag_name.split('.')[0]
    #schema_full_name = tag_full_name.split('.')[0] + '.' + tag_full_name.split('.')[1]
    #tag_name = tag_full_name.split('.')[2]

    data=[]
    try:
        query = '''
                SELECT POLICY_DB || '.' || POLICY_SCHEMA || '.' || POLICY_NAME as MASKING_POLICIES
                FROM TABLE (''' + database_name + '''.INFORMATION_SCHEMA.POLICY_REFERENCES(
                    REF_ENTITY_DOMAIN => 'TAG',
                    REF_ENTITY_NAME => %s ))
                WHERE POLICY_KIND = 'MASKING_POLICY'
                    and POLICY_STATUS = 'ACTIVE'
                ; 
                '''
        cur.execute(query, (full_tag_name))
        for rec in cur:
            data.append(rec['MASKING_POLICIES'])
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data

    