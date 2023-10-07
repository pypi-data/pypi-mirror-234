from schema import Schema, Optional, SchemaError, And, Or
def validate_task(self, config:dict):

    config_schema = Schema({
        Optional("WAREHOUSE"): Or(str, None)
        , Optional("SCHEDULE"): Or(str, None)
        , Optional("ALLOW_OVERLAPPING_EXECUTION"): Or(bool, None)
        , Optional("PREDECESSORS"): Or(list, None)
        , Optional("ERROR_INTEGRATION"): Or(str, None)
        , Optional("OWNER"): Or(str, None)
        , Optional("COMMENT"): Or(str, None)
        , Optional("ENABLED"): Or(bool, None)
        , Optional("CONDITION"): Or(str, None)
        , Optional("USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE"): Or(Or('XSMALL','SMALL','MEDIUM','LARGE','XLARGE','XXLARGE','XXXLARGE','X4LARGE','X5LARGE','X6LARGE'), None)
        , Optional("USER_TASK_TIMEOUT_MS"): Or(str, None)
        , Optional("SUSPEND_TASK_AFTER_NUM_FAILURES"): Or(str, None)
        , Optional("DEFINITION"): Or(str, None)
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
