from snowflake.connector import DictCursor

def functions_get(self,database_name:str, schema_name:str)->dict:
    cur = self._conn.cursor(DictCursor)
    
    schema_with_db = database_name + '.' + schema_name
    info_sec_name = database_name + '.INFORMATION_SCHEMA.FUNCTIONS'
    
    query = '''
        SELECT 
            FUNCTION_NAME, FUNCTION_OWNER, ARGUMENT_SIGNATURE, IS_SECURE, DATA_TYPE, FUNCTION_LANGUAGE, COMMENT
            , RUNTIME_VERSION, IMPORTS, PACKAGES, HANDLER
            , FUNCTION_DEFINITION 
        FROM identifier(%s) WHERE FUNCTION_SCHEMA = %s;
    '''
    data=[]
    try:
        cur.execute(query,(info_sec_name,schema_name))
        for rec in cur:
            nw = {}

            nw['FUNCTION_NAME'] = rec['FUNCTION_NAME']
            #nw['FUNCTION_NAME_SANS_ENV'] = remove_prefix(rec['FUNCTION_NAME'],env_function_prefix)
            nw['COMMENT'] = rec['COMMENT']
            nw['OWNER'] = rec['FUNCTION_OWNER']
            nw['IS_SECURE'] = False if rec['IS_SECURE'].upper() == 'NO' else True
            nw['RETURNS'] = rec['DATA_TYPE']
            nw['LANGUAGE'] = rec['FUNCTION_LANGUAGE']
            nw['BODY'] = rec['FUNCTION_DEFINITION']
            if rec['FUNCTION_LANGUAGE'] == 'PYTHON':
                nw['RUNTIME_VERSION'] = rec['RUNTIME_VERSION']
                nw['HANDLER'] = rec['HANDLER']
                nw['IMPORTS'] = json.loads(rec['IMPORTS'].replace("'",'"')) 
                nw['PACKAGES'] = json.loads(rec['PACKAGES'].replace("'",'"')) 
                
            ARGUMENT_SIGNATURE = rec['ARGUMENT_SIGNATURE']
            ARGUMENT_SIGNATURE = ARGUMENT_SIGNATURE[1:] # remove first "("
            ARGUMENT_SIGNATURE = ARGUMENT_SIGNATURE[:-1] # remove first ")"
            ARGUMENT_SIGNATURE_TO_MATCH = '('
            cnt = 1
            INPUT_ARGS = []
            for a in ARGUMENT_SIGNATURE.split(', '):
                if a != '':
                    if cnt > 1:
                        ARGUMENT_SIGNATURE_TO_MATCH += ', '
                    ARGUMENT_SIGNATURE_TO_MATCH += a.split(' ')[1] # extract the data type
                    f = {}
                    key = a.split(' ')[0]
                    f[key] = a.split(' ')[1]
                    #f['name'] = a.split(' ')[0]
                    #f['type'] = a.split(' ')[1]
                    INPUT_ARGS.append(f)
                cnt += 1
            ARGUMENT_SIGNATURE_TO_MATCH += ')' 
            nw['INPUT_ARGS'] = INPUT_ARGS
            
            # Save the signature types to append to filename
            nw['FUNCTION_SIGNATURE_TYPES'] = ARGUMENT_SIGNATURE_TO_MATCH.replace(' ','') 
            
            # for creating the correct function name for the tags query
            nw['ARGUMENT_SIGNATURE_TO_MATCH'] = rec['FUNCTION_NAME'] + ARGUMENT_SIGNATURE_TO_MATCH
            
            data.append(nw)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
        
    return data