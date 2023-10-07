from schema import Schema, Optional, SchemaError, And, Or
def validate_row_access_policy(self, config:dict):

    config_schema = Schema({
        Optional("SIGNATURE"): Or(list, None)
        , Optional("RETURN_TYPE"): Or(str, None)
        , Optional("EXEMPT_OTHER_POLICIES"): Or(bool, None)
        , Optional("OWNER"): Or(str, None)
        , Optional("COMMENT"): Or(str, None)
        , Optional("BODY"): Or(str, None)
        , Optional("TAGS"): Or(list, None)
        , Optional("GRANTS"): Or(list, None)
        , Optional("DEPLOY_ENV"): Or(list, None)
        , Optional("DEPLOY_LOCK"): Or(bool,None)
    })

    try:
        config_schema.validate(config)
        #print("Configuration is valid.")
    except SchemaError as se:
        raise se
