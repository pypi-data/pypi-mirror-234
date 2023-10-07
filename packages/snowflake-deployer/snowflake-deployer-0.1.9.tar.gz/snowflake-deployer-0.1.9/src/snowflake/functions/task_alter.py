from snowflake.connector import DictCursor
import json
def task_alter(self,task_full_name:str, WAREHOUSE:str, SCHEDULE:str, ALLOW_OVERLAPPING_EXECUTION:bool, ERROR_INTEGRATION:str, PREDECESSORS:list, COMMENT:str, ENABLED:bool, CONDITION:str, USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE:str, USER_TASK_TIMEOUT_MS:str, SUSPEND_TASK_AFTER_NUM_FAILURES:str, BODY:str, OWNER:str, TAGS:list, GRANTS:list, deploy_role:str):
    # task_name = <db>.<schema>.<task_name>
    cur = self._conn.cursor(DictCursor)
    query = ''
    try:
        set_cnt = 0
        unset_cnt = 0
        
        if WAREHOUSE is not None and WAREHOUSE != '':
            sql_warehouse_set = "  WAREHOUSE = '" + WAREHOUSE + "' "
            sql_warehouse_unset = ""
            set_cnt += 1
        else:
            sql_warehouse_set = ""
            sql_warehouse_unset = ', ' if unset_cnt > 0 else ''
            sql_warehouse_unset += " WAREHOUSE "
            unset_cnt += 1
        
        if USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE is not None and USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE != '':
            sql_user_task_managed_initial_warehouse_size_set = "  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = '" + USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE + "' "
            sql_user_task_managed_initial_warehouse_size_unset = ""
            set_cnt += 1
        else:
            sql_user_task_managed_initial_warehouse_size_set = ""
            sql_user_task_managed_initial_warehouse_size_unset = ', ' if unset_cnt > 0 else ''
            sql_user_task_managed_initial_warehouse_size_unset += " USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE "
            unset_cnt += 1

        if SCHEDULE is not None and SCHEDULE != '':
            sql_schedule_set = "  SCHEDULE = '" + SCHEDULE + "' "
            sql_schedule_unset = ""
            set_cnt += 1
        else:
            sql_schedule_set = ""
            sql_schedule_unset = ', ' if unset_cnt > 0 else ''
            sql_schedule_unset += " SCHEDULE "
            unset_cnt += 1

        if ALLOW_OVERLAPPING_EXECUTION is not None:
            sql_allow_overlapping_execution_set = "  ALLOW_OVERLAPPING_EXECUTION = " + str(ALLOW_OVERLAPPING_EXECUTION)
            sql_allow_overlapping_execution_unset = ""
            set_cnt += 1
        else:
            sql_allow_overlapping_execution_set = ""
            sql_allow_overlapping_execution_unset = ', ' if unset_cnt > 0 else ''
            sql_allow_overlapping_execution_unset += " ALLOW_OVERLAPPING_EXECUTION "
            unset_cnt += 1

        if USER_TASK_TIMEOUT_MS is not None and USER_TASK_TIMEOUT_MS != '':
            sql_user_task_timeout_ms_set = "  USER_TASK_TIMEOUT_MS = " + USER_TASK_TIMEOUT_MS
            sql_user_task_timeout_ms_unset = ""
            set_cnt += 1
        else:
            sql_user_task_timeout_ms_set = ""
            sql_user_task_timeout_ms_unset = ', ' if unset_cnt > 0 else ''
            sql_user_task_timeout_ms_unset += " USER_TASK_TIMEOUT_MS "
            unset_cnt += 1
        
        if SUSPEND_TASK_AFTER_NUM_FAILURES is not None and SUSPEND_TASK_AFTER_NUM_FAILURES != '':
            sql_suspend_task_after_num_failures_set = "  SUSPEND_TASK_AFTER_NUM_FAILURES = " + SUSPEND_TASK_AFTER_NUM_FAILURES 
            sql_suspend_task_after_num_failures_unset = ""
            set_cnt += 1
        else:
            sql_suspend_task_after_num_failures_set = ""
            sql_suspend_task_after_num_failures_unset = ', ' if unset_cnt > 0 else ''
            sql_suspend_task_after_num_failures_unset += " SUSPEND_TASK_AFTER_NUM_FAILURES "
            unset_cnt += 1

        if ERROR_INTEGRATION is not None and ERROR_INTEGRATION != '':
            sql_error_integration_set = "  ERROR_INTEGRATION = '" + ERROR_INTEGRATION + "' "
            sql_error_integration_unset = ""
            set_cnt += 1
        else:
            sql_error_integration_set = ""
            sql_error_integration_unset = ', ' if unset_cnt > 0 else ''
            sql_error_integration_unset += " ERROR_INTEGRATION "
            unset_cnt += 1

        if COMMENT is not None and COMMENT != '':
            sql_comment_set = "  COMMENT = '" + COMMENT + "' "
            sql_comment_unset = ""
            set_cnt += 1
        else:
            sql_comment_set = ""
            sql_comment_unset = ', ' if unset_cnt > 0 else ''
            sql_comment_unset += " COMMENT "
            unset_cnt += 1

        # Set params
        if set_cnt > 0:
            query = "ALTER TASK " + task_full_name + " SET "
            query += sql_warehouse_set
            query += sql_user_task_managed_initial_warehouse_size_set
            query += sql_schedule_set
            query += sql_allow_overlapping_execution_set
            query += sql_user_task_timeout_ms_set
            query += sql_suspend_task_after_num_failures_set
            query += sql_error_integration_set
            query += sql_comment_set
            cur.execute(query)

        # Unset params not set
        if unset_cnt > 0:
            query = "ALTER TASK " + task_full_name + " UNSET "
            query += sql_warehouse_unset
            query += sql_user_task_managed_initial_warehouse_size_unset
            query += sql_schedule_unset
            query += sql_allow_overlapping_execution_unset
            query += sql_user_task_timeout_ms_unset
            query += sql_suspend_task_after_num_failures_unset
            query += sql_error_integration_unset
            query += sql_comment_unset
            
            cur.execute(query)

            
        # Resume/Suspend
        if ENABLED:
            query = "ALTER TASK " + task_full_name + " RESUME;"
            cur.execute(query)
        else:
            query = "ALTER TASK " + task_full_name + " SUSPEND;"
            cur.execute(query)

        # Body
        query = "ALTER TASK " + task_full_name + " MODIFY AS " + BODY
        cur.execute(query)

        # When condition
        if CONDITION is not None and CONDITION != '':
            query = "ALTER TASK " + task_full_name + " MODIFY WHEN " + CONDITION
            cur.execute(query)

        #  PREDECESSORS alter

        # get current PREDECESSORS
        schema_with_db = task_full_name.split('.')[0] + '.' + task_full_name.split('.')[1]
        task_name = task_full_name.split('.')[2]
        query = "SHOW TASKS LIKE '" + task_name + "' IN SCHEMA identifier(%s);"
        data = []
        cur.execute(query,(schema_with_db))
        for rec in cur:
            PREDECESSORS_DB = json.loads(rec['predecessors'])
        if PREDECESSORS_DB is None:
            PREDECESSORS_DB = []
        if PREDECESSORS is None:
            PREDECESSORS = []

        predecessors_to_remove = list(set(PREDECESSORS_DB) - set(PREDECESSORS))
        predecessors_to_add = list(set(PREDECESSORS) - set(PREDECESSORS_DB))

        if predecessors_to_remove != []:
            query = "ALTER TASK " + task_full_name + " REMOVE AFTER " + ", ".join(predecessors_to_remove)
            cur.execute(query)

        if predecessors_to_add != []:
            query = "ALTER TASK " + task_full_name + " ADD AFTER " + ", ".join(predecessors_to_add)
            cur.execute(query)
        
        # Tags
        if TAGS is not None and TAGS != []:
            for t in TAGS:
                tag_key = list(t)[0]
                tag_val = t[tag_key]
                query = 'ALTER TASK ' + task_full_name + ' SET TAG identifier(%s) = %s;'
                params = (tag_key,tag_val)
                cur.execute(query,params)

        # Owner    
        if OWNER is not None and OWNER != deploy_role: #if owner is deploy role, no need to run this:
            query = "GRANT OWNERSHIP ON TASK " + task_full_name + " TO ROLE identifier(%s) COPY CURRENT GRANTS;"
            cur.execute(query,(OWNER))

        # Grants
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
""" 
ALTER TASK [ IF EXISTS ] <name> RESUME | SUSPEND

ALTER TASK [ IF EXISTS ] <name> REMOVE AFTER <string> [ , <string> , ... ] | ADD AFTER <string> [ , <string> , ... ]

ALTER TASK [ IF EXISTS ] <name> SET
  [ WAREHOUSE = <string> ]
  [ SCHEDULE = '{ <number> MINUTE | USING CRON <expr> <time_zone> }' ]
  [ CONFIG = <configuration_string> ]
  [ ALLOW_OVERLAPPING_EXECUTION = TRUE | FALSE ]
  [ USER_TASK_TIMEOUT_MS = <num> ]
  [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
  [ COMMENT = <string> ]
  [ <session_parameter> = <value> [ , <session_parameter> = <value> ... ] ]

ALTER TASK [ IF EXISTS ] <name> UNSET
  [ WAREHOUSE ]
  [ SCHEDULE ]
  [ CONFIG ]
  [ ALLOW_OVERLAPPING_EXECUTION ]
  [ USER_TASK_TIMEOUT_MS ]
  [ SUSPEND_TASK_AFTER_NUM_FAILURES ]
  [ COMMENT ]
  [ <session_parameter> [ , <session_parameter> ... ] ]
  [ , ... ]

ALTER TASK [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER TASK [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER TASK [ IF EXISTS ] <name> MODIFY AS <sql>

ALTER TASK [ IF EXISTS ] <name> MODIFY WHEN <boolean_expr> """