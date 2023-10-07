def warehouse_create(self,warehouse_name, warehouse_type:str, warehouse_size:str, min_cluster_count:int, max_cluster_count:int, scaling_policy:str, auto_suspend:int, auto_resume:bool, owner:str, comment:str, enable_query_acceleration:bool, query_acceleration_max_scale_factor:int, tags:list, grants:list, deploy_role:str):
    cur = self._conn.cursor()
    query = ''
    try:
        query = 'CREATE WAREHOUSE identifier(%s)'
        params = [warehouse_name]
        if warehouse_type is not None:
            query += ' WAREHOUSE_TYPE = %s'
            params.append(warehouse_type)
        if warehouse_size is not None:
            query += ' WAREHOUSE_SIZE = %s'
            params.append(warehouse_size)
        if min_cluster_count is not None:
            query += ' MIN_CLUSTER_COUNT = %s'
            params.append(min_cluster_count)
        if max_cluster_count is not None:
            query += ' MAX_CLUSTER_COUNT = %s'
            params.append(max_cluster_count)
        if scaling_policy is not None:
            query += ' SCALING_POLICY = %s'
            params.append(scaling_policy)
        if auto_suspend is not None:
            query += ' AUTO_SUSPEND = %s'
            params.append(auto_suspend)
        if auto_resume is not None:
            query += ' AUTO_RESUME = %s'
            params.append(auto_resume)
        if comment is not None:
            query += ' COMMENT = %s'
            params.append(comment)
        if enable_query_acceleration is not None:
            query += ' ENABLE_QUERY_ACCELERATION = %s'
            params.append(enable_query_acceleration)
        if query_acceleration_max_scale_factor is not None:
            query += ' QUERY_ACCELERATION_MAX_SCALE_FACTOR = %s'
            params.append(query_acceleration_max_scale_factor)

        cur.execute(query, params)

        if tags is not None and tags != []:
            for t in tags:
                tag_key = list(t)[0]
                tag_val = t[tag_key]
                query = 'ALTER WAREHOUSE identifier(%s) SET TAG identifier(%s) = %s;'
                params = (warehouse_name,tag_key,tag_val)
                cur.execute(query,params)

        if owner is not None and owner != deploy_role: #if owner is deploy role, no need to run this:
            query = '''
                GRANT OWNERSHIP ON WAREHOUSE identifier(%s) TO ROLE identifier(%s) COPY CURRENT GRANTS;
            '''
            cur.execute(query,(warehouse_name, owner))

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
                    query = "GRANT " + permission + " ON WAREHOUSE identifier(%s) TO ROLE " + role + ";"
                    cur.execute(query,(warehouse_name))
                else:
                    raise Exception('Invalid grants for warehouse: ' + warehouse_name)
                
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
# objectProperties ::=
#   WAREHOUSE_TYPE = STANDARD | SNOWPARK-OPTIMIZED
#   WAREHOUSE_SIZE = XSMALL | SMALL | MEDIUM | LARGE | XLARGE | XXLARGE | XXXLARGE | X4LARGE | X5LARGE | X6LARGE
#   MAX_CLUSTER_COUNT = <num>
#   MIN_CLUSTER_COUNT = <num>
#   SCALING_POLICY = STANDARD | ECONOMY
#   AUTO_SUSPEND = <num> | NULL
#   AUTO_RESUME = TRUE | FALSE
#   INITIALLY_SUSPENDED = TRUE | FALSE
#   RESOURCE_MONITOR = <monitor_name>
#   COMMENT = '<string_literal>'
#   ENABLE_QUERY_ACCELERATION = TRUE | FALSE
#   QUERY_ACCELERATION_MAX_SCALE_FACTOR = <num>