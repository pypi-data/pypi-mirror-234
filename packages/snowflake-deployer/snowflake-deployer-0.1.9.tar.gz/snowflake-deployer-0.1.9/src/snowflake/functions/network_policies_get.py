from snowflake.connector import DictCursor

def network_policies_get(self)->dict:
    cur = self._conn.cursor(DictCursor)
    cur_desc = self._conn.cursor(DictCursor)
    query = "SHOW NETWORK POLICIES in ACCOUNT;"
    data=[]
    try:
        cur.execute(query)
        for rec in cur:
            nw = {}
            nw['NETWORK_POLICY_NAME'] = rec['name']
            nw['COMMENT'] = rec['comment']

            query_desc = "DESC NETWORK POLICY " + nw['NETWORK_POLICY_NAME']
            cur_desc.execute(query_desc)
            allowed_ip_list = []
            blocked_ip_list = []
            for rec_desc in cur_desc:
                #       name       |     value    
                #  ALLOWED_IP_LIST or BLOCKED_IP_LIST
                if rec_desc['name'] == 'ALLOWED_IP_LIST':
                    allowed_ip_list.append(rec_desc['value'])
                elif rec_desc['name'] == 'BLOCKED_IP_LIST':
                    blocked_ip_list.append(rec_desc['value'])
            nw['ALLOWED_IP_LIST'] = allowed_ip_list
            nw['BLOCKED_IP_LIST'] = blocked_ip_list
            data.append(nw)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data

# NOTES
# Pausing on this one.... there's no way to currently get the owner.  This needs a little more testing