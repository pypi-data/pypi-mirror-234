def deploy_db_install(self,deploy_db_name: str)->bool:
    cur = self._conn.cursor()
    query = ''
    try:
        # Permissions
        #query = "GRANT CREATE DATABASE ON ACCOUNT TO ROLE INSTANCEADMIN;"
        #cur.execute(query)
        #query = "GRANT CREATE USER ON ACCOUNT TO ROLE INSTANCEADMIN;"
        #cur.execute(query)
        #query = "GRANT CREATE ROLE ON ACCOUNT TO ROLE INSTANCEADMIN;"
        #cur.execute(query)
        #query = "GRANT CREATE WAREHOUSE ON ACCOUNT TO ROLE INSTANCEADMIN;"
        #cur.execute(query)

        query = '''
            CREATE DATABASE IF NOT EXISTS identifier(%s) COMMENT = 'Database to manage deployments using MetaOps Deployer'
        '''
        cur.execute(query, (deploy_db_name))

        schema_full_name = deploy_db_name + '.TAG';
        query = '''
            CREATE SCHEMA IF NOT EXISTS identifier(%s) COMMENT = 'Schema to store tags for MetaOps Deployer'
        '''
        cur.execute(query, (schema_full_name))

        tag_full_name = deploy_db_name + '.TAG.DEPLOY_HASH';
        query = '''
            CREATE TAG IF NOT EXISTS identifier(%s) COMMENT = 'Tag to store deployment hash for MetaOps Deployer'
        '''
        cur.execute(query, (tag_full_name))

        tag_full_name = deploy_db_name + '.TAG.DEPLOY_CODE_HASH';
        query = '''
            CREATE TAG IF NOT EXISTS identifier(%s) COMMENT = 'Tag to store deployment hash for code files for MetaOps Deployer'
        '''
        cur.execute(query, (tag_full_name))

        
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()