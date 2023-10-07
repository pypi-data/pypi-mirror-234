from schema import Schema, Optional, SchemaError, And, Or
def validate_function(self, config:dict):

    config_schema = Schema({
        Optional("INPUT_ARGS"): Or(list, None)
        , Optional("IS_SECURE"): Or(bool, None)
        , Optional("RETURNS"): Or(str, None)
        , Optional("LANGUAGE"): Or(Or('JAVA','SQL','JAVASCRIPT','PYTHON','SCALA'), None)
        , Optional("NULL_HANDLING"): Or(Or('CALLED ON NULL INPUT','RETURNS NULL ON NULL INPUT','STRICT'), None)
        #,Optional("EXECUTE_AS"): Or(str, None)
        , Optional("OWNER"): Or(str, None)
        , Optional("COMMENT"): Or(str, None)
        , Optional("BODY"): Or(str, None)
        , Optional("TAGS"): Or(list, None)
        , Optional("GRANTS"): Or(list, None)
        #PYTHON
        , Optional("IMPORTS"): Or(list, None)
        , Optional("HANDLER"): Or(str, None)
        , Optional("RUNTIME_VERSION"): Or(str, None)
        , Optional("PACKAGES"): Or(list, None)
        , Optional("DEPLOY_ENV"): Or(list, None)
        , Optional("DEPLOY_LOCK"): Or(bool,None)
    })
    
    try:
        config_schema.validate(config)
        #print("Configuration is valid.")
    except SchemaError as se:
        raise se
