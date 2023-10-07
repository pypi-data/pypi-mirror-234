from schema import Schema, Optional, SchemaError, And, Or
def validate_warehouse(self, config:dict):

    config_schema = Schema({
        Optional("WAREHOUSE_TYPE"): Or('STANDARD','SNOWPARK-OPTIMIZED')
        , Optional("WAREHOUSE_SIZE"): Or('XSMALL','SMALL','MEDIUM','LARGE','XLARGE','XXLARGE','XXXLARGE','X4LARGE','X5LARGE','X6LARGE')
        , Optional("MIN_CLUSTER_COUNT"): And(int, lambda n: 1 <= n <= 10)
        , Optional("MAX_CLUSTER_COUNT"): And(int, lambda n: 1 <= n <= 10)
        , Optional("SCALING_POLICY"): Or('STANDARD','ECONOMY')
        , Optional("AUTO_SUSPEND"): And(int, lambda n: n > 0)
        , Optional("OWNER"): Or(str, None)
        , Optional("COMMENT"): Or(str, None)
        , Optional("QUERY_ACCELERATION_MAX_SCALE_FACTOR"): And(int, lambda n: n > 0)
        , Optional("TAGS"): Or(list, None)
        , Optional("GRANTS"): Or(list, None)
        , Optional("AUTO_RESUME"): Or(bool, None)
        , Optional("ENABLE_QUERY_ACCELERATION"): Or(bool, None)
        , Optional("DEPLOY_ENV"): Or(list, None)
        , Optional("DEPLOY_LOCK"): Or(bool,None)
    })
       
    try:
        config_schema.validate(config)
        #print("Configuration is valid.")
    except SchemaError as se:
        raise se
