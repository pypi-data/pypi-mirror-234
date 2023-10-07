def role_alter(self,role_name, owner:str, comment:str, parent_roles:list, tags:list):
    cur = self._conn.cursor()
    query = ''
    try:
        query = 'ALTER ROLE identifier(%s) SET '
        params = [role_name]
        if comment is not None:
            query += ' COMMENT = %s'
            params.append(comment)
        if len(params) > 1: # something to execute
            cur.execute(query, params)

        if tags is not None and tags != []:
            for t in tags:
                tag_key = list(t)[0]
                tag_val = t[tag_key]
                query = 'ALTER ROLE identifier(%s) SET TAG identifier(%s) = %s;'
                params = (role_name,tag_key,tag_val)
                cur.execute(query,params)

        if parent_roles is not None and parent_roles != []:
            for parent_role in parent_roles:
                query = "GRANT ROLE " + role_name + " TO ROLE " + parent_role + ";"
                cur.execute(query)
                
        if owner is not None:
            query = '''
                GRANT OWNERSHIP ON ROLE identifier(%s) TO ROLE identifier(%s) COPY CURRENT GRANTS;
            '''
            cur.execute(query,(role_name, owner))

    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
