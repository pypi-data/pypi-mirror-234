from pathlib import Path
import yaml
import os
class yaml_reader:

    def read_database_yaml(self,db_name_no_env: str)->dict:
        config_path = 'data/' + db_name_no_env + '/database.yml'
        with open(config_path, "r") as yamlfile:
            config_raw = yaml.load(yamlfile, Loader=yaml.FullLoader)
        return config_raw
    