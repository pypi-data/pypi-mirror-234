def task_create(self,task_full_name:str, WAREHOUSE:str, SCHEDULE:str, ALLOW_OVERLAPPING_EXECUTION:bool, ERROR_INTEGRATION:str, PREDECESSORS:list, COMMENT:str, ENABLED:bool, CONDITION:str, USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE:str, USER_TASK_TIMEOUT_MS:str, SUSPEND_TASK_AFTER_NUM_FAILURES:str, BODY:str, OWNER:str, TAGS:list, GRANTS:list, deploy_role:str):
    # task_name = <db>.<schema>.<task_name>
    cur = self._conn.cursor()
    query = ''
    try:
        sql_warehouse = "  WAREHOUSE = '" + WAREHOUSE + "' " if WAREHOUSE is not None and WAREHOUSE != '' else ''
        sql_user_task_managed_initial_warehouse_size = "  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = '" + USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE + "'" if USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE is not None and USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE != '' else ''
        sql_schedule = "  SCHEDULE = '" + SCHEDULE + "' " if SCHEDULE is not None and SCHEDULE != '' else ''
        #sql_config = "  CONFIG = '" + CONFIG + "'" if CONFIG is not None and CONFIG != '' else ''
        sql_allow_overlapping_execution = "  ALLOW_OVERLAPPING_EXECUTION = " + str(ALLOW_OVERLAPPING_EXECUTION) if ALLOW_OVERLAPPING_EXECUTION is not None and ALLOW_OVERLAPPING_EXECUTION != '' else ''
        sql_user_task_timeout_ms = "  USER_TASK_TIMEOUT_MS = " + USER_TASK_TIMEOUT_MS if USER_TASK_TIMEOUT_MS is not None and USER_TASK_TIMEOUT_MS != '' else ''
        sql_suspend_task_aftern_num_failures = "  SUSPEND_TASK_AFTER_NUM_FAILURES = " + SUSPEND_TASK_AFTER_NUM_FAILURES if SUSPEND_TASK_AFTER_NUM_FAILURES is not None and SUSPEND_TASK_AFTER_NUM_FAILURES != '' else ''
        sql_error_integration = "  ERROR_INTEGRATION = '" + ERROR_INTEGRATION + "' " if ERROR_INTEGRATION is not None and ERROR_INTEGRATION != '' else ''
        sql_comment = "  COMMENT = '" + COMMENT + "' " if COMMENT is not None else ''
        sql_after = "  AFTER = " + ', '.join(PREDECESSORS) if PREDECESSORS is not None and PREDECESSORS != [] else ''
        sql_when = "  WHEN = " + CONDITION if CONDITION is not None and CONDITION != '' else ''

        query = "CREATE OR REPLACE TASK " + task_full_name + " "
        query += sql_warehouse
        query += sql_user_task_managed_initial_warehouse_size
        query += sql_schedule
        #query += sql_config
        query += sql_allow_overlapping_execution
        query += sql_user_task_timeout_ms
        query += sql_suspend_task_aftern_num_failures
        query += sql_error_integration
        query += sql_comment
        query += sql_after
        query += sql_when
        query += " as " + BODY
        
        cur.execute(query)
        
        if ENABLED:
            query = "ALTER TASK " + task_full_name + " RESUME"
            cur.execute(query)
            
        if TAGS is not None and TAGS != []:
            for t in TAGS:
                tag_key = list(t)[0]
                tag_val = t[tag_key]
                query = 'ALTER TASK ' + task_full_name + ' SET TAG identifier(%s) = %s;'
                params = (tag_key,tag_val)
                cur.execute(query,params)
                
        if OWNER is not None and OWNER != deploy_role: #if owner is deploy role, no need to run this:
            query = "GRANT OWNERSHIP ON TASK " + task_full_name + " TO ROLE identifier(%s) COPY CURRENT GRANTS;"
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
                    query = "GRANT " + permission + " ON TASK identifier(%s) TO ROLE " + role + ";"
                    cur.execute(query,(task_full_name))
                else:
                    raise Exception('Invalid grants for task: ' + task_full_name)
            
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
# CREATE [ OR REPLACE ] TASK [ IF NOT EXISTS ] <name>
#   [ { WAREHOUSE = <string> } | { USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = <string> } ]
#   [ SCHEDULE = '{ <num> MINUTE | USING CRON <expr> <time_zone> }' ]
#   [ CONFIG = <configuration_string> ]
#   [ ALLOW_OVERLAPPING_EXECUTION = TRUE | FALSE ]
#   [ <session_parameter> = <value> [ , <session_parameter> = <value> ... ] ]
#   [ USER_TASK_TIMEOUT_MS = <num> ]
#   [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
#   [ ERROR_INTEGRATION = <integration_name> ]
#   [ COPY GRANTS ]
#   [ COMMENT = '<string_literal>' ]
#   [ AFTER <string> [ , <string> , ... ] ]
# [ WHEN <boolean_expr> ]
# AS
#   <sql>