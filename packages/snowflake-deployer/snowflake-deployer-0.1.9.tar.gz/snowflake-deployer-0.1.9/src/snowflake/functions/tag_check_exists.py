from snowflake.connector import DictCursor

def tag_check_exists(self,tag_full_name: str)->bool:
    cur = self._conn.cursor(DictCursor)
    schema_full_name = tag_full_name.split('.')[0] + '.' + tag_full_name.split('.')[1]
    tag_name = tag_full_name.split('.')[2]
    database_name = tag_full_name.split('.')[0]

    try:
        query = '''
            SHOW TAGS LIKE %s in schema identifier(%s);
        '''

        cur.execute(query, (tag_name,schema_full_name))
        res = {}
        res['tag_exists'] = (cur.rowcount>0)
        for rec in cur:
            res['comment'] = rec['comment']
            res['owner'] = rec['owner']
            res['allowed_values'] = rec['allowed_values']
        if 'owner' not in res:
            res['owner'] = None

        query = '''
            SELECT ARRAY_AGG(POLICY_DB || '.' || POLICY_SCHEMA || '.' || POLICY_NAME) as MASKING_POLICIES
            FROM TABLE (''' + database_name + '''.INFORMATION_SCHEMA.POLICY_REFERENCES(
                REF_ENTITY_DOMAIN => 'TAG',
                REF_ENTITY_NAME => %s ))
            WHERE POLICY_KIND = 'MASKING_POLICY'
                and POLICY_STATUS = 'ACTIVE'
            ;
            '''
        if res['tag_exists']:
            cur.execute(query, (tag_full_name))
            for rec in cur:
                res['masking_policies'] = rec['MASKING_POLICIES']
        # 'PROD_CONTROL.GOVERNANCE.SEMANTIC'
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    #return (res.rowcount>0)
    return res

    #masking_policies