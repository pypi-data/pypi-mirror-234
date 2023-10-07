def deploy_database(self, database_name:str, file_hash:str, config)->str:
    
    # Get vars from config
    DATA_RETENTION_TIME_IN_DAYS = int(config['DATA_RETENTION_TIME_IN_DAYS']) if 'DATA_RETENTION_TIME_IN_DAYS' in config else None 
    COMMENT = config['COMMENT'] if 'COMMENT' in config else None
    OWNER = config['OWNER'] if 'OWNER' in config else None
    TAGS = config['TAGS'] if 'TAGS' in config and config['TAGS'] != '' and config['GRANTS'] is not None else []
    GRANTS = config['GRANTS'] if 'GRANTS' in config and config['GRANTS'] != '' and config['GRANTS'] is not None else []
    ENVS = config['DEPLOY_ENV'] if 'DEPLOY_ENV' in config else None
        
    # commenting this out and moving to the validator class
    #if DATA_RETENTION_TIME_IN_DAYS is not None and type(DATA_RETENTION_TIME_IN_DAYS) is not int:
    #    raise Exception('Invalid DATA_RETENTION_TIME_IN_DAYS in YAML config - must be a int')
    #if COMMENT is not None and type(COMMENT) is not str:
    #    raise Exception('Invalid COMMENT in YAML config - must be a string')
    #if OWNER is not None and type(OWNER) is not str:
    #    raise Exception('Invalid OWNER in YAML config - must be a string')
    #if TAGS is not None and type(TAGS) is not list:
    #    raise Exception('Invalid TAGS in YAML config - must be a list')

    # Check if db exists 
    if ENVS is not None and self._deploy_env not in ENVS:
        return_status = 'E'
    else: 
        db_exists, sf_owner = self._sf.database_check_exists(database_name)
            
        if not db_exists:
            # Create database
            self._sf.database_create(database_name, DATA_RETENTION_TIME_IN_DAYS, COMMENT, OWNER, TAGS, GRANTS, self._deploy_role)

            self._sf.deploy_hash_apply(database_name, file_hash, 'DATABASE', self._deploy_db_name)

            return_status = 'C'
        else:
            self._handle_ownership(sf_owner, 'database', database_name)

            # Get file hash from Snowflake & check if exist
            sf_deploy_hash = self._sf.deploy_hash_get(self._deploy_db_name, database_name, 'database')
            
            if sf_deploy_hash != file_hash:
                self._sf.database_alter(database_name, DATA_RETENTION_TIME_IN_DAYS, COMMENT, OWNER, TAGS, GRANTS)
                self._sf.deploy_hash_apply(database_name, file_hash, 'DATABASE', self._deploy_db_name)
            
                return_status = 'U'
            else:
                # else - ignore - everything up to date if hashes match
                #print('Ignoring ' + database_name + ' - deploy_hash tag matches file hash')

                return_status = 'I'

    return return_status