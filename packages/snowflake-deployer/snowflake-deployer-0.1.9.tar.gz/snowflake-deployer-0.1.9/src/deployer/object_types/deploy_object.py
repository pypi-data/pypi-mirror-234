from src.common.exceptions import feature_not_supported
def deploy_object(self, object_name:str, file_hash:str, config:dict)->str:
    # object_name in format <DATABASE_NAME>.<SCHEMA_NAME>.<OBJECT_NAME> 
    # THIS CAN BE A TABLE OR VIEW!!!
    
    # Get vars from config
    DATA_RETENTION_TIME_IN_DAYS = int(config['DATA_RETENTION_TIME_IN_DAYS']) if 'DATA_RETENTION_TIME_IN_DAYS' in config else None 
    COMMENT = config['COMMENT'] if 'COMMENT' in config else None
    OWNER = config['OWNER'] if 'OWNER' in config else None
    CHANGE_TRACKING = config['CHANGE_TRACKING'] if 'CHANGE_TRACKING' in config else None
    TAGS = config['TAGS'] if 'TAGS' in config and config['TAGS'] != '' and config['TAGS'] is not None else []
    COLUMNS = config['COLUMNS'] if 'COLUMNS' in config and config['COLUMNS'] != '' and config['COLUMNS'] is not None else []
    GRANTS = config['GRANTS'] if 'GRANTS' in config and config['GRANTS'] != '' and config['GRANTS'] is not None else []
    ENVS = config['DEPLOY_ENV'] if 'DEPLOY_ENV' in config else None
    ROW_ACCESS_POLICY = config['ROW_ACCESS_POLICY'] if 'ROW_ACCESS_POLICY' in config else None
    ROW_ACCESS_POLICY_COLUMNS = config['ROW_ACCESS_POLICY_COLUMNS'] if 'ROW_ACCESS_POLICY_COLUMNS' in config and config['ROW_ACCESS_POLICY_COLUMNS'] != '' and config['ROW_ACCESS_POLICY_COLUMNS'] is not None else []

    #if DATA_RETENTION_TIME_IN_DAYS is not None and type(DATA_RETENTION_TIME_IN_DAYS) is not int:
    #    raise Exception('Invalid DATA_RETENTION_TIME_IN_DAYS in YAML config - must be a int')
    #if COMMENT is not None and type(COMMENT) is not str:
    #    raise Exception('Invalid COMMENT in YAML config - must be a string')
    #if OWNER is not None and type(OWNER) is not str:
    #    raise Exception('Invalid OWNER in YAML config - must be a string')
    #if CHANGE_TRACKING is not None and type(CHANGE_TRACKING) is not bool:
    #    raise Exception('Invalid CHANGE_TRACKING in YAML config - must be a boolean')
    #if TAGS is not None and type(TAGS) is not list:
    #    raise Exception('Invalid TAGS in YAML config - must be a list')
    #if COLUMNS is not None and type(COLUMNS) is not list:
    #    raise Exception('Invalid COLUMNS in YAML config - must be a list')
    if ROW_ACCESS_POLICY is not None and ROW_ACCESS_POLICY != '':
        if ROW_ACCESS_POLICY_COLUMNS is None or ROW_ACCESS_POLICY_COLUMNS == []:
            raise Exception('Must include ROW_ACCESS_POLICY_COLUMNS if ROW_ACCESS_POLICY included')
    if ENVS is not None and self._deploy_env not in ENVS:
        return_status = 'E'
    else: 
        # Check if schema exists 
        object_exists, sf_owner = self._sf.object_check_exists(object_name)

        if not object_exists:
            # Create Object
            #raise feature_not_supported('object', 'create new object')
            print('Ignoring object: ' + object_name + '; Object does not exist')
            #self._sf.schema_create(object_name, DATA_RETENTION_TIME_IN_DAYS, COMMENT, OWNER, TAGS)
            #self._sf.deploy_hash_apply(object_name, file_hash, 'SCHEMA', deploy_db_name)
            return_status = 'I'
            #return_status = 'C'
        else:
            self._handle_ownership(sf_owner, 'table', object_name)

            # Get file hash from Snowflake & check if exist
            sf_deploy_hash = self._sf.deploy_hash_get(self._deploy_db_name, object_name, 'table')
            
            if sf_deploy_hash != file_hash:
                self._sf.object_alter(object_name, DATA_RETENTION_TIME_IN_DAYS, COMMENT, OWNER, CHANGE_TRACKING, ROW_ACCESS_POLICY, ROW_ACCESS_POLICY_COLUMNS, TAGS, GRANTS)
                
                for column in COLUMNS:
                    if 'TAGS' in column: # only update column if something exists to update
                        self._sf.column_alter(object_name, column['NAME'], column['TAGS'])
                
                self._sf.deploy_hash_apply(object_name, file_hash, 'TABLE', self._deploy_db_name)

                return_status = 'U'
            else:
                # else - ignore - everything up to date if hashes match
                #print('Ignoring ' + object_name + ' - deploy_hash tag matches file hash')

                return_status = 'I'
    return return_status