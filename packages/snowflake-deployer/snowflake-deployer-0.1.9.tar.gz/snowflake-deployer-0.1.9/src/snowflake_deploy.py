import os
import src.common.common as cmn
from src.snowflake.snowflake_client import snowflake_client as sf_client
from src.deployer.deployer import deployer
from src.deploy_logger.logger import deploy_logger
#from yaml_writer.yaml_writer import yaml_writer
#from yaml_reader.yaml_reader import yaml_reader
from src.common.common import *
import logging
import shutil
from time import sleep
import time
#from random import random
import threading
import random 
import hashlib
import re 
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, meta, StrictUndefined
from src.common.exceptions import object_type_not_supported
from src.common.enums import HANDLE_OWNERSHIP_OPTION
import traceback
from src.validator.validator import validator
from src.configurator.configurator import configurator

def role(ref_val: str) -> str:
    val = validator()
    val.validate_role_exists('snowflake', ref_val, template_path)
    
    parts = ref_val.split('__')
    if len(parts) == 1:
        #ref_id = ref_val
        jinja_ref_id = 'role__' + ref_val  # obj_type defined in loop
        processed_name = get_sf_role_name(ref_val, config['ENV_ROLE_PREFIX'])
    else:
        raise Exception('Must use ref (not role()) for reference ' + ref_val + ' in file ' + template_path)

    r={}
    if file_ext.upper() in ('YML','YAML'):
        r['path'] = template_path
        r['code_path'] = ''
    else:
        raise Exception('Invalid file type in ' + template_path)

    #r['path'] = template_path # defined in the template loop that render (and hence ref) is called from
    r['obj_name'] = obj_name  # defined in the template loop that render (and hence ref) is called from
    r['ref_id'] = ref_id # defined in the tempalte loop that rendered (and hence ref) is called from
    r['obj_type'] = obj_type  # defined in the template loop that render (and hence ref) is called from
    r['deps'] = [jinja_ref_id]
    _references.append(r)

    return processed_name

def warehouse(ref_val: str) -> str:
    val = validator()
    val.validate_warehouse_exists('snowflake', ref_val, template_path)

    parts = ref_val.split('__')
    if len(parts) == 1:
        #ref_id = ref_val
        jinja_ref_id = 'warehouse__' + ref_val  # obj_type defined in loop
        processed_name = get_sf_warehouse_name(ref_val, config['ENV_WAREHOUSE_PREFIX'])
    else:
        raise Exception('Must use ref (not warehouse()) for reference ' + ref_val + ' in file ' + template_path)
    
    r={}
    if file_ext.upper() in ('YML','YAML'):
        r['path'] = template_path
        r['code_path'] = ''
    else:
        raise Exception('Invalid file type in ' + template_path)

    #r['path'] = template_path # defined in the template loop that render (and hence ref) is called from
    r['obj_name'] = obj_name  # defined in the template loop that render (and hence ref) is called from
    r['ref_id'] = ref_id # defined in the tempalte loop that rendered (and hence ref) is called from
    r['obj_type'] = obj_type  # defined in the template loop that render (and hence ref) is called from
    r['deps'] = [jinja_ref_id]
    _references.append(r)

    return processed_name

def ref(ref_val: str)->str:
    
    val = validator()
    val.validate_ref_exists('snowflake', ref_val, template_path)
    
    parts = ref_val.split('__')
    if len(parts) == 1:
        raise Exception('Must use account level function (warehouse() or role()) for ref ' + ref_val + ' in file ' + template_path)
    elif len(parts) == 3:
        db = parts[0]
        schema = parts[1]
        object = parts[2]
        jinja_ref_id = db + '.' + schema + '.' + object
        db_env = get_sf_database_name(parts[0], config['ENV_DATABASE_PREFIX']) 
        processed_name = db_env + '.' + schema + '.' + object
    else:
        raise Exception('Invalid formatted ref value in ' + template_path)
        
    #schema_id = db + '.' + schema
    r={}
    if file_ext.upper() in ('YML','YAML'):
        r['path'] = template_path
        r['code_path'] = ''
    else:
        yml_obj_path = re.sub(file_ext+'$','yml',template_path)
        #yaml_obj_path = re.sub(file_ext+'$','yaml',template_path)
        r['path'] = yml_obj_path
        r['code_path'] = template_path
    #r['path'] = template_path # defined in the template loop that render (and hence ref) is called from
    r['obj_name'] = obj_name  # defined in the template loop that render (and hence ref) is called from
    r['ref_id'] = ref_id # defined in the tempalte loop that rendered (and hence ref) is called from
    r['obj_type'] = obj_type  # defined in the template loop that render (and hence ref) is called from
    r['deps'] = [jinja_ref_id]
    _references.append(r)

    return processed_name

def task(semaphore, tn:str, ref_id:str, data:dict, completed:list, processing:list, deploy, base_rendered_path:str, deploy_config:dict, logger, available_roles:list, val:validator):
    thread_start_time = time.time()
    #object_name:str
    try:
        # Connect with the semaphore so particular thread knows whether it is allowed to process
        # The semaphore is like a "thread pool" that controls the number of concurrent threads processing at once
        with semaphore:
            if ref_id not in processing:
                object_name = data[ref_id]['obj_name']
                processing.append(ref_id)
                name = threading.current_thread().name
                good_to_process = True
                for d in data[ref_id]['deps']:
                    if d not in completed:
                        good_to_process = False # if any deps has not been completed, then need to skip (means there's multiple next references and this thread will fire again after that reference)
                
                #if not good_to_process:
                    #print('Skipping thread ' + tn + ' as not all dependencies have finished')
                #else: 
                if good_to_process:
                    #print(f'{object_name} - Starting')
                    logger.log(object_name,'Start')
                    # DO THE WORK HERE SINCE GOOD TO PROCESS
                    #print('Processing thread ' + tn)
                    # Wait a random number of seconds (between 2-5) to demonstrate threads running vs waiting to process
                    #value = random.randint(2, 5) 
                    #sleep(value)

                    # Read in YAML config
                    #print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                    #print(data[object_name])
                    config_path = base_rendered_path + data[ref_id]['path']
                    with open(config_path, "r") as yamlfile:
                        config_raw = yaml.load(yamlfile, Loader=yaml.FullLoader) 


                    if data[ref_id]['obj_type'] in ('procedure','function','masking_policy','row_access_policy','task'):
                        code_path = base_rendered_path + data[ref_id]['code_path']
                        with open(code_path, "r") as codefile:
                            body_code = codefile.read() 

                        file_hash_code = hashlib.sha256(open(code_path,'rb').read()).hexdigest() 
                    else:
                        file_hash_code = None

                    file_hash = hashlib.sha256(open(config_path,'rb').read()).hexdigest() 
                    
                    #deploy_db_name = deploy_config['DEPLOY_DATABASE_NAME']
                    #deploy_role = deploy_config['DEPLOY_ROLE']
                    #handle_ownership = deploy_config['HANDLE_OWNERSHIP']
                    #deploy_env = deploy_config['DEPLOY_ENV']

                    object_type = data[ref_id]['obj_type']
                    # Deploy
                    if object_type == 'database':
                        val.validate_database(config_raw)
                        return_status = deploy.deploy_database(object_name, file_hash, config_raw)
                    elif object_type == 'schema':
                        val.validate_schema(config_raw)
                        return_status = deploy.deploy_schema(object_name, file_hash, config_raw)
                    elif object_type == 'tag':
                        val.validate_tag(config_raw)
                        return_status = deploy.deploy_tag(object_name, file_hash, config_raw)
                    elif object_type == 'object':
                        val.validate_object(config_raw)
                        return_status = deploy.deploy_object(object_name, file_hash, config_raw)
                    elif object_type == 'warehouse':
                        val.validate_warehouse(config_raw)
                        return_status = deploy.deploy_warehouse(object_name, file_hash, config_raw)
                    elif object_type == 'role':
                        val.validate_role(config_raw)
                        return_status = deploy.deploy_role(object_name, file_hash, config_raw)
                    elif object_type == 'procedure':
                        val.validate_procedure(config_raw)
                        return_status = deploy.deploy_procedure(object_name, file_hash, file_hash_code, config_raw, body_code)
                    elif object_type == 'function':
                        val.validate_function(config_raw)
                        return_status = deploy.deploy_function(object_name, file_hash, file_hash_code, config_raw, body_code)
                    elif object_type == 'task':
                        val.validate_task(config_raw)
                        return_status = deploy.deploy_task(object_name, file_hash, file_hash_code, config_raw, body_code)
                    elif object_type == 'masking_policy':
                        val.validate_masking_policy(config_raw)
                        return_status = deploy.deploy_masking_policy(object_name, file_hash, file_hash_code, config_raw, body_code)
                        #dummy = True
                    elif object_type == 'row_access_policy':
                        val.validate_row_access_policy(config_raw)
                        return_status = deploy.deploy_row_access_policy(object_name, file_hash, file_hash_code, config_raw, body_code)
                        #dummy = True
                    else:
                        raise object_type_not_supported(object_type)
                    #print(f'Thread {name} Mid')
                    completed.append(ref_id)

                    #filter = [d for d in data if d['num'] == next]
                    #threads = []
                    for next_ref_id in data[ref_id]['next']: 
                        tn2 = 'thread_' + next_ref_id
                        t2 = threading.Thread(target=task, name=tn2, args=(semaphore, tn2, next_ref_id, data, completed, processing, deploy, base_rendered_path, deploy_config, logger, available_roles, val))
                        #                                                   semaphore, tn, object_name, data, completed
                        t2.start()
                        
                    if return_status == 'C':
                        msg = 'created (%s seconds)' % (round(time.time() - thread_start_time,1))
                        logger.log(object_name,msg)
                        #print(f'{object_name} - created (%s seconds)' % (round(time.time() - thread_start_time,1)))
                    elif return_status == 'U':
                        msg = 'updated (%s seconds)' % (round(time.time() - thread_start_time,1))
                        logger.log(object_name,msg)
                        #print(f'{object_name} - updated (%s seconds)' % (round(time.time() - thread_start_time,1)))
                    elif return_status == 'I':
                        msg = 'ignored (%s seconds)' % (round(time.time() - thread_start_time,1))
                        logger.log(object_name, msg)
                    elif return_status == 'E':
                        msg = 'ignored - not deployable in this env (%s seconds)' % (round(time.time() - thread_start_time,1))
                        logger.log(object_name, msg)
                        #print(f'{object_name} - ignored - nothing to update (%s seconds)' % (round(time.time() - thread_start_time,1)))
                    #print(f'{object_name} - Completed in %s seconds' % (round(time.time() - thread_start_time,1)))

                processing.remove(ref_id)
    except Exception as ex:
        #print(str(ex))
        traceback_text = traceback.format_exc() # get error traceback
        msg = 'error (%s seconds) - see error log at end' % (round(time.time() - thread_start_time,1))
        logger.log(object_name,msg)
        logger.log_error(str(ex), object_name, traceback_text)
        #raise

def check_for_circular_ref(map, key, original_key):
    #print('key:' + key + '; next:'+str(map[key]['next']))
    if map[key]['next'] == []:
        is_circle = False
        #print('key:' + key + '; is_circle:'+str(is_circle))
    else:
        for n in map[key]['next']:
            if n == original_key:
                is_circle = True
            else:
                is_circle = check_for_circular_ref(map, n, original_key) # check the next of the next
                break
            #print('key:' + key + '; n:'+n+ '; is_circle:'+str(is_circle))
    return is_circle
    

def snowflake_deploy(args:dict):
    global template_path
    global file_ext
    global config
    global obj_name
    global ref_id
    global obj_type
    global _references

    #print('this is the deploy file')
    start_time = time.time()

    logging.basicConfig(level=logging.WARNING)
    logger = deploy_logger('info')

    val = validator()
    val.validate_directory_structure('snowflake')

    # Check if data directory exists
    snowflake_directory_exists = os.path.exists('snowflake/')
    if not snowflake_directory_exists:
        raise Exception('Snowflake directory does not exist.  See documentation.')

    conf = configurator(args)
    config = conf.get_config()

    ###############################################################################################################
    #                                                   Defaults
    ###############################################################################################################

    deploy_db_name = config['DEPLOY_DATABASE_NAME']
    deploy_role = config['DEPLOY_ROLE']
    handle_ownership = config['HANDLE_OWNERSHIP']
    deploy_env = config['DEPLOY_ENV']

    try:
        ###############################################################################################################
        #                                                   Connect to Snowflake
        ###############################################################################################################
        sf = sf_client(config['SNOWFLAKE_PRIVATE_KEY'], config['SNOWFLAKE_PRIVATE_KEY_PASSWORD'], config['SNOWFLAKE_ACCOUNT'], config['SNOWFLAKE_USERNAME'], config['SNOWFLAKE_WAREHOUSE'], config['database'], config['schema'] )
        #print('Connected to Snowflake')
        logging.info('Connected to Snowflake')

        # Get current role
        available_roles = []
        current_role = sf.current_role_get()
        available_roles.append(current_role)
        #ignore_roles_list = config['STANDARD_ROLES']
        #ignore_roles_list.append(current_role) # ignore out of the box roles PLUS the role that owns deployments (which can be hard coded in the files)
        
        #####################################################
        # Install Deploy DB if not exists
        
        
        deploy = deployer(sf, deploy_db_name, deploy_role, handle_ownership, available_roles, deploy_env)
        deploy.check_and_install_deployer_db()

        # Set up jinja environment and load all data files
        _references = []
        env = Environment(loader=FileSystemLoader(['snowflake']), undefined=StrictUndefined)
        # register the python function for jinja environment
        env.globals['ref'] = ref 
        env.globals['warehouse'] = warehouse
        env.globals['role'] = role

        base_rendered_path = 'metaops-deploy-rendered/'

        # Delete existing rendered
        dirpath = Path(base_rendered_path)
        if dirpath.exists() and dirpath.is_dir():
            #os.remove(base_rendered_path)
            shutil.rmtree(base_rendered_path)
        
        # Loop files and render
        for template_path in env.list_templates():
            template = env.get_template(template_path)
            #print(template_path)
            filename = os.path.splitext(os.path.basename(template_path))[0]
            folders = template_path.split('/')
            top_level = folders[0]

            if folders[0].upper() == 'ACCOUNT':
                if folders[1].upper() == 'WAREHOUSES':
                    obj_type = 'warehouse'
                    raw_name = folders[2].split('.')[0]
                    obj_name = get_sf_warehouse_name(raw_name, config['ENV_WAREHOUSE_PREFIX'])
                    ref_id = obj_type + '__' + raw_name
                    file_ext = folders[2].split('.')[1]
                    deps = []
                elif folders[1].upper() == 'ROLES':
                    obj_type = 'role'
                    raw_name = folders[2].split('.')[0]
                    obj_name = get_sf_role_name(raw_name, config['ENV_ROLE_PREFIX'])
                    ref_id = obj_type + '__' + raw_name
                    file_ext = folders[2].split('.')[1]
                    deps = []
                else:
                    raise Exception('Invalid folder structure - folder not valid:' + folders[0] + '/' + folders[1])                
            elif folders[0].upper() == 'DATA':  # data
                db_raw = folders[1]
                db_env = get_sf_database_name(db_raw, config['ENV_DATABASE_PREFIX'])
                if( len(folders) == 3 ):
                    if( folders[2].split('.')[0].upper() != 'DATABASE' ):
                        raise Exception('database ' + folders[1] + ' does not contain database.yml config')
                    obj_type = 'database'
                    obj_name = db_env
                    ref_id = db_raw
                    file_ext = folders[2].split('.')[1]
                    deps = []
                elif( len(folders) == 4):
                    if( folders[3].split('.')[0].upper() != 'SCHEMA' ):
                        raise Exception('schema ' + folders[1] + '.' + folders[2] + ' does not contain schema.yml config')
                    obj_type = 'schema'
                    raw_schema = folders[2]
                    obj_name = db_env + '.' + raw_schema
                    ref_id = db_raw + '.' + raw_schema
                    file_ext = folders[3].split('.')[1]
                    deps = [db_raw]
                elif( len(folders) == 5):
                    #if( folders[2].upper() not in ('TAGS') ):
                    if folders[3].upper() == 'TAGS':
                        obj_type = 'tag'
                        raw_name = folders[4].split('.')[0].split('__')[2]
                        obj_name = db_env + '.' + folders[2] + '.' + raw_name
                        ref_id = db_raw + '.' + folders[2] + '.' + raw_name
                        schema_id = db_raw + '.' + folders[2]
                        file_ext = folders[4].split('.')[1]
                        deps = [schema_id]
                    elif folders[3].upper() == 'OBJECTS':
                        obj_type = 'object'
                        raw_name = folders[4].split('.')[0].split('__')[2]
                        obj_name = db_env + '.' + folders[2] + '.' + raw_name
                        ref_id = db_raw + '.' + folders[2] + '.' + raw_name
                        schema_id = db_raw + '.' + folders[2]
                        file_ext = folders[4].split('.')[1]
                        deps = [schema_id]
                    elif folders[3].upper() == 'PROCEDURES':
                        obj_type = 'procedure'
                        raw_name = folders[4].split('.')[0].split('__')[2] + '__' + folders[4].split('.')[0].split('__')[3]
                        obj_name = db_env + '.' + folders[2] + '.' + raw_name
                        ref_id = db_raw + '.' + folders[2] + '.' + raw_name
                        schema_id = db_raw + '.' + folders[2]
                        file_ext = folders[4].split('.')[1]
                        deps = [schema_id]
                    elif folders[3].upper() == 'FUNCTIONS':
                        obj_type = 'function'
                        raw_name = folders[4].split('.')[0].split('__')[2] + '__' + folders[4].split('.')[0].split('__')[3]
                        obj_name = db_env + '.' + folders[2] + '.' + raw_name
                        ref_id = db_raw + '.' + folders[2] + '.' + raw_name
                        schema_id = db_raw + '.' + folders[2]
                        file_ext = folders[4].split('.')[1]
                        deps = [schema_id]
                    elif folders[3].upper() == 'TASKS':
                        obj_type = 'task'
                        raw_name = folders[4].split('.')[0].split('__')[2]
                        obj_name = db_env + '.' + folders[2] + '.' + raw_name
                        ref_id = db_raw + '.' + folders[2] + '.' + raw_name
                        schema_id = db_raw + '.' + folders[2]
                        file_ext = folders[4].split('.')[1]
                        deps = [schema_id]
                    elif folders[3].upper() == 'MASKING_POLICIES':
                        obj_type = 'masking_policy'
                        raw_name = folders[4].split('.')[0].split('__')[2]
                        obj_name = db_env + '.' + folders[2] + '.' + raw_name
                        ref_id = db_raw + '.' + folders[2] + '.' + raw_name
                        schema_id = db_raw + '.' + folders[2]
                        file_ext = folders[4].split('.')[1]
                        deps = [schema_id]
                    elif folders[3].upper() == 'ROW_ACCESS_POLICIES':
                        obj_type = 'row_access_policy'
                        raw_name = folders[4].split('.')[0].split('__')[2]
                        obj_name = db_env + '.' + folders[2] + '.' + raw_name
                        ref_id = db_raw + '.' + folders[2] + '.' + raw_name
                        schema_id = db_raw + '.' + folders[2]
                        file_ext = folders[4].split('.')[1]
                        deps = [schema_id]
                    else:
                        raise object_type_not_supported(folders[3])
                        #raise Exception('object type ' + folders[2] + ' not currently support')
                    
            else:
                raise Exception('Invalid folder structure - top folder not valid:' + folders[0])
            
            
            r = {}
            if file_ext.upper() in ('YML','YAML'):
                r['path'] = template_path
                r['code_path'] = ''
            else:
                yml_obj_path = re.sub(file_ext+'$','yml',template_path)
                #print(yml_obj_path)
                #yaml_obj_path = re.sub(file_ext+'$','yaml',template_path)
                r['path'] = yml_obj_path
                r['code_path'] = template_path
            #print('###########################################')    
            r['obj_name'] = obj_name
            r['ref_id'] = ref_id
            r['obj_type'] = obj_type
            r['deps'] = deps 
            #print(config['VARS'])
            
            _references.append(r)
            new_path = base_rendered_path + template_path
            output_file = Path(new_path)
            output_file.parent.mkdir(exist_ok=True, parents=True)
            with open(new_path, "w") as f:
                f.write(template.render(config['VARS']))


        #print('###################################')
        #print(_references)
        #print('###################################')
        #####################################################
        # Translate References into a map of downstream and upstream for each obj
        map = {}
        for r in _references:
            path = r['path']
            code_path = r['code_path']
            obj_name = r['obj_name']
            ref_id = r['ref_id']
            obj_type = r['obj_type']
            deps = r['deps']

            # Add object to path
            if ref_id not in map.keys():
                map[ref_id] = {}
                map[ref_id]['path'] = path
                map[ref_id]['code_path'] = code_path
                map[ref_id]['obj_type'] = obj_type
                map[ref_id]['obj_name'] = obj_name
                map[ref_id]['deps'] = []
                map[ref_id]['next'] = []
            else:  
                map[ref_id]['path'] = path # if added by Nexts, need to update path of object
                map[ref_id]['obj_type'] = obj_type
                map[ref_id]['obj_name'] = obj_name
                if 'code_path' in map[ref_id] and (map[ref_id]['code_path'] is None or map[ref_id]['code_path'] == ''):
                    map[ref_id]['code_path'] = code_path

            for d in deps:
                # Deps - 
                if d not in map[ref_id]['deps']:
                    map[ref_id]['deps'].append(d)

                # Nexts
                if d not in map.keys():
                    map[d] = {}
                    map[d]['deps'] = []
                    map[d]['next'] = []
                if ref_id not in map[d]['next']:
                    map[d]['next'].append(ref_id)

        #{
        #'CONTROL.GOVERNANCE.ENV': 
        #    { 'deps': ['CONTROL.GOVERNANCE'], 'next': ['CONTROL','CONTROL2']}
        #
        #, 'CONTROL.GOVERNANCE': 
        #    {'deps': ['CONTROL'], 'next': ['CONTROL.GOVERNANCE.ENV']}
        #
        #, 'CONTROL': 
        #    {'deps': ['CONTROL.GOVERNANCE.ENV'], 'next': ['CONTROL.GOVERNANCE']}
        #}


        #####################################################
        # Check for circular dependencies
        
        circular_keys = []
        for key in map.keys():
            is_circle = check_for_circular_ref(map, key, key)
            if is_circle and key not in circular_keys:
                circular_keys.append(key)
                
        if circular_keys != []:
            circular_keys_string = '[' + ', '.join(circular_keys) + ']'
            raise Exception('Circular keys found in the following objects: ' + circular_keys_string)

        # # flatten next
        # flatten = []
        # for key in map.keys():
        #     deps = map[key]['deps']
        #     for n in map[key]['next']:
        #         flatten.append({"ref_id": key, "deps": deps, "next": n})
        
        # circular_keys = []
        # for f in flatten:
        #     key = f['ref_id']
        #     continue = True
        #     while continue:
        #         next = map[key]['next']
        #         if next == []:
        #             continue = False
        #         for 




        #####################################################
        # Get starting objects (ones with no dependencies)
        #print('&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        #print(map)
        #print('&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        map_start = []
        for key in map.keys():
            if map[key]['deps'] == []:
                map_start.append(key)
        #print(map_start)

        # Semaphore sets the number of concurrent threads running at any one time
        semaphore = threading.Semaphore(config['MAX_THREADS'])

        completed = []  # need to track the objects already processed to know when downstream (next) processes can begin based on all dependencies being "complete"
        processing = []  # need to track currently executing processes for race conditions when a process kicks off (from a next of another object) that is already processing to avoid duplicate execution
        # Create a bunch of threads and add to array
        # NOTE: These threads have not actually began to execute yet
        threads = []
        #for i in range(10):
        for ref_id in map_start:
            tn = 'thread_' + ref_id
            t = threading.Thread(target=task, name=tn, args=(semaphore, tn, ref_id, map, completed, processing, deploy, base_rendered_path, config, logger, available_roles, val))
            threads.append(t)

        # Kick off all threads to begin execution
        for t in threads:
            t.start()

        # if threads are not joined, the script will continue to run while the threads are also running.
        # Joining the threads means we will wait here until all the threads are done processing before continuing
        for t in threads:
            t.join()

        while len(threading.enumerate()) > 1:
            #print('Active processes: ' + str(len(threading.enumerate())))
            sleep(1)

        # Once all threads are complete
        
        logger.log('','all deployments have completed')
        msg = "--- Executed in %s seconds ---" % (round(time.time() - start_time,1))
        logger.log('',msg)

    except Exception as ex:
        #print(str(ex))
        traceback_text = traceback.format_exc() # get error traceback
        msg = 'error - see error log at end'
        logger.log('',msg)
        logger.log_error(str(ex), 'script', traceback_text)

    finally:
        if 'sf' in locals() or 'sf' in globals():
            del sf
        
        error_count = logger.get_error_count()
        if error_count > 0:
            logger.show_all_errors()
            raise Exception("Errors occured - see log for details")
        else:
            logger.log('','No errors! Nice job!')