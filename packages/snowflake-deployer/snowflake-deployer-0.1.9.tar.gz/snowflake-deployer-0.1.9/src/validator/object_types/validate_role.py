from schema import Schema, Optional, SchemaError, And, Or
def validate_role(self, config:dict):

    config_schema = Schema({
        Optional("COMMENT"): Or(str, None)
        , Optional("OWNER"): Or(str, None)
        , Optional("PARENT_ROLES"): Or(list, None)
        , Optional("TAGS"): Or(list, None)
        , Optional("DEPLOY_ENV"): Or(list, None)
        , Optional("DEPLOY_LOCK"): Or(bool,None)
    })
       
    try:
        config_schema.validate(config)
        #print("Configuration is valid.")
    except SchemaError as se:
        raise se