from schema import Schema, Optional, SchemaError, And, Or
def validate_database(self, config:dict):

    config_schema = Schema({
        Optional("DATA_RETENTION_TIME_IN_DAYS"): And(int, lambda n: 1 <= n <= 90)
        , Optional("COMMENT"): Or(str, None)
        , Optional("OWNER"): Or(str, None)
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