import os
import re
import shutil
from TheSilent.clear import clear

CYAN = "\033[1;36m"
RED = "\033[1;31m"
GREEN = "\033[0;32m"

def oyster_av(directory):
    clear()
    malware_list = []
    hash_list = []
    count = -1

    mal_def = ["ettercap","metasploit","nessus","nikto","openvas","sqlmap"]
    mal_list = []

    for root,directories,files in os.walk(directory, topdown=True):
        for directory in directories:
            try:
                for file in files:
                    if os.path.isfile(root + "/" + directory + "/" + file) and os.path.getsize(root + "/" + directory + "/" + file) > 0  and os.path.getsize(root + "/" + directory + "/" + file) <= 4294967296:
                        print(CYAN + root + "/" + directory + "/" + file)
                        with open(root + "/" + directory + "/" + file, "rb") as f:
                            data = f.read()
                        data = data.decode(errors="ignore")
                        for _ in mal_def:
                            if re.search(_,data.lower()):
                                mal_list.append(root + "/" + directory + "/" + file)

            except PermissionError:
                print(RED + "ERROR! Permission Denied!")
                continue

            except OSError as error:
                if error.errno == 61:
                    continue

    clear()

    mal_list = list(set(mal_list[:]))
    mal_list.sort()
    if len(mal_list) > 0:
        print(RED + "potential hacking tools found:")
        for malware in mal_list:
            print(RED + f"found: {malware}")

    else:
        print(GREEN + "no malware found")

oyster_av("/")
