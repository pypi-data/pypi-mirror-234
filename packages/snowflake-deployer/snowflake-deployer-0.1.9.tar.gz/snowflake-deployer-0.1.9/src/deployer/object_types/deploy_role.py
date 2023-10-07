def deploy_role(self, role_name:str, file_hash:str, config:dict)->str:
    # warehouse_name in format <WAREHOUSE_NAME>
    
    # Get vars from config
    OWNER = config['OWNER'] if 'OWNER' in config else None
    COMMENT = config['COMMENT'] if 'COMMENT' in config else None
    PARENT_ROLES = config['PARENT_ROLES'] if 'PARENT_ROLES' in config else None
    TAGS = config['TAGS'] if 'TAGS' in config and config['TAGS'] != '' and config['TAGS'] is not None else []
    ENVS = config['DEPLOY_ENV'] if 'DEPLOY_ENV' in config else None

    #if OWNER is not None and type(OWNER) is not str:
    #    raise Exception('Invalid OWNER in YAML config - must be a string')
    #if COMMENT is not None and type(COMMENT) is not str:
    #    raise Exception('Invalid COMMENT in YAML config - must be a string')
    #if TAGS is not None and type(TAGS) is not list:
    #    raise Exception('Invalid TAGS in YAML config - must be a list')
    if ENVS is not None and self._deploy_env not in ENVS:
        return_status = 'E'
    else:
        # Check if db exists 
        role_exists, sf_owner = self._sf.role_check_exists(role_name)

        if not role_exists:
            # Create database
            self._sf.role_create(role_name, OWNER, COMMENT, PARENT_ROLES, TAGS, self._deploy_role)

            self._sf.deploy_hash_apply(role_name, file_hash, 'ROLE', self._deploy_db_name)
            return_status = 'C'
        else:
            self._handle_ownership(sf_owner, 'role', role_name)

            # Get file hash from Snowflake & check if exist
            sf_deploy_hash = self._sf.deploy_hash_get(self._deploy_db_name, role_name, 'role')
            
            if sf_deploy_hash != file_hash:
                self._sf.role_alter(role_name, OWNER, COMMENT, PARENT_ROLES, TAGS)
                self._sf.deploy_hash_apply(role_name, file_hash, 'ROLE', self._deploy_db_name)

                return_status = 'U'
            else:
                # else - ignore - everything up to date if hashes match
                #print('Ignoring ' + role_name + ' - deploy_hash tag matches file hash')
                return_status = 'I'

    return return_status