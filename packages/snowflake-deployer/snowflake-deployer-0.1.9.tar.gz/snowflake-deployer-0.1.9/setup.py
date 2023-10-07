from setuptools import setup, find_packages
#import pathlib
#import pkg_resources

#with pathlib.Path('requirements.txt').open() as requirements_txt:
#    install_requires = [
#        str(requirement)
#        for requirement
#        in pkg_resources.parse_requirements(requirements_txt)
#    ]


setup(
    name='snowflake-deployer',
    version='0.1.9',
    description='Snowflake state based deployer',
    long_description='Deploy objects to Snowflake instance in a stateful manner.  See Project Docs for details.',
    long_description_content_type="text/markdown",
    author='Justin Hanson, Jernej Plankelj',
    entry_points = {
        'console_scripts': ['snowflake-deployer=src.cli:cli'],
        #'console_scripts': ['snowflake_deployer=src.command_line:cli'],
    },
    #install_requires=install_requires,
    install_requires=['cryptography','snowflake-connector-python','pyyaml','schema','jinja2'],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    keywords = ['SNOWFLAKE','DATAOPS','DEVOPS','DATA','DEPLOYMENT'],
    project_urls = {
        'Project Docs': 'https://metaopslabs.github.io/snowflake_deployer/'
    }

) 
