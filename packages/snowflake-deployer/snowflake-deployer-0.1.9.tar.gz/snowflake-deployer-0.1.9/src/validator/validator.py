import os
class validator:
    def __init__(self):
        #self._sf = sf
        self._tst = 'tst'
    
    from .object_types.validate_database import validate_database
    from .object_types.validate_function import validate_function
    from .object_types.validate_masking_policy import validate_masking_policy
    from .object_types.validate_object import validate_object
    from .object_types.validate_procedure import validate_procedure
    from .object_types.validate_role import validate_role
    from .object_types.validate_row_access_policy import validate_row_access_policy
    from .object_types.validate_schema import validate_schema 
    from .object_types.validate_tag import validate_tag
    from .object_types.validate_task import validate_task
    from .object_types.validate_warehouse import validate_warehouse 
    
    def validate_role_exists(self, base_dir: str, ref_filename: str, ref_source_file: str):
        base_dir_adj = base_dir + '/account/roles'
        self._validate_file_exists(base_dir_adj, ref_filename, ref_source_file)

    def validate_warehouse_exists(self, base_dir: str, ref_filename: str, ref_source_file: str):
        base_dir_adj = base_dir + '/account/warehouses'
        self._validate_file_exists(base_dir_adj, ref_filename, ref_source_file)

    def validate_ref_exists(self, base_dir:str, ref_filename:str, ref_source_file:str):
        base_dir_adj = base_dir + '/data'
        self._validate_file_exists(base_dir_adj, ref_filename, ref_source_file)

    def _validate_file_exists(self, base_dir, ref_filename: str, ref_source_file: str):
        found = False
        for subdir, dirs, files in os.walk(base_dir):
            #os.path.basename(path).split('/')[-1]
            for file in files:
                file_name = file.split('.')[0]
                file_ext = file.split('.')[1]
                if file_ext.upper() in ('YML','YAML') and file_name == ref_filename:
                    found = True
                    break

        if not found:
            raise Exception('Invalid ref "' + ref_filename + '" in file ' + ref_source_file)
    


    def validate_directory_structure(self, base_dir:str):
        #rootdir = 'C:/Users/sid/Desktop/test'
        for subdir, dirs, files in os.walk(base_dir):
            subdir_raw = repr(subdir).replace("'","")
            if '\\' in subdir_raw:
                subdir_arr = subdir_raw.split('\\')
                level = len(subdir_arr) # windows
                
            else:
                subdir_arr = subdir_raw.split('/')
                level = len(subdir_arr)
            #print(subdir_raw)
            #print(subdir_arr)
            #print(level)
            #print(subdir)
            #print(dirs)
            #print(files)
            #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            
            base_ex_msg = 'Directory Valudation Error - '
            doc_msg = 'See documentation for file structure.'
            if level == 1:
                for d in dirs:
                    if d.upper() not in ('ACCOUNT','DATA'):
                        raise Exception(base_ex_msg + 'Directories in ' + subdir_raw + ' must be in [account,data].  Found directory: ' + d)
                if len(files) != 0:
                    raise Exception(base_ex_msg + 'No files can exists in directory: ' + subdir_raw + '. ' + doc_msg)
            else:
                top_folder_name = subdir_arr[1]
                if top_folder_name.upper() == 'DATA':
                    if level == 2:
                        if len(files) != 0:
                            raise Exception(base_ex_msg + 'No files can exists in directory: ' + subdir_raw + '. ' + doc_msg)
                    
                    elif level == 3:
                        # database level
                        if len(files) != 1:
                            raise Exception(base_ex_msg + 'Database directory ' + subdir_raw + ' must contain a database.yml file. ' + doc_msg)
                                
                        for f in files:
                            file_name = f.split('.')[0].upper()
                            file_ext = f.split('.')[1].upper()
                            if file_name != 'DATABASE' or file_ext not in ('YAML','YML'):
                                raise Exception(base_ex_msg + 'Database directory ' + subdir_raw + ' must contain a database.yml file. ' + doc_msg)

                    elif level == 4:
                        # schema level 
                        if len(files) != 1:
                            raise Exception(base_ex_msg + 'Database directory ' + subdir_raw + ' must contain a schema.yml file. ' + doc_msg)
                                
                        for f in files:
                            file_name = f.split('.')[0].upper()
                            file_ext = f.split('.')[1].upper()
                            if file_name != 'SCHEMA' or file_ext not in ('YAML','YML'):
                                raise Exception(base_ex_msg + 'Database directory ' + subdir_raw + ' must contain a schema.yml file. ' + doc_msg)

                        for d in dirs:
                            if d.upper() not in ('OBJECTS','TAGS','PROCEDURES','FUNCTIONS','TASKS','MASKING_POLICIES','ROW_ACCESS_POLICIES'):
                                raise Exception(base_ex_msg + 'Directories in ' + subdir_raw + ' must be in [objects,tags,procedures,functions,tasks,masking_policies,row_access_policies].  Found directory: ' + d)
                
                    elif level == 5:
                        if len(dirs) != 0:
                            raise Exception(base_ex_msg + 'No directires should exists in ' + subdir_raw + '. ' + doc_msg)

                        for f in files:
                            file_ext = f.split('.')[1].upper()
                            folder_type = subdir_arr[4].upper()
                            #print(subdir_arr)
                            if folder_type not in ('FUNCTIONS','PROCEDURES','TASKS','MASKING_POLICIES','ROW_ACCESS_POLICIES') and file_ext not in ('YAML','YML'):
                                raise Exception(base_ex_msg + 'Directory ' + subdir_raw + ' should ony contain yaml files. ' + doc_msg)
                            if folder_type in ('FUNCTIONS','PROCEDURES','TASKS','MASKING_POLICIES','ROW_ACCESS_POLICIES') and file_ext not in ('YAML','YML','JS','PY','JAVA','SCALA','SQL'):
                                raise Exception(base_ex_msg + 'Directory ' + subdir_raw + ' should ony contain yaml files. ' + doc_msg)
                    
                elif top_folder_name.upper() == 'ACCOUNT':
                    if level == 2:
                        for d in dirs:
                            if d.upper() not in ('ROLES','WAREHOUSES'):
                                raise Exception(base_ex_msg + 'Directories in ' + subdir_raw + ' must be in [roles,warehouses].  Found directory: ' + d)
                        if len(files) != 0:
                            raise Exception(base_ex_msg + 'No files can exists in directory: ' + subdir_raw + '. ' + doc_msg)
                    elif level == 3:
                        # account/roles & account/warehouses
                        if len(dirs) != 0:
                            # roles & warehouse folders should only contain yaml files
                            raise Exception(base_ex_msg + 'No directories can exists in directory: ' + subdir_raw + '. ' + doc_msg)
                        for f in files:
                            # roles & warehouse folders should only contain yaml files
                            ext = f.split('.')[1].upper()
                            if ext not in ('YML','YAML'):
                                raise Exception(base_ex_msg + 'Only yaml files should exists in : ' + subdir_raw + '. ' + doc_msg)
        print('Directory structure valid!')                
                #for file in files:
                #    print(os.path.join(subdir, file))