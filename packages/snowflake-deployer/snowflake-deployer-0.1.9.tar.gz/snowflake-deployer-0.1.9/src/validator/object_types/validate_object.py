from schema import Schema, Optional, SchemaError, And, Or
def validate_object(self, config:dict):

    #Optional("DATA_RETENTION_TIME_IN_DAYS"): And(int, lambda n: 1 <= n <= 90)
    config_schema = Schema({
        Optional("RETENTION_TIME_IN_DAYS"): And(int, lambda n: n > 0)
        , Optional('OBJECT_TYPE'): Or(str, None)
        , Optional("COMMENT"): Or(str, None)
        , Optional("OWNER"): Or(str, None)
        , Optional("CHANGE_TRACKING"): Or(bool, None)
        , Optional("TAGS"): Or(list[str], None)
        , Optional("COLUMNS"): Or(list[str], None)
        , Optional("GRANTS"): Or(list, None)
        , Optional("ROW_ACCESS_POLICY"): Or(str, None)
        , Optional("ROW_ACCESS_POLICY_COLUMNS"): Or(list, None)
        , Optional("DEPLOY_ENV"): Or(list, None)
        , Optional("DEPLOY_LOCK"): Or(bool, None)
    })
       
    try:
        config_schema.validate(config)
        #print("Configuration is valid.")
    except SchemaError as se:
        raise se