def tag_create(self,tag_name:str, comment:str, owner:str, allowed_values:list, masking_policies:list, deploy_role:str):
    cur = self._conn.cursor()
    query = ''
    try:
        query = 'CREATE TAG ' + tag_name
        #params = [tag_name]
        params = []
        if allowed_values is not None and allowed_values != []:
            query += ' ALLOWED_VALUES '
            for av in allowed_values:
                query += "%s,"
                params.append(str(av))
            query = query[:-1] # remove last comma
            
            
        if comment is not None:
            query += ' COMMENT = %s'
            params.append(comment)

        cur.execute(query, params)

        if masking_policies is not None and masking_policies != []:
            query = 'ALTER TAG ' + tag_name + ' SET '
            params = []
            for masking_policy in masking_policies:
                query += 'MASKING POLICY ' + masking_policy + ','
                #params.append(masking_policy)
            query = query[:-1] # remove last comma
            cur.execute(query)
            
        if owner is not None and owner != deploy_role: #if owner is deploy role, no need to run this:
            query = '''
                GRANT OWNERSHIP ON TAG identifier(%s) TO ROLE identifier(%s) COPY CURRENT GRANTS;
            '''
            cur.execute(query,(tag_name, owner))

    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
#CREATE [ OR REPLACE ] TAG [ IF NOT EXISTS ] <name> [ COMMENT = '<string_literal>' ]
#
#CREATE [ OR REPLACE ] TAG [ IF NOT EXISTS ] <name>
#    [ ALLOWED_VALUES '<val_1>' [ , '<val_2>' , [ ... ] ] ]
#CREATE TAG PROD_SECURITY.PUBLIC.TEST ALLOWED_VALUES 'test1','test2','test3' COMMENT='Some comment';
