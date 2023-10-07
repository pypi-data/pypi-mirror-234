from snowflake.connector import DictCursor
import json
from src.util.util import cast_string_to_bool

def tasks_get(self,database_name:str, schema_name:str)->dict:
    cur = self._conn.cursor(DictCursor)
    schema_with_db = database_name + '.' + schema_name
    query = "SHOW TASKS IN SCHEMA identifier(%s);"
    data=[]
    try:
        cur.execute(query,(schema_with_db))
        for rec in cur:
            nw = {}
            nw['TASK_NAME'] = rec['name']
            nw['WAREHOUSE'] = rec['warehouse']
            nw['SCHEDULE'] = rec['schedule']
            nw['ALLOW_OVERLAPPING_EXECUTION'] = cast_string_to_bool(rec['allow_overlapping_execution'])
            nw['PREDECESSORS'] = json.loads(rec['predecessors'])
            nw['CONDITION'] = rec['condition']
            nw['ERROR_INTEGRATION'] = rec['error_integration'] if rec['error_integration'].upper() != 'NULL' else None
            nw['OWNER'] = rec['owner']
            nw['COMMENT'] = rec['comment']
            nw['DEFINITION'] = rec['definition']
            nw['ENABLED'] = True if rec['state'].upper() == 'STARTED' else False
            #USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE
            #USER_TASK_TIMEOUT_MS
            #SUSPEND_TASK_AFTER_NUM_FAILURES
            data.append(nw)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return data


#CREATE OR REPLACE TASK PROD_CONTROL.AUTOMATION.TEST_TASK
#  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
#  --WAREHOUSE (check to see if this or above is there)
#  SCHEDULE = 'USING CRON  0 * * * * America/Los_Angeles'
#  --CONFIG ... no
#  ALLOW_OVERLAPPING_EXECUTION = TRUE
#  --ERROR_INTEGRATION .. yes (string)
#  USER_TASK_TIMEOUT_MS = 600
#  SUSPEND_TASK_AFTER_NUM_FAILURES = 5
#  COMMENT = 'test task'
#  --AFTER ... yes (PREDECESSORS)
#  --WHEN ... yes (CONDITION)
#AS -- definition
#BEGIN
#  ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF';
#  SELECT CURRENT_TIMESTAMP;
#END;
#-- state (ENABLED)