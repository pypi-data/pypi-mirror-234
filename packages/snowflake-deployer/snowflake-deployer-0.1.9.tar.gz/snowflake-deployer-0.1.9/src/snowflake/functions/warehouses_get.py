from snowflake.connector import DictCursor

def warehouses_get(self,env_warehouse_prefix:str)->dict:
    cur = self._conn.cursor(DictCursor)
    query = "SHOW WAREHOUSES like '" + env_warehouse_prefix + "%' in ACCOUNT;"
    data=[]
    try:
        cur.execute(query)
        for rec in cur:
            nw = {}
            nw['WAREHOUSE_NAME'] = rec['name']
            nw['WAREHOUSE_TYPE'] = rec['type']
            nw['WAREHOUSE_SIZE'] = rec['size']
            nw['MIN_CLUSTER_COUNT'] = rec['min_cluster_count']
            nw['MAX_CLUSTER_COUNT'] = rec['max_cluster_count']
            nw['SCALING_POLICY'] = rec['scaling_policy']
            nw['AUTO_SUSPEND'] = rec['auto_suspend']
            nw['AUTO_RESUME'] = True if rec['auto_resume'].upper() == 'TRUE' else False
            #nw['RESOURCE_MONITOR'] = rec['resource_monitor']
            nw['OWNER'] = rec['owner']
            nw['COMMENT'] = rec['comment']
            nw['ENABLE_QUERY_ACCELERATION'] = True if rec['enable_query_acceleration'].upper() == 'TRUE' else False
            nw['QUERY_ACCELERATION_MAX_SCALE_FACTOR'] = rec['query_acceleration_max_scale_factor']
            data.append(nw)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data