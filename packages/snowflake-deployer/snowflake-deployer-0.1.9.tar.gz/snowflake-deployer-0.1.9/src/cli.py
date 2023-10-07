import src
import sys
import argparse
from src.snowflake_deploy import snowflake_deploy
from src.snowflake_import import snowflake_import
from src.snowflake_generate_rsa_keys import snowflake_generate_rsa_keys

def cli():
    parser = argparse.ArgumentParser(prog = 'snowflake-deployer', description = 'Deploy state based yaml config to Snowflake. Full readme at https://github.com/metaopslabs/snowflake_deployer', formatter_class = argparse.RawTextHelpFormatter)
    subcommands = parser.add_subparsers(dest='subcommand')
    
    # Command Line Parameters
    #parser.add_argument("-u", "--SNOWFLAKE_USERNAME", default='', help="Snowflake Username")
    #parser.add_argument("-a", "--SNOWFLAKE_ACCOUNT", default='', help="Snowflake Account (<identifier>.<region>.<name>)")
    #parser.add_argument("-w", "--SNOWFLAKE_WAREHOUSE", default='', help="Snowflake Warehouse for deployments")
    #parser.add_argument("-r", "--SNOWFLAKE_ROLE", default='', help="Snowflake Role for username connection")
    #parser.add_argument("-c", "--CONFIG_PATH", default='', help="File path to the deployment config file (can vary by environment)")

    # Add sub commands
    parser_deploy = subcommands.add_parser("deploy", description="Deployment to Snowflake")
    parser_import = subcommands.add_parser('import', description="Reverse Engineer from Snowflake to YAML config.")
    parser_keys = subcommands.add_parser('keys', description="Generate RSA public/private keys used for authentication")
    
    
    # DEPLOY command line params
    parser_deploy.add_argument("-u", "--SNOWFLAKE_USERNAME", default='', help="Snowflake Username")
    parser_deploy.add_argument("-a", "--SNOWFLAKE_ACCOUNT", default='', help="Snowflake Account (<identifier>.<region>.<name>)")
    parser_deploy.add_argument("-w", "--SNOWFLAKE_WAREHOUSE", default='', help="Snowflake Warehouse for deployments")
    parser_deploy.add_argument("-r", "--SNOWFLAKE_ROLE", default='', help="Snowflake Role for username connection")
    parser_deploy.add_argument("-c", "--CONFIG_PATH", default='', help="File path to the deployment config file (can vary by environment)")
    
    # IMPORT command line params
    parser_import.add_argument("-u", "--SNOWFLAKE_USERNAME", default='', help="Snowflake Username")
    parser_import.add_argument("-a", "--SNOWFLAKE_ACCOUNT", default='', help="Snowflake Account (<identifier>.<region>.<name>)")
    parser_import.add_argument("-w", "--SNOWFLAKE_WAREHOUSE", default='', help="Snowflake Warehouse for deployments")
    parser_import.add_argument("-r", "--SNOWFLAKE_ROLE", default='', help="Snowflake Role for username connection")
    parser_import.add_argument("-c", "--CONFIG_PATH", default='', help="File path to the deployment config file (can vary by environment)")
    
    # KEY GENERATOR 
    parser_keys.add_argument("-p", "--PRIVATE_KEY_PASSWORD", default='', help="Private key passphased used to encrypt keys.  Provided during authentication use RSA keys.")

    # Store passed in values
    subcommand = parser.parse_args().subcommand
    args = vars(parser.parse_args())
    
    # Checks
    if subcommand is None:
        raise Exception('Missing deployer command.  Must call via "snowflake_deployer [deploy/import]" command. See documentation for further details.')
    elif subcommand.upper() not in ('DEPLOY','IMPORT','KEYS'):
        raise Exception('Invalid deployer command.  Must call via "snowflake_deployer [deploy/import]" command. See documentation for further details.')
    
    if subcommand.upper() == 'DEPLOY':
        snowflake_deploy(args)
    elif subcommand.upper() == 'IMPORT':
        snowflake_import(args)
    elif subcommand.upper() == 'KEYS':
        snowflake_generate_rsa_keys(args)
        
