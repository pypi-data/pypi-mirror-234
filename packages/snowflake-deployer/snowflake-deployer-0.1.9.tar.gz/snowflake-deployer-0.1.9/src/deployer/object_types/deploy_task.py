def deploy_task(self, task_full_name:str, file_hash:str, file_hash_code:str, config:dict, body_code:str)->str:
    # task_full_name = <db>.<schema>.<name>
   
    # Get vars from config
    WAREHOUSE = config['WAREHOUSE'] if 'WAREHOUSE' in config else None
    SCHEDULE = config['SCHEDULE'] if 'SCHEDULE' in config else None
    ALLOW_OVERLAPPING_EXECUTION = config['ALLOW_OVERLAPPING_EXECUTION'] if 'ALLOW_OVERLAPPING_EXECUTION' in config else None
    ERROR_INTEGRATION = config['ERROR_INTEGRATION'] if 'ERROR_INTEGRATION' in config else None
    PREDECESSORS = config['PREDECESSORS'] if 'PREDECESSORS' in config and config['PREDECESSORS'] != '' and config['PREDECESSORS'] is not None else []
    OWNER = config['OWNER'] if 'OWNER' in config else None
    COMMENT = config['COMMENT'] if 'COMMENT' in config else None
    ENABLED = config['ENABLED'] if 'ENABLED' in config else None
    CONDITION = config['CONDITION'] if 'CONDITION' in config else None
    USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = config['USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE'] if 'USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE' in config else None
    USER_TASK_TIMEOUT_MS = config['USER_TASK_TIMEOUT_MS'] if 'USER_TASK_TIMEOUT_MS' in config else None
    SUSPEND_TASK_AFTER_NUM_FAILURES = config['SUSPEND_TASK_AFTER_NUM_FAILURES'] if 'SUSPEND_TASK_AFTER_NUM_FAILURES' in config else None
    
    TAGS = config['TAGS'] if 'TAGS' in config and config['TAGS'] != '' and config['TAGS'] is not None else []
    BODY = body_code
    GRANTS = config['GRANTS'] if 'GRANTS' in config and config['GRANTS'] != '' and config['GRANTS'] is not None else []
    ENVS = config['DEPLOY_ENV'] if 'DEPLOY_ENV' in config else None

    if WAREHOUSE is not None and WAREHOUSE != '' and USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE is not None and USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE != '':
        raise Exception('Only one of WAREHOUSE or USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE can have a value.')
    #if ((WAREHOUSE is None or WAREHOUSE == '') and (USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE is None or USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE == '')):
    #    raise Exception('WAREHOUSE or USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE must have a value (but only 1).')

    if ENVS is not None and self._deploy_env not in ENVS:
        return_status = 'E'
    else:
        # Check if db exists 

        task_exists, sf_owner = self._sf.task_check_exists(task_full_name)

        if not task_exists:
            # Create database
            self._sf.task_create(task_full_name, WAREHOUSE, SCHEDULE, ALLOW_OVERLAPPING_EXECUTION, ERROR_INTEGRATION, PREDECESSORS, COMMENT, ENABLED, CONDITION, USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE, USER_TASK_TIMEOUT_MS, SUSPEND_TASK_AFTER_NUM_FAILURES, BODY, OWNER, TAGS, GRANTS, self._deploy_role)

            self._sf.deploy_hash_apply(task_full_name, file_hash, 'TASK', self._deploy_db_name)
            self._sf.deploy_code_hash_apply(task_full_name, file_hash_code, 'TASK', self._deploy_db_name)
        
            return_status = 'C'
        else:
            self._handle_ownership(sf_owner, 'task', task_full_name)

            # Get file hash from Snowflake & check if exist
            sf_deploy_hash = self._sf.deploy_hash_get(self._deploy_db_name, task_full_name, 'task')
            sf_deploy_code_hash = self._sf.deploy_code_hash_get(self._deploy_db_name, task_full_name, 'task')
            
            if sf_deploy_hash != file_hash or sf_deploy_code_hash != file_hash_code:
                self._sf.task_alter(task_full_name, WAREHOUSE, SCHEDULE, ALLOW_OVERLAPPING_EXECUTION, ERROR_INTEGRATION, PREDECESSORS, COMMENT, ENABLED, CONDITION, USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE, USER_TASK_TIMEOUT_MS, SUSPEND_TASK_AFTER_NUM_FAILURES, BODY, OWNER, TAGS, GRANTS, self._deploy_role)
                self._sf.deploy_hash_apply(task_full_name, file_hash, 'TASK', self._deploy_db_name)
                self._sf.deploy_code_hash_apply(task_full_name, file_hash_code, 'TASK', self._deploy_db_name)
        
                return_status = 'U'
            else:
                return_status = 'I'
    return return_status