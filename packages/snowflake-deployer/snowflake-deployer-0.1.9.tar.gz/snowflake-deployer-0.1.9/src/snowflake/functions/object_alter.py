def object_alter(self,object_name:str, data_retention_time_in_days:int, comment:str, owner:str, change_tracking:bool, row_access_policy:str, row_access_policy_columns:list, tags:list, grants:list):
    cur = self._conn.cursor()
    query = ''
    try:
        # NOTE - alter table will also alter schema
        query = 'ALTER TABLE identifier(%s) SET '
        params = [object_name]
        if data_retention_time_in_days is not None:
            query += ' DATA_RETENTION_TIME_IN_DAYS = %s'
            params.append(data_retention_time_in_days)
        if comment is not None:
            query += ' COMMENT = %s'
            params.append(comment)
        if change_tracking is not None:
            query += ' CHANGE_TRACKING = %s'
            params.append(change_tracking)
        if len(params) > 1: # something to execute
            cur.execute(query, params)

        if tags is not None and tags != []:
            for t in tags:
                tag_key = list(t)[0]
                tag_val = t[tag_key]
                query = 'ALTER TABLE identifier(%s) SET TAG identifier(%s) = %s;'
                params = (object_name,tag_key,tag_val)
                cur.execute(query,params)

        if owner is not None:
            query = '''
                GRANT OWNERSHIP ON TABLE identifier(%s) TO ROLE identifier(%s) COPY CURRENT GRANTS;
            '''
            cur.execute(query,(object_name, owner))

        if row_access_policy is not None and row_access_policy != '':
            query = 'ALTER TABLE identifier(%s) ADD ROW ACCESS POLICY ' + row_access_policy + ' ON ('
            for row_access_policy_column in row_access_policy_columns:
                query += '"' + row_access_policy_column + '",'
            query = query[:-1] # remove last comma
            query += ');'
            cur.execute(query,(object_name))

        if grants is not None:
            for grant in grants:
                grant_keys = grant.keys()
                grant_option = grant['GRANT_OPTION'] if 'GRANT_OPTION' in grant_keys else False
                role = ''
                permission = ''
                for key in grant_keys:
                    if key != 'GRANT_OPTION':
                        role = key
                        permission = grant[key]
                if role != '' and permission != '':
                    query = "GRANT " + permission + " ON TABLE identifier(%s) TO ROLE " + role + ";"
                    cur.execute(query,(object_name))
                else:
                    raise Exception('Invalid grants for object: ' + object_name)
            
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
