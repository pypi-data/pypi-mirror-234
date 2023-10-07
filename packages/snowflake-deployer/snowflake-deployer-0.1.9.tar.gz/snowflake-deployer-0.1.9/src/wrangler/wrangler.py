import logging
from src.common.enums import HANDLE_OWNERSHIP_OPTION

# Abstract to handle the reverse engineering from Snowflake to source code for each object type

class wrangler:
    def __init__(self,sf):
        self._sf = sf
    
    def create_jinja_ref(self, database_name:str, schema_name:str, object_name:str):
        #return "!!{{!!ref(!!|!!" + database_name + "__" + schema_name + "__" + object_name + "!!|!!)!!}}!!"
        return "<~<~ref(!!|!!" + database_name + "__" + schema_name + "__" + object_name + "!!|!!)~>~>"
    
    def create_jinja_ref_instance(self, object_name:str):
        #return "!!{{!!ref(!!|!!" + object_name + "!!|!!)!!}}!!"
        return "<~<~ref(!!|!!" + object_name + "!!|!!)~>~>"
    
    def create_jinja_role_instance(self, object_name:str):
        #return "!!{{!!role(!!|!!" + object_name + "!!|!!)!!}}!!"
        return "<~<~role(!!|!!" + object_name + "!!|!!)~>~>"
    
    def create_jinja_warehouse_instance(self, object_name:str):
        #return "!!{{!!warhouse(!!|!!" + object_name + "!!|!!)!!}}!!"
        return "<~<~warhouse(!!|!!" + object_name + "!!|!!)~>~>"
    

    def _handle_ownership(self, handle_ownership:HANDLE_OWNERSHIP_OPTION, object_owner:str, object_type:str, object_name:str, current_role:str, available_roles:list)->str:
        return_role = object_owner
        if handle_ownership == HANDLE_OWNERSHIP_OPTION.GRANT:
            if object_owner not in available_roles:
                role_available = self._sf.role_check_assigned(object_owner)
                if not role_available:
                    role_granted = self._sf.role_grant_to_role(object_owner, current_role)
                    if not role_granted: 
                        self._sf.ownership_transfer(object_type,object_name,current_role)
                        return_role = current_role
        return return_role 

    def _combine_grants(self,grants):
        grants_combined = []
        for grant_dict in grants:
            key = list(grant_dict.keys())[0]
            found = False
            #for grants_new in grants_combined:
            for i in range(len(grants_combined)):
                if key in grants_combined[i].keys():
                    new_val = grants_combined[i][key] + ', ' + grant_dict[key]
                    grants_combined[i] = {key:new_val}
                    found = True
            if not found:
                grants_combined.append({key: grant_dict[key]})
        return grants_combined

    from .object_types.wrangle_column import wrangle_column
    from .object_types.wrangle_database import wrangle_database
    from .object_types.wrangle_function import wrangle_function
    from .object_types.wrangle_masking_policy import wrangle_masking_policy
    from .object_types.wrangle_object import wrangle_object
    from .object_types.wrangle_procedure import wrangle_procedure
    from .object_types.wrangle_role import wrangle_role
    from .object_types.wrangle_row_access_policy import wrangle_row_access_policy
    from .object_types.wrangle_schema import wrangle_schema
    from .object_types.wrangle_tag import wrangle_tag
    from .object_types.wrangle_task import wrangle_task
    from .object_types.wrangle_warehouse import wrangle_warehouse