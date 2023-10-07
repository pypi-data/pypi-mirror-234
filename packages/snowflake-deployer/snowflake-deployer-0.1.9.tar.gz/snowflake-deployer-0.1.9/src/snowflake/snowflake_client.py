import snowflake.connector
from snowflake.connector.errors import DatabaseError, ProgrammingError
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
#from snowflake.connector import DictCursor
import os

class snowflake_client:
    def __init__(self,private_key: str, private_key_password: str, host: str
                      , username: str, warehouse: str
                      #, role: str
                      , database: str, schema: str):
        #self.field1 = 0
        #self.field2 = whatever
        p_key= serialization.load_pem_private_key(
            private_key.encode(),
            password=private_key_password.encode(),
            backend=default_backend()
        )

        pkb = p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())

        try:
            self._conn = snowflake.connector.connect(
                user=username,
                account=host,
                private_key=pkb,
                warehouse=warehouse,
                #role=role,
                database=database,
                schema=schema
                )
            self._connected = True

        except DatabaseError as db_ex:
            self._conn = None 
            self._connected = False 
            raise
        except Exception as ex:
            self._conn = None 
            self._connected = False 
            raise
    
    def create_sql_error_msg(self, msg:str, query:str )->str:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        return msg

    def __del__(self):
        if self._connected:
            self._conn.close()
    
    from .functions.columns_get import columns_get
    from .functions.column_alter import column_alter
    from .functions.database_create import database_create
    from .functions.database_alter import database_alter
    from .functions.database_check_exists import database_check_exists
    from .functions.databases_get import databases_get
    from .functions.schema_create import schema_create
    from .functions.schema_alter import schema_alter
    from .functions.schema_check_exists import schema_check_exists
    from .functions.schemas_get import schemas_get
    from .functions.current_role_get import current_role_get
    from .functions.deploy_code_hash_apply import deploy_code_hash_apply
    from .functions.deploy_code_hash_get import deploy_code_hash_get
    from .functions.deploy_db_check_installed import deploy_db_check_installed
    from .functions.deploy_db_install import deploy_db_install
    from .functions.deploy_hash_get import deploy_hash_get
    from .functions.deploy_hash_apply import deploy_hash_apply
    from .functions.functions_get import functions_get
    from .functions.function_create import function_create
    from .functions.function_check_exists import function_check_exists
    from .functions.function_get import function_get
    from .functions.grants_get import grants_get
    from .functions.masking_policies_get import masking_policies_get
    from .functions.masking_policy_alter import masking_policy_alter
    from .functions.masking_policy_create import masking_policy_create
    from .functions.masking_policy_check_exists import masking_policy_check_exists
    from .functions.objects_get import objects_get
    from .functions.object_alter import object_alter
    from .functions.object_check_exists import object_check_exists
    from .functions.ownership_transfer import ownership_transfer
    from .functions.procedures_get import procedures_get
    from .functions.procedure_get import procedure_get
    from .functions.procedure_check_exists import procedure_check_exists
    from .functions.procedure_create import procedure_create
    from .functions.role_check_assigned import role_check_assigned
    from .functions.role_handle_ownership import role_handle_ownership
    from .functions.roles_get import roles_get
    from .functions.role_check_exists import role_check_exists
    from .functions.role_alter import role_alter
    from .functions.role_create import role_create
    from .functions.role_check_assigned import role_check_assigned
    from .functions.role_grant_to_role import role_grant_to_role
    from .functions.role_parent_grants_get import role_parent_grants_get
    from .functions.row_access_policies_get import row_access_policies_get
    from .functions.row_access_policy_alter import row_access_policy_alter
    from .functions.row_access_policy_create import row_access_policy_create
    from .functions.row_access_policy_check_exists import row_access_policy_check_exists
    from .functions.tag_check_exists import tag_check_exists
    from .functions.tag_alter import tag_alter
    from .functions.tag_create import tag_create
    from .functions.tag_masking_policy_reference import tag_masking_policy_reference
    from .functions.tag_references_get import tag_references_get
    from .functions.tags_get import tags_get
    from .functions.tasks_get import tasks_get
    from .functions.task_check_exist import task_check_exists
    from .functions.task_create import task_create
    from .functions.task_alter import task_alter
    from .functions.warehouses_get import warehouses_get
    from .functions.warehouse_check_exists import warehouse_check_exists
    from .functions.warehouse_alter import warehouse_alter
    from .functions.warehouse_create import warehouse_create

  