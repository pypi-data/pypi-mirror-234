from snowflake.connector import DictCursor
import json

def procedures_get(self,database_name:str, schema_name:str)->dict:
    cur = self._conn.cursor(DictCursor)
    cur_show = self._conn.cursor(DictCursor)
    cur_desc = self._conn.cursor(DictCursor)

    schema_with_db = database_name + '.' + schema_name
    info_sec_name = database_name + '.INFORMATION_SCHEMA.PROCEDURES'
    
    query = "SELECT PROCEDURE_NAME, PROCEDURE_OWNER, ARGUMENT_SIGNATURE, COMMENT FROM identifier(%s) WHERE PROCEDURE_SCHEMA = %s;"
    data=[]
    try:
        cur.execute(query,(info_sec_name,schema_name))
        for rec in cur:
            nw = {}
            nw['PROCEDURE_NAME'] = rec['PROCEDURE_NAME']
            nw['COMMENT'] = rec['COMMENT']
            nw['OWNER'] = rec['PROCEDURE_OWNER']

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
            nw['PROCEDURE_SIGNATURE_TYPES'] = ARGUMENT_SIGNATURE_TO_MATCH.replace(' ','') 
            
            # Add the procedure name for matching
            ARGUMENT_SIGNATURE_TO_MATCH = rec['PROCEDURE_NAME'] + ARGUMENT_SIGNATURE_TO_MATCH
            nw['ARGUMENT_SIGNATURE_TO_MATCH'] = ARGUMENT_SIGNATURE_TO_MATCH
            
            # SHOW is the only thing that shows whether it's a secure procedure
            query_show = "SHOW PROCEDURES like '" + rec['PROCEDURE_NAME'] + "' IN SCHEMA identifier(%s);"
            cur_show.execute(query_show,(schema_with_db))
            for rec_show in cur_show:
                SHOW_MATCH = rec_show['arguments'].split('RETURN')[0].strip()
                if SHOW_MATCH == ARGUMENT_SIGNATURE_TO_MATCH:
                    nw['IS_SECURE'] = rec_show['is_secure']
            
            # DESC shows all the key/value pairs of the config specific to the language
            query_desc = 'DESC PROCEDURE ' + schema_with_db + '.' + ARGUMENT_SIGNATURE_TO_MATCH + ';'
            cur_desc.execute(query_desc)
            for rec_desc in cur_desc:
                key = rec_desc['property'].upper()
                val_string = rec_desc['value']
                if key in ['PACKAGES', 'IMPORTS']:
                    val = json.loads(val_string.replace("'",'"'))
                else:
                    val = val_string
                nw[key] = val
                
            data.append(nw)
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
        cur_show.close()
        cur_desc.close()
    return data