def tag_alter(self,tag_name:str, comment:str, owner:str, allowed_values:list, masking_policies:list):
    cur = self._conn.cursor()
    query = ''
    try:
        if comment is not None:
            query = 'ALTER TAG identifier(%s) SET COMMENT = %s'
            params = [tag_name, comment]
            cur.execute(query, params)
        
        if allowed_values is not None and allowed_values != []:
            query = 'ALTER TAG identifier(%s) ADD ALLOWED_VALUES '
            params = [tag_name]
            for av in allowed_values:
                query += "%s,"
                params.append(str(av))
            query = query[:-1] # remove last comma
            cur.execute(query, params)
            
        if masking_policies is not None and masking_policies != []:
            query = 'ALTER TAG ' + tag_name + ' SET '
            params = []
            for masking_policy in masking_policies:
                query += ' MASKING POLICY ' + masking_policy + ','
            query = query[:-1]  # remove last comma
            cur.execute(query)
            
        if owner is not None:
            query = '''
                GRANT OWNERSHIP ON TAG identifier(%s) TO ROLE identifier(%s) COPY CURRENT GRANTS;
            '''
            cur.execute(query,(tag_name, owner))

    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
# ALTER TAG [ IF EXISTS ] <name> RENAME TO <new_name>

# ALTER TAG [ IF EXISTS ] <name> { ADD | DROP } ALLOWED_VALUES '<val_1>' [ , '<val_2>' , [ ... ] ]

# ALTER TAG <name> UNSET ALLOWED_VALUES

# ALTER TAG <name> SET MASKING POLICY <masking_policy_name> [ , MASKING POLICY <masking_policy_2_name> , ... ]
#                                                           [ FORCE ]

# ALTER TAG <name> UNSET MASKING POLICY <masking_policy_name> [ , MASKING POLICY <masking_policy_2_name> , ... ]

# ALTER TAG [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

# ALTER TAG [ IF EXISTS ] <name> UNSET COMMENT