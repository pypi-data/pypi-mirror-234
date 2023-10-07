from snowflake.connector import DictCursor
import json
from src.util.util import cast_string_to_bool

def row_access_policies_get(self,database_name:str, schema_name:str)->dict:
    cur = self._conn.cursor(DictCursor)
    cur_desc = self._conn.cursor(DictCursor)
    schema_with_db = database_name + '.' + schema_name
    query = "SHOW ROW ACCESS POLICIES IN SCHEMA identifier(%s);"
    data=[]
    try:
        cur.execute(query,(schema_with_db))
        for rec in cur:
            nw = {}
            #name, owner, comment, options
            nw['ROW_ACCESS_POLICY_NAME'] = rec['name']
            nw['OWNER'] = rec['owner']
            nw['COMMENT'] = rec['comment']
            
            if rec['options'] is not None and rec['options'] != '':
                options = json.loads(rec['options'])
                if 'EXEMPT_OTHER_POLICIES' in options:
                    nw['EXEMPT_OTHER_POLICIES'] = True if options['EXEMPT_OTHER_POLICIES'].upper() == 'TRUE' else False
                else:
                    nw['EXEMPT_OTHER_POLICIES'] = None
            else:
                nw['EXEMPT_OTHER_POLICIES'] = None
                
            full_policy_name = schema_with_db + '.' + nw['ROW_ACCESS_POLICY_NAME']
            query_desc = "DESC ROW ACCESS POLICY " + full_policy_name
            cur_desc.execute(query_desc)
            for rec_desc in cur_desc:
                # rec_desc['signature'] = (VAL VARCHAR, VAL2 VARCHAR)
                signature_list_raw = rec_desc['signature'].replace('(', '').replace(')', '').split(',')
                signature_list = []
                for signature in signature_list_raw:
                    key = signature.split(' ')[0]
                    val = signature.split(' ')[1]
                    sig = {}
                    sig[key] = val
                    signature_list.append(sig)
                nw['SIGNATURE'] = signature_list 
                nw['RETURN_TYPE'] = rec_desc['return_type']
                nw['BODY'] = rec_desc['body']

            data.append(nw)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
        cur_desc.close()
    return data
