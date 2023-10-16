import os
import sys, argparse

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Function run yaml file datahub')
    parser.add_argument("-d", "--database_name", help="database_name")
    parser.add_argument("--allow", nargs="+", help='list table pattern allow')
    parser.add_argument("--deny", nargs="+", help='list table pattern deny')
    parser.add_argument("--file_password", help='Path file to file have user and password')
    parser.add_argument("--user", help='User name')
    parser.add_argument("--profiling", help="Enable profiling")
    parser.add_argument("--password", help='PassWord')

    options = parser.parse_args(args)
    return options

def create_yaml_file(username, password, database_name, table_pattern_allow = [], table_pattern_deny = [], profiling=False):
    if table_pattern_allow:
        table_pattern_allow_txt = '            allow:\n'

        for i in table_pattern_allow:
            table_pattern_allow_txt += "                - " + database_name + '.' + i +'$\n'
    else:
        table_pattern_allow_txt = ''
        
    if table_pattern_deny:
        table_pattern_deny_txt = '\n'
    
        for i in table_pattern_deny:
            table_pattern_deny_txt += "                - " + database_name + '.' + i +'\n'
    else:
        table_pattern_deny_txt = ''
        
    if profiling:
        profiling = """
        profiling:
            enabled: true 
        """
    else:
        profiling = ""

    yaml = f"""
source:
    type: sqlalchemy
    config:
        platform: hive
        connect_uri: "hive://{username}:{password}@172.24.178.40:10009/{database_name}"
        include_views: False
        table_pattern:
{table_pattern_allow_txt}
            deny:
                - "{database_name}.test.*"
                - "{database_name}.tmp.*"
                - "{database_name}.bk.*"
                - "{database_name}.backup.*"
                - "{database_name}.view_.*"
                
                - ".*test.*"
                - ".*backup.*"
                - ".*tmp.*"
{table_pattern_deny_txt}
        schema_pattern:
            allow:
                - "{database_name}"
            deny:
                - "information_schema"
        options:
            connect_args:
                auth: 'LDAP'

{profiling}
sink:
    type: "datahub-rest"
    config:
        server: "http://gms-dev-datahub.cads.live"
    
    """
    
    
    with open(f'datahub_ingest_{database_name}.yaml', 'w') as file:
        file.write(yaml)
    
    return f'datahub_ingest_{database_name}.yaml'
    
def run_yaml_file(yaml_file_name):
    os.system(f'datahub ingest -c {yaml_file_name}')

if __name__ == '__main__':
    options = getOptions()
    file_password = options.file_password
    password = options.password
    profiling = options.profiling

    if file_password:
        f = open(options.file_password, "r")
        PASSWORD = f.read()
        PASSWORD = PASSWORD.strip()

    elif password:
        PASSWORD = password

    yaml_file_name = create_yaml_file(
        username = options.user,
        password = PASSWORD,
        database_name = options.database_name,
        table_pattern_allow=options.allow,
        table_pattern_deny=options.deny,
        profiling=profiling
     )


    run_yaml_file(yaml_file_name)
