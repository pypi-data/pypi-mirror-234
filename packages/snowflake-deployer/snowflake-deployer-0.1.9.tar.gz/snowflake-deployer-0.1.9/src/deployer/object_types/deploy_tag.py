import json
def deploy_tag(self, tag_name:str, file_hash:str, config:dict)->str:
    # tag_name in format <DATABASE_NAME>.<SCHEMA_NAME>.<TAG_NAME>
    
    # Get vars from config
    COMMENT = config['COMMENT'] if 'COMMENT' in config else None
    OWNER = config['OWNER'] if 'OWNER' in config else None
    ALLOWED_VALUES = config['ALLOWED_VALUES'] if 'ALLOWED_VALUES' in config and config['ALLOWED_VALUES'] != '' and config['ALLOWED_VALUES'] is not None else []
    MASKING_POLICIES = config['MASKING_POLICIES'] if 'MASKING_POLICIES' in config and config['MASKING_POLICIES'] != '' and config['MASKING_POLICIES'] is not None else []
    ENVS = config['DEPLOY_ENV'] if 'DEPLOY_ENV' in config else None

    #if COMMENT is not None and type(COMMENT) is not str:
    #    raise Exception('Invalid COMMENT in YAML config - must be a string')
    #if OWNER is not None and type(OWNER) is not str:
    #    raise Exception('Invalid OWNER in YAML config - must be a string')
    #if ALLOWED_VALUES is not None and type(ALLOWED_VALUES) is not list:
    #    raise Exception('Invalid ALLOWED_VALUES in YAML config - must be a list')

    # Check if schema exists 
    tag_res = self._sf.tag_check_exists(tag_name)
    
    tag_exists = tag_res['tag_exists']
    sf_owner = tag_res['owner']

    if ENVS is not None and self._deploy_env not in ENVS:
        return_status = 'E'
    else: 
        if not tag_exists:
            # Create Schema
            self._sf.tag_create(tag_name, COMMENT, OWNER, ALLOWED_VALUES, MASKING_POLICIES, self._deploy_role)
            #self._sf.deploy_hash_apply(tag_name, file_hash, 'TAG', deploy_db_name)

            return_status = 'C'
        else:
            self._handle_ownership(sf_owner, 'tag', tag_name)

            # Get file hash from Snowflake & check if exist
            #sf_deploy_hash = self._sf.deploy_hash_get(deploy_db_name, tag_name, 'tag')
            if tag_res['allowed_values'] is not None:
                sf_allowed_values = json.loads(tag_res['allowed_values'])
            else:
                sf_allowed_values = []
            if tag_res['masking_policies'] is not None:
                sf_masking_policies = json.loads(tag_res['masking_policies'])
            else:
                sf_masking_policies = []

            # SNOWFLAKE DOESN'T SUPPORT TAGGING A TAG ... SO NEED TO CHECK THE VALUES OF THE TAG ITSELF RATHER THAN USING THE DEPLOY_HASH TAG
            if( 
                (COMMENT is not None and COMMENT != tag_res['comment']) 
                or (OWNER is not None and OWNER != tag_res['owner']) 
                or (ALLOWED_VALUES is not None and sorted(ALLOWED_VALUES) != sorted(sf_allowed_values))
                or (MASKING_POLICIES is not None and sorted(MASKING_POLICIES) != sorted(sf_masking_policies))
                ):
                
                self._sf.tag_alter(tag_name, COMMENT, OWNER, ALLOWED_VALUES, MASKING_POLICIES)

                return_status = 'U'
            else:
                return_status = 'I'
            #if sf_deploy_hash != file_hash:
                #self._sf.deploy_hash_apply(tag_name, file_hash, 'TAG', deploy_db_name)
            # else - ignore - everything up to date if hashes match
            
    return return_status
