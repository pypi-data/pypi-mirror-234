def masking_policy_alter(self,policy_full_name:str, SIGNATURE:list, RETURN_TYPE:str, EXEMPT_OTHER_POLICIES:bool, OWNER:str, COMMENT:str, BODY:str, TAGS:list, GRANTS:list, DEPLOY_ROLE:str):
    # task_name = <db>.<schema>.<task_name>
    cur = self._conn.cursor()
    query = ''
    try:
        # Body
        query = "ALTER MASKING POLICY " + policy_full_name + " SET BODY -> " + BODY
        cur.execute(query)

        # Comment
        COMMENT_SQL = COMMENT if COMMENT is not None else ''
        query = "ALTER MASKING POLICY " + policy_full_name + " SET COMMENT = '" + COMMENT_SQL + "'"
        cur.execute(query)
        
        if TAGS is not None and TAGS != []:
            for t in TAGS:
                tag_key = list(t)[0]
                tag_val = t[tag_key]
                query = 'ALTER MASKING POLICY ' + policy_full_name + ' SET TAG identifier(%s) = %s;'
                params = (tag_key,tag_val)
                cur.execute(query,params)
                
        if OWNER is not None and OWNER != DEPLOY_ROLE: #if owner is deploy role, no need to run this:
            query = "GRANT OWNERSHIP ON MASKING_POLICY " + policy_full_name + " TO ROLE identifier(%s) COPY CURRENT GRANTS;"
            cur.execute(query,(OWNER))

        if GRANTS is not None:
            for grant in GRANTS:
                grant_keys = grant.keys()
                grant_option = grant['GRANT_OPTION'] if 'GRANT_OPTION' in grant_keys else False
                role = ''
                permission = ''
                for key in grant_keys:
                    if key != 'GRANT_OPTION':
                        role = key
                        permission = grant[key]
                if role != '' and permission != '':
                    query = "GRANT " + permission + " ON MASKING POLICY " + policy_full_name + " TO ROLE " + role + ";"
                    cur.execute(query)
                else:
                    raise Exception('Invalid grants for masking policy: ' + policy_full_name)
            
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()

""" 
ALTER MASKING POLICY [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER MASKING POLICY [ IF EXISTS ] <name> SET BODY -> <expression_on_arg_name>

ALTER MASKING POLICY [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER MASKING POLICY [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER MASKING POLICY [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER MASKING POLICY [ IF EXISTS ] <name> UNSET COMMENT
"""