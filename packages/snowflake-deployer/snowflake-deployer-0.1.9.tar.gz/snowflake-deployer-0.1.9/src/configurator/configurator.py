import os
#from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from src.common.exceptions import file_not_exists, missing_parameter
import yaml
from src.common.enums import HANDLE_OWNERSHIP_OPTION

class configurator:
    def __init__(self, args):
        self._args = args
    
    def _get_param_from_env_or_config(self, config_file:dict, param_name:str, default_value:str)->str:
        if param_name in os.environ:
            param = os.environ.get(param_name)
        elif param_name in config_file and config_file[param_name] != '':
            param = config_file[param_name]
        else:
            param = default_value
        return param

    def _get_param_from_env_or_config_list(self, config_file:dict, param_name:str)->list:
        if param_name in os.environ:
            param = os.environ.get(param_name)
        elif param_name in config_file and config_file[param_name] != '' and config_file[param_name] != []:
            param = config_file[param_name]
        else:
            param = []
        if param is None:
            param = []
        return param

    def get_config(self)->dict:
        
        # Set up parameters
        SNOWFLAKE_USERNAME = self._args["SNOWFLAKE_USERNAME"]
        SNOWFLAKE_ACCOUNT = self._args["SNOWFLAKE_ACCOUNT"]
        SNOWFLAKE_WAREHOUSE = self._args["SNOWFLAKE_WAREHOUSE"]
        SNOWFLAKE_ROLE = self._args["SNOWFLAKE_ROLE"]
        DEPLOY_CONFIG_PATH = self._args["CONFIG_PATH"]
        
        ###########################################################
        # Params that require env var or argument
        if SNOWFLAKE_USERNAME == '':
            if "SNOWFLAKE_USERNAME" in os.environ and os.environ.get('SNOWFLAKE_USERNAME') != '':
                SNOWFLAKE_USERNAME = os.environ.get('SNOWFLAKE_USERNAME')
            else: 
                raise missing_parameter('SNOWFLAKE_USERNAME')
        if SNOWFLAKE_ACCOUNT == '':
            if "SNOWFLAKE_ACCOUNT" in os.environ and os.environ.get('SNOWFLAKE_ACCOUNT') != '':
                SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT')
            else: 
                raise missing_parameter('SNOWFLAKE_ACCOUNT')

        if "SNOWFLAKE_PRIVATE_KEY_PASSWORD" in os.environ:
            SNOWFLAKE_PRIVATE_KEY_PASSWORD = os.environ.get('SNOWFLAKE_PRIVATE_KEY_PASSWORD')
        else:
            raise missing_parameter('SNOWFLAKE_PRIVATE_KEY_PASSWORD')
        
        if "SNOWFLAKE_PRIVATE_KEY" in os.environ:
            SNOWFLAKE_PRIVATE_KEY = os.environ.get('SNOWFLAKE_PRIVATE_KEY')
        else:
            raise missing_parameter('SNOWFLAKE_PRIVATE_KEY')
        
        ###########################################################
        # Params that can also be in file  

        # Get config path
        if DEPLOY_CONFIG_PATH != '':
            DEPLOY_PATH_SET = True
        elif DEPLOY_CONFIG_PATH == '':
            if "DEPLOY_CONFIG_PATH" in os.environ and os.environ.get('DEPLOY_CONFIG_PATH') != '':
                DEPLOY_CONFIG_PATH = os.environ.get('DEPLOY_CONFIG_PATH')
                DEPLOY_PATH_SET = True
            else: 
                DEPLOY_CONFIG_PATH = "deploy_config.yml"
                DEPLOY_PATH_SET = False

        # Check if config file exists if and error if included
        config_file_exists = os.path.exists(DEPLOY_CONFIG_PATH)
        if not config_file_exists and DEPLOY_PATH_SET:
            raise file_not_exists(DEPLOY_CONFIG_PATH, 'Config path included in execution')
        if config_file_exists:
            with open(DEPLOY_CONFIG_PATH, "r") as yamlfile:
                config_file = yaml.load(yamlfile, Loader=yaml.FullLoader)
        else:
            config_file = {}

        if SNOWFLAKE_WAREHOUSE == '':
            if "SNOWFLAKE_WAREHOUSE" in os.environ and os.environ.get('SNOWFLAKE_WAREHOUSE') != '':
                SNOWFLAKE_WAREHOUSE = os.environ.get('SNOWFLAKE_WAREHOUSE')
                WAREHOUSE_SET = True
            elif "SNOWFLAKE_WAREHOUSE" in config_file and config_file['SNOWFLAKE_WAREHOUSE'] != '':
                SNOWFLAKE_WAREHOUSE = config_file['SNOWFLAKE_WAREHOUSE']
                WAREHOUSE_SET = True
            else: 
                WAREHOUSE_SET = False # Optional as can use optional from the user in Snowflake
        else:
            WAREHOUSE_SET = True 

        if SNOWFLAKE_ROLE == '':
            if "SNOWFLAKE_ROLE" in os.environ and os.environ.get('SNOWFLAKE_ROLE') != '':
                SNOWFLAKE_ROLE = os.environ.get('SNOWFLAKE_ROLE')
                ROLE_SET = True
            elif "SNOWFLAKE_ROLE" in config_file and config_file['SNOWFLAKE_ROLE'] != '':
                SNOWFLAKE_ROLE = config_file['SNOWFLAKE_ROLE']
                ROLE_SET = True
            else: 
                ROLE_SET = False # Optional as can use optional from the user in Snowflake
        else:
            ROLE_SET = True 

        if "ENV_DATABASE_PREFIX" in os.environ:
            ENV_DATABASE_PREFIX = os.environ.get('ENV_DATABASE_PREFIX')
        elif "ENV_DATABASE_PREFIX" in config_file and config_file['ENV_DATABASE_PREFIX'] != '':
            ENV_DATABASE_PREFIX = config_file['ENV_DATABASE_PREFIX']
        else:
            ENV_DATABASE_PREFIX = ''

        if "ENV_WAREHOUSE_PREFIX" in os.environ:
            ENV_WAREHOUSE_PREFIX = os.environ.get('ENV_WAREHOUSE_PREFIX')
        elif "ENV_WAREHOUSE_PREFIX" in config_file and config_file['ENV_WAREHOUSE_PREFIX'] != '':
            ENV_WAREHOUSE_PREFIX = config_file['ENV_WAREHOUSE_PREFIX']
        else:
            ENV_WAREHOUSE_PREFIX = ''

        if "ENV_ROLE_PREFIX" in os.environ:
            ENV_ROLE_PREFIX = os.environ.get('ENV_ROLE_PREFIX')
        elif "ENV_ROLE_PREFIX" in config_file and config_file['ENV_ROLE_PREFIX'] != '':
            ENV_ROLE_PREFIX = config_file['ENV_ROLE_PREFIX']
        else:
            ENV_ROLE_PREFIX = ''

        if "ENV_PROCEDURE_PREFIX" in os.environ:
            ENV_PROCEDURE_PREFIX = os.environ.get('ENV_PROCEDURE_PREFIX')
        elif "ENV_PROCEDURE_PREFIX" in config_file and config_file['ENV_PROCEDURE_PREFIX'] != '':
            ENV_PROCEDURE_PREFIX = config_file['ENV_PROCEDURE_PREFIX']
        else:
            ENV_PROCEDURE_PREFIX = ''

        if "ENV_FUNCTION_PREFIX" in os.environ:
            ENV_FUNCTION_PREFIX = os.environ.get('ENV_FUNCTION_PREFIX')
        elif "ENV_FUNCTION_PREFIX" in config_file and config_file['ENV_FUNCTION_PREFIX'] != '':
            ENV_FUNCTION_PREFIX = config_file['ENV_FUNCTION_PREFIX']
        else:
            ENV_FUNCTION_PREFIX = ''

        if "OBJECT_METADATA_ONLY" in os.environ:
            OBJECT_METADATA_ONLY = os.environ.get('OBJECT_METADATA_ONLY')
        elif "OBJECT_METADATA_ONLY" in config_file and config_file['OBJECT_METADATA_ONLY'] != '':
            OBJECT_METADATA_ONLY = config_file['OBJECT_METADATA_ONLY']
        else:
            OBJECT_METADATA_ONLY = ''
        
        if "MAX_THREADS" in os.environ:
            MAX_THREADS = os.environ.get('MAX_THREADS')
        elif "MAX_THREADS" in config_file and config_file['MAX_THREADS'] != '':
            MAX_THREADS = config_file['MAX_THREADS']
        else:
            MAX_THREADS = 3
        
        if "DEPLOY_DATABASE_NAME" in os.environ:
            DEPLOY_DATABASE_NAME = os.environ.get('DEPLOY_DATABASE_NAME')
        elif "DEPLOY_DATABASE_NAME" in config_file and config_file['DEPLOY_DATABASE_NAME'] != '':
            DEPLOY_DATABASE_NAME = config_file['DEPLOY_DATABASE_NAME']
        else:
            DEPLOY_DATABASE_NAME = '_DEPLOY'
        
        #if "DEPLOY_ENV" in os.environ:
        #    DEPLOY_ENV = os.environ.get('DEPLOY_ENV')
        if "DEPLOY_ENV" in config_file and config_file['DEPLOY_ENV'] != '':
            DEPLOY_ENV = config_file['DEPLOY_ENV']
        else:
            DEPLOY_ENV = None
        
        if "VARS" in config_file and config_file['VARS'] != []:
            var_list = list(config_file['VARS'])
        else:
            var_list = []
        var_dict = {}
        for v in var_list:
            for k in v.keys():
                var_dict[k] = v[k]
        #if "DEPLOY_ROLE" in os.environ:
        #    DEPLOY_ROLE = os.environ.get('DEPLOY_ROLE')
        #elif "DEPLOY_ROLE" in config_file and config_file['DEPLOY_ROLE'] != '':
        #    DEPLOY_ROLE = config_file['DEPLOY_ROLE']
        #else:
        #    DEPLOY_ROLE = 'INSTANCEADMIN'
        DEPLOY_ROLE = self._get_param_from_env_or_config(config_file, 'DEPLOY_ROLE', 'INSTANCEADMIN')

        HANDLE_OWNERSHIP_RAW = self._get_param_from_env_or_config(config_file, 'HANDLE_OWNERSHIP', 'ERROR')

        IMPORT_DATABASES_RAW = self._get_param_from_env_or_config_list(config_file, 'IMPORT_DATABASES')
        IMPORT_DATABASES = []
        for db in IMPORT_DATABASES_RAW:
            if db.startswith(ENV_DATABASE_PREFIX):
                IMPORT_DATABASES.append(db)
            else:
                new_db = ENV_DATABASE_PREFIX + db
                IMPORT_DATABASES.append(new_db)

        if HANDLE_OWNERSHIP_RAW.upper() == 'GRANT':
            HANDLE_OWNERSHIP = HANDLE_OWNERSHIP_OPTION.GRANT
        elif HANDLE_OWNERSHIP_RAW.upper() == 'ERROR':
            HANDLE_OWNERSHIP = HANDLE_OWNERSHIP_OPTION.ERROR
        else:
            raise Exception('Invalid HANDLE_OWNERSHIP - must be in (GRANT,ERROR)')
        #grant,error,

        # Default Values
        # Database & Schema just needed for connection - all code uses db.schema.object naming convention
        database = 'SNOWFLAKE'
        schema = 'PUBLIC'
        standard_roles = ['ORGADMIN','ACCOUNTADMIN','SYSADMIN','SECURITYADMIN','USERADMIN','PUBLIC']
        excluded_databases = ['SNOWFLAKE_SAMPLE_DATA','SNOWFLAKE','SCHEMACHANGE']
        deploy_tag_list = ['DEPLOY_HASH','DEPLOY_CODE_HASH']
        #deploy_role = 'INSTANCEADMIN'

        # Store and return
        config = {}
        config['SNOWFLAKE_USERNAME'] = SNOWFLAKE_USERNAME 
        config['SNOWFLAKE_ACCOUNT'] = SNOWFLAKE_ACCOUNT
        config['SNOWFLAKE_WAREHOUSE'] = SNOWFLAKE_WAREHOUSE
        config['WAREHOUSE_SET'] = WAREHOUSE_SET
        config['SNOWFLAKE_ROLE'] = SNOWFLAKE_ROLE
        config['ROLE_SET'] = ROLE_SET
        config['SNOWFLAKE_PRIVATE_KEY_PASSWORD'] = SNOWFLAKE_PRIVATE_KEY_PASSWORD
        config['SNOWFLAKE_PRIVATE_KEY'] = SNOWFLAKE_PRIVATE_KEY
        config['database'] = database 
        config['schema'] = schema
        config['ENV_DATABASE_PREFIX'] = ENV_DATABASE_PREFIX
        config['ENV_WAREHOUSE_PREFIX'] = ENV_WAREHOUSE_PREFIX
        config['ENV_ROLE_PREFIX'] = ENV_ROLE_PREFIX
        config['ENV_PROCEDURE_PREFIX'] = ENV_PROCEDURE_PREFIX
        config['ENV_FUNCTION_PREFIX'] = ENV_FUNCTION_PREFIX
        config['OBJECT_METADATA_ONLY'] = OBJECT_METADATA_ONLY
        config['MAX_THREADS'] = MAX_THREADS
        config['DEPLOY_DATABASE_NAME'] = DEPLOY_DATABASE_NAME
        config['DEPLOY_ROLE'] = DEPLOY_ROLE
        config['DEPLOY_TAGS'] = deploy_tag_list
        config['STANDARD_ROLES'] = standard_roles
        config['HANDLE_OWNERSHIP'] = HANDLE_OWNERSHIP
        config['EXCLUDED_DATABASES'] = excluded_databases
        config['VARS'] = var_dict
        config['DEPLOY_ENV'] = DEPLOY_ENV
        config['IMPORT_DATABASES'] = IMPORT_DATABASES
        return config