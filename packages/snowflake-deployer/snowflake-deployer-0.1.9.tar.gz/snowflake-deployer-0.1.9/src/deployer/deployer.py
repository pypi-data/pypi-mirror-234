import logging
from src.common.enums import HANDLE_OWNERSHIP_OPTION

# Abstract to handle the deployment from source code to Snowflake for each object type

class deployer:
    def __init__(self,sf, deploy_db_name:str, deploy_role:str, handle_ownership, available_roles:list, deploy_env:str):
        self._sf = sf
        self._deploy_db_name = deploy_db_name
        self._deploy_role = deploy_role
        self._ownership_handling = handle_ownership
        self._available_roles = available_roles
        self._deploy_env = deploy_env
    
    def check_and_install_deployer_db(self):
        is_installed = self._sf.deploy_db_check_installed(self._deploy_db_name)
        if not is_installed:
            self._sf.deploy_db_install(self._deploy_db_name)
            logging.info('Deploy DB Created')
    
    def _handle_ownership(self, object_owner: str, object_type: str, object_name: str):
        if self._ownership_handling == HANDLE_OWNERSHIP_OPTION.GRANT:
            self._sf.role_handle_ownership(object_owner, object_type, object_name, self._deploy_role, self._available_roles)

    from .object_types.deploy_database import deploy_database
    from .object_types.deploy_function import deploy_function
    from .object_types.deploy_masking_policy import deploy_masking_policy
    from .object_types.deploy_object import deploy_object
    from .object_types.deploy_procedure import deploy_procedure
    from .object_types.deploy_role import deploy_role
    from .object_types.deploy_row_access_policy import deploy_row_access_policy
    from .object_types.deploy_schema import deploy_schema
    from .object_types.deploy_tag import deploy_tag
    from .object_types.deploy_task import deploy_task
    from .object_types.deploy_warehouse import deploy_warehouse