def function_create(self,function_name:str, sql_function_name:str, is_secure:bool, input_args:dict, returns:str, language:str, comment:str, body:str, imports:str, handler:str, runtime_version:str, packages:str, owner:str, tags:list, grants:list, deploy_role:str):
    # function_name = <db>.<schema>.<proc>
    cur = self._conn.cursor()
    query = ''
    try:

        if packages is None or packages == [] or packages == '':
            packages_adj = '()'
        else:
            packages_adj = "('" + "','".join(packages) + "')"
        if imports is None or imports == [] or imports == '':
            imports_adj = '()'
        else:
            imports_adj = "('" + "','".join(imports) + "')"
        func_name_adj = '"' + function_name.split('.')[0] + '"."' + function_name.split('.')[1] + '"."' + function_name.split('.')[2] + '"'
        sql_secure = 'SECURE' if is_secure else ''
        sql_returns = 'RETURNS ' + returns if returns is not None else ''
        sql_runtime_version = "RUNTIME_VERSION = " + runtime_version if runtime_version is not None else ''
        sql_packages = "PACKAGES = " + packages_adj if packages is not None and packages != [] else ''
        sql_imports = "IMPORTS = " + imports_adj if imports is not None and imports != [] else ''
        sql_handler = "HANDLER = '" + handler + "'" if handler is not None else ''
        #sql_null_handling = null_handling if null_handling is not None else '
        sql_comment = "COMMENT = '" + comment + "'" if comment is not None else ''

        query = "CREATE OR REPLACE " + sql_secure + " FUNCTION " + func_name_adj + "(" 
        cnt = 1
        for arg in input_args:
            for key in arg.keys():
                query += ', ' if cnt > 1 else ''
                query += key + ' ' + arg[key]
                cnt += 1
        #cnt = 1
        #for arg in input_args:
        #    if cnt > 1:
        #        query += ','
        #    query += arg['name'] + ' ' + arg['type']
        #    cnt += 1
        
        query += ') COPY GRANTS ' + sql_returns + ' LANGUAGE ' + language + ' ' 
        query += sql_runtime_version + ' ' + sql_packages + ' ' + sql_imports + ' ' + sql_handler + ' '
        #query += sql_null_handling + ' ' + 
        query += sql_comment + ' ' + ' as $$ ' + body + ' $$;'
        
        cur.execute(query)
        #params = [role_name]
        #if comment is not None:
        #    query += ' COMMENT = %s'
        #    params.append(comment)
        #cur.execute(query, params)
        #' identifier(%s)
        if tags is not None and tags != []:
            for t in tags:
                tag_key = list(t)[0]
                tag_val = t[tag_key]
                query = 'ALTER FUNCTION ' + sql_function_name + ' SET TAG identifier(%s) = %s;'
                params = (tag_key,tag_val)
                #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                #print(query)
                #print(params)
                #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                cur.execute(query,params)
                
        if owner is not None and owner != deploy_role: #if owner is deploy role, no need to run this:
            query = "GRANT OWNERSHIP ON FUNCTION " + sql_function_name + " TO ROLE identifier(%s) COPY CURRENT GRANTS;"
            cur.execute(query,(owner))

        if grants is not None:
            for grant in grants:
                grant_keys = grant.keys()
                grant_option = grant['GRANT_OPTION'] if 'GRANT_OPTION' in grant_keys else False
                role = ''
                permission = ''
                for key in grant_keys:
                    if key != 'GRANT_OPTION':
                        role = key
                        permission = grant[key]
                if role != '' and permission != '':
                    query = "GRANT " + permission + " ON FUNCTION " + sql_function_name + " TO ROLE " + role + ";"
                    cur.execute(query)
                else:
                    raise Exception('Invalid grants for procedure: ' + sql_function_name)
                
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()

# CREATE [ OR REPLACE ] [ TEMP | TEMPORARY ] [ SECURE ] FUNCTION [ IF NOT EXISTS ] <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
#     [ COPY GRANTS ]
#     RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
#     [ [ NOT ] NULL ]
#     LANGUAGE PYTHON
#     [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
#     [ VOLATILE | IMMUTABLE ]
#     RUNTIME_VERSION = <python_version>
#     [ COMMENT = '<string_literal>' ]
#     [ IMPORTS = ( '<stage_path_and_file_name_to_read>' [ , ... ] ) ]
#     [ PACKAGES = ( '<package_name>[==<version>]' [ , ... ] ) ]
#     HANDLER = '<function_name>'
#     AS '<function_definition>'