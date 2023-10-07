from schema import Schema, Optional, SchemaError, And, Or
def validate_tag(self, config:dict):

    config_schema = Schema({
        Optional("COMMENT"): Or(str, None)
        , Optional("OWNER"): Or(str, None)
        , Optional("ALLOWED_VALUES"): Or(list[str], None)
        , Optional("MASKING_POLICIES"): Or(list[str], None)
        , Optional("DEPLOY_ENV"): Or(list[str], None)
        , Optional("DEPLOY_LOCK"): Or(bool,None)
    })
       
    try:
        config_schema.validate(config)
        #print("Configuration is valid.")
    except SchemaError as se:
        raise se