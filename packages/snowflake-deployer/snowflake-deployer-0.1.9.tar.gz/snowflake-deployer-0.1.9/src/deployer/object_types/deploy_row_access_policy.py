def deploy_row_access_policy(self, policy_full_name:str, file_hash:str, file_hash_code:str, config:dict, body_code:str)->str:
    # policy_full_name = <db>.<schema>.<name>
    #SIGNATURE:list, RETURN_TYPE:str, EXEMPT_OTHER_POLICIES:bool, OWNER:str, COMMENT:str, BODY:str, TAGS:list, GRANTS:list, DEPLOY_ROLE:str
    #SIGNATURE, RETURN_TYPE, EXEMPT_OTHER_POLICIES, OWNER, COMMENT, BODY, TAGS, GRANTS, DEPLOY_ROLE
    # Get vars from config
    SIGNATURE = config['SIGNATURE'] if 'SIGNATURE' in config and config['SIGNATURE'] != '' and config['SIGNATURE'] is not None else []
    RETURN_TYPE = config['RETURN_TYPE'] if 'RETURN_TYPE' in config else None
    OWNER = config['OWNER'] if 'OWNER' in config else None
    COMMENT = config['COMMENT'] if 'COMMENT' in config else None

    TAGS = config['TAGS'] if 'TAGS' in config and config['TAGS'] != '' and config['TAGS'] is not None else []
    BODY = body_code
    GRANTS = config['GRANTS'] if 'GRANTS' in config and config['GRANTS'] != '' and config['GRANTS'] is not None else []
    ENVS = config['DEPLOY_ENV'] if 'DEPLOY_ENV' in config else None

    if ENVS is not None and self._deploy_env not in ENVS:
        return_status = 'E'
    else:
        # Check if db exists 

        policy_exists, sf_owner = self._sf.row_access_policy_check_exists(policy_full_name)

        if not policy_exists:
            # Create database
            self._sf.row_access_policy_create(policy_full_name, SIGNATURE, RETURN_TYPE, OWNER, COMMENT, BODY, TAGS, GRANTS, self._deploy_role)

            self._sf.deploy_hash_apply(policy_full_name, file_hash, 'ROW ACCESS POLICY', self._deploy_db_name)
            self._sf.deploy_code_hash_apply(policy_full_name, file_hash_code, 'ROW ACCESS POLICY', self._deploy_db_name)
        
            return_status = 'C'
        else:
            self._handle_ownership(sf_owner, 'row access policy', policy_full_name)

            # Get file hash from Snowflake & check if exist
            sf_deploy_hash = self._sf.deploy_hash_get(self._deploy_db_name, policy_full_name, 'row access policy')
            sf_deploy_code_hash = self._sf.deploy_code_hash_get(self._deploy_db_name, policy_full_name, 'row access policy')
            
            if sf_deploy_hash != file_hash or sf_deploy_code_hash != file_hash_code:
                self._sf.row_access_policy_alter(policy_full_name, SIGNATURE, RETURN_TYPE, OWNER, COMMENT, BODY, TAGS, GRANTS, self._deploy_role)
                self._sf.deploy_hash_apply(policy_full_name, file_hash, 'ROW ACCESS POLICY', self._deploy_db_name)
                self._sf.deploy_code_hash_apply(policy_full_name, file_hash_code, 'ROW ACCESS POLICY', self._deploy_db_name)
        
                return_status = 'U'
            else:
                return_status = 'I'
    return return_status