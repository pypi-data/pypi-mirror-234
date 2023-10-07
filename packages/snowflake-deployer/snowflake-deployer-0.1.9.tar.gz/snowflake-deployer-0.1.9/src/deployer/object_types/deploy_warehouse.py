def deploy_warehouse(self, warehouse_name:str, file_hash:str, config:dict)->str:
    # warehouse_name in format <WAREHOUSE_NAME>
    
    # Get vars from config
    WAREHOUSE_TYPE = config['WAREHOUSE_TYPE'] if 'WAREHOUSE_TYPE' in config else None
    WAREHOUSE_SIZE = config['WAREHOUSE_SIZE'] if 'WAREHOUSE_SIZE' in config else None
    MIN_CLUSTER_COUNT = config['MIN_CLUSTER_COUNT'] if 'MIN_CLUSTER_COUNT' in config else None
    MAX_CLUSTER_COUNT = config['MAX_CLUSTER_COUNT'] if 'MAX_CLUSTER_COUNT' in config else None
    SCALING_POLICY = config['SCALING_POLICY'] if 'SCALING_POLICY' in config else None
    AUTO_SUSPEND = config['AUTO_SUSPEND'] if 'AUTO_SUSPEND' in config else None
    AUTO_RESUME = config['AUTO_RESUME'] if 'AUTO_RESUME' in config else None
    OWNER = config['OWNER'] if 'OWNER' in config else None
    COMMENT = config['COMMENT'] if 'COMMENT' in config else None
    ENABLE_QUERY_ACCELERATION = config['ENABLE_QUERY_ACCELERATION'] if 'ENABLE_QUERY_ACCELERATION' in config else None
    QUERY_ACCELERATION_MAX_SCALE_FACTOR = config['QUERY_ACCELERATION_MAX_SCALE_FACTOR'] if 'QUERY_ACCELERATION_MAX_SCALE_FACTOR' in config else None
    TAGS = config['TAGS'] if 'TAGS' in config and config['TAGS'] != '' and config['TAGS'] is not None else []
    GRANTS = config['GRANTS'] if 'GRANTS' in config and config['GRANTS'] != '' and config['GRANTS'] is not None else []
    ENVS = config['DEPLOY_ENV'] if 'DEPLOY_ENV' in config else None

    #if WAREHOUSE_TYPE is not None and WAREHOUSE_TYPE.upper() not in ('STANDARD','SNOWPARK-OPTIMIZED'):
    #    raise Exception('Invalid WAREHOUSE_TYPE in YAML config - must be STANDARD or SNOWPARK-OPTIMIZED')
    #if WAREHOUSE_SIZE is not None and WAREHOUSE_SIZE.replace('-','').upper() not in ('XSMALL','SMALL','MEDIUM','LARGE','XLARGE','XXLARGE','XXXLARGE','X4LARGE','X5LARGE','X6LARGE'):
    #    raise Exception('Invalid WAREHOUSE_SIZE in YAML config - must be a standard warehouse see - see documentation')
    #if MIN_CLUSTER_COUNT is not None and type(MIN_CLUSTER_COUNT) is not int:
    #    raise Exception('Invalid MIN_CLUSTER_COUNT in YAML config - must be a int')
    #if MAX_CLUSTER_COUNT is not None and type(MAX_CLUSTER_COUNT) is not int:
    #    raise Exception('Invalid MAX_CLUSTER_COUNT in YAML config - must be a int')
    #if SCALING_POLICY is not None and SCALING_POLICY.upper() not in ('STANDARD','ECONOMY'):
    #    raise Exception('Invalid SCALING_POLICY in YAML config - must be STANDARD or ECONOMY')
    #if AUTO_SUSPEND is not None and type(AUTO_SUSPEND) is not int:
    #    raise Exception('Invalid AUTO_SUSPEND in YAML config - must be a int')
    #if OWNER is not None and type(OWNER) is not str:
    #    raise Exception('Invalid OWNER in YAML config - must be a string')
    #if COMMENT is not None and type(COMMENT) is not str:
    #    raise Exception('Invalid COMMENT in YAML config - must be a string')
    #if QUERY_ACCELERATION_MAX_SCALE_FACTOR is not None and type(QUERY_ACCELERATION_MAX_SCALE_FACTOR) is not int:
    #    raise Exception('Invalid QUERY_ACCELERATION_MAX_SCALE_FACTOR in YAML config - must be a int')
    #if TAGS is not None and type(TAGS) is not list:
    #    raise Exception('Invalid TAGS in YAML config - must be a list')

    if ENVS is not None and self._deploy_env not in ENVS:
        return_status = 'E'
    else: 
        # Check if db exists 
        wh_exists, sf_owner = self._sf.warehouse_check_exists(warehouse_name)

        if not wh_exists:
            # Create database
            self._sf.warehouse_create(warehouse_name, WAREHOUSE_TYPE, WAREHOUSE_SIZE, MIN_CLUSTER_COUNT, MAX_CLUSTER_COUNT, SCALING_POLICY, AUTO_SUSPEND, AUTO_RESUME, OWNER, COMMENT, ENABLE_QUERY_ACCELERATION, QUERY_ACCELERATION_MAX_SCALE_FACTOR, TAGS, GRANTS, self._deploy_role)

            self._sf.deploy_hash_apply(warehouse_name, file_hash, 'WAREHOUSE', self._deploy_db_name)
            return_status = 'C'
        else:
            self._handle_ownership(sf_owner, 'warehouse', warehouse_name)

            # Get file hash from Snowflake & check if exist
            sf_deploy_hash = self._sf.deploy_hash_get(self._deploy_db_name, warehouse_name, 'warehouse')
            
            if sf_deploy_hash != file_hash:
                self._sf.warehouse_alter(warehouse_name, WAREHOUSE_TYPE, WAREHOUSE_SIZE, MIN_CLUSTER_COUNT, MAX_CLUSTER_COUNT, SCALING_POLICY, AUTO_SUSPEND, AUTO_RESUME, OWNER, COMMENT, ENABLE_QUERY_ACCELERATION, QUERY_ACCELERATION_MAX_SCALE_FACTOR, TAGS, GRANTS)
                self._sf.deploy_hash_apply(warehouse_name, file_hash, 'WAREHOUSE', self._deploy_db_name)
                return_status = 'U'
            else:
                # else - ignore - everything up to date if hashes match
                #print('Ignoring ' + warehouse_name + ' - deploy_hash tag matches file hash')
                return_status = 'I'
    return return_status