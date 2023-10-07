def deploy_procedure(self, procedure_name_with_signature:str, file_hash:str, file_hash_code:str, config:dict, body_code:str)->str:
    # procedure_name_with_signature = <db>.<schema>.<name>__<signature>
    
    # Object name in deployer wrapper includes the signature (ie. (varchar,int) ) as 
    # Procedures with the same name but different signatures may exist
    procedure_name = procedure_name_with_signature.split('__')[0]
    procedure_signature = procedure_name_with_signature.split('__')[1]
    sql_procedure_name = '"' + procedure_name.split('.')[0] + '"."' + procedure_name.split('.')[1] + '"."' + procedure_name.split('.')[2] + '"' + procedure_name_with_signature.split('__')[1]
    
    # Get vars from config
    INPUT_ARGS = config['INPUT_ARGS'] if 'INPUT_ARGS' in config and config['INPUT_ARGS'] != '' and config['INPUT_ARGS'] is not None else []
    IS_SECURE = config['IS_SECURE'] if 'IS_SECURE' in config else None
    RETURNS = config['RETURNS'] if 'RETURNS' in config else None
    LANGUAGE = config['LANGUAGE'] if 'LANGUAGE' in config else None
    NULL_HANDLING = config['NULL_HANDLING'] if 'NULL_HANDLING' in config else None
    EXECUTE_AS = config['EXECUTE_AS'] if 'EXECUTE_AS' in config else None
    OWNER = config['OWNER'] if 'OWNER' in config else None
    COMMENT = config['COMMENT'] if 'COMMENT' in config else None
    TAGS = config['TAGS'] if 'TAGS' in config and config['TAGS'] != '' and config['TAGS'] is not None else []
    BODY = body_code
    GRANTS = config['GRANTS'] if 'c' in config and config['GRANTS'] != '' and config['GRANTS'] is not None else []
    ENVS = config['DEPLOY_ENV'] if 'DEPLOY_ENV' in config else None

    if config['LANGUAGE'] == 'PYTHON':
        IMPORTS = config['IMPORTS'] if 'IMPORTS' in config and config['IMPORTS'] != '' and config['IMPORTS'] is not None else []
        HANDLER = config['HANDLER'] if 'HANDLER' in config else None
        RUNTIME_VERSION = config['RUNTIME_VERSION'] if 'RUNTIME_VERSION' in config else None
        PACKAGES = config['PACKAGES'] if 'PACKAGES' in config and config['PACKAGES'] != '' and config['PACKAGES'] is not None else []
        #INSTALLED_PACKAGES = config['INSTALLED_PACKAGES'] if 'INSTALLED_PACKAGES' in config else None
    else:
        IMPORTS = None
        HANDLER = None
        RUNTIME_VERSION = None 
        PACKAGES = None
        
    #if INPUT_ARGS is not None and type(INPUT_ARGS) is not dict:
    #    for i in INPUT_ARGS:
    #        if ('name' not in i and 'NAME' not in i) or ('type' not in i and 'TYPE' not in i):
    #            raise Exception('INPUT_ARGS must be an array of {"name":<name>,"type":<type>}')
    #if IS_SECURE is not None and type(IS_SECURE) is not bool:
    #    raise Exception('Invalid IS_SECURE in YAML config - must be a bool')
    #
    #if RETURNS is not None and type(RETURNS) is not str:
    #    raise Exception('Invalid IS_SECURE in YAML config - must be a string')
    #if IS_SECURE is not None and type(IS_SECURE) is not bool:
    #    raise Exception('Invalid IS_SECURE in YAML config - must be a bool')
    #if LANGUAGE is not None and LANGUAGE.upper() not in ('SCALA','JAVA','SQL','PYTHON','JAVASCRIPT'):
    #    raise Exception('Invalid LANGUAGE in YAML config - Snowflake supports SCALA,JAVA,SQL,PYTHON,JAVASCRIPT')
    #if NULL_HANDLING is not None and NULL_HANDLING.upper() not in ('CALLED ON NULL INPUT','RETURNS NULL ON NULL INPUT','STRICT'):
    #    raise Exception('Invalid NULL_HANDLING in YAML config - must be (CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT)')
    #if EXECUTE_AS is not None and EXECUTE_AS not in ('CALLER','OWNER'):
    #    raise Exception('Invalid EXECUTE_AS in YAML config - must be (CALLER | OWNER)')
    #if BODY is not None and type(BODY) is not str:
    #    raise Exception('Invalid BODY in YAML config - must be a string')

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
        procedure_exists = self._sf.procedure_check_exists(procedure_name, procedure_signature)

        if not procedure_exists:
            # Create database
            self._sf.procedure_create(procedure_name, sql_procedure_name, IS_SECURE, INPUT_ARGS, RETURNS, LANGUAGE, NULL_HANDLING, EXECUTE_AS, COMMENT, BODY, IMPORTS, HANDLER, RUNTIME_VERSION, PACKAGES, OWNER, TAGS, GRANTS, self._deploy_role)

            self._sf.deploy_hash_apply(sql_procedure_name, file_hash, 'PROCEDURE', self._deploy_db_name)
            self._sf.deploy_code_hash_apply(sql_procedure_name, file_hash_code, 'PROCEDURE', self._deploy_db_name)
        
            return_status = 'C'
        else:
            proc_details = self._sf.procedure_get(procedure_name, procedure_signature)
            sf_owner = proc_details['owner']
            self._handle_ownership(sf_owner, 'procedure', sql_procedure_name)

            # Get file hash from Snowflake & check if exist
            sf_deploy_hash = self._sf.deploy_hash_get(self._deploy_db_name, sql_procedure_name, 'procedure')
            sf_deploy_code_hash = self._sf.deploy_code_hash_get(self._deploy_db_name, sql_procedure_name, 'procedure')
            
            if sf_deploy_hash != file_hash or sf_deploy_code_hash != file_hash_code:
                self._sf.procedure_create(procedure_name, sql_procedure_name, IS_SECURE, INPUT_ARGS, RETURNS, LANGUAGE, NULL_HANDLING, EXECUTE_AS, COMMENT, BODY, IMPORTS, HANDLER, RUNTIME_VERSION, PACKAGES, OWNER, TAGS, GRANTS, self._deploy_role)
                self._sf.deploy_hash_apply(sql_procedure_name, file_hash, 'PROCEDURE', self._deploy_db_name)
                self._sf.deploy_code_hash_apply(sql_procedure_name, file_hash_code, 'PROCEDURE', self._deploy_db_name)
        
                return_status = 'U'
            else:
                return_status = 'I'
    return return_status