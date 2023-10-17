import importlib
import io
import random
import re
import time
import urllib.parse
import TheSilent.kitten_crawler as kitten_crawler
import TheSilent.puppy_requests as puppy_requests
from TheSilent.clear import clear
from TheSilent.return_user_agent import return_user_agent

RED = "\033[1;31m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"

def pumpkin_scanner(init_host,delay=0,scripts=None):
    clear()
    hits = []
    file_list = [".doc",".docx",".gif",".ico",".jpeg",".jpg",".m4a",".mp3",".mp4",".pdf",".png"]
    host_list = kitten_crawler.kitten_crawler(init_host,delay)
    host_list = random.sample(host_list[:],len(host_list[:]))
    for host in host_list:
        time.sleep(delay)
        print(CYAN + f"scanning for interesting things on {host}")
        try:
            if scripts != None:
                data = puppy_requests.text(host,raw=True)
                for script in scripts:
                    if script == "faces":
                        init_script = importlib.import_module(script)
                        init_script.read(data,urllib.parse.urlparse(host).netloc + urllib.parse.urlparse(host).path.replace("/","<>"))

                    if script == "identify":
                        init_script = importlib.import_module(script)
                        result = init_script.read(data)
                        if result == "True":
                            with open(f"{urllib.parse.urlparse(init_host).netloc}_identify.txt","a") as file:
                                file.write(f"{host}: True\n")

                    if script == "ocr":
                        init_script = importlib.import_module(script)
                        img_data = init_script.read(io.BytesIO(data))
                        if len(img_data) > 0 and re.search("\w",img_data):
                            with open(f"{urllib.parse.urlparse(init_host).netloc}_ocr.txt","a") as file:
                                file.write(f"{host}: {img_data}\n")

            else:
                data = puppy_requests.text(host,raw=False)

            if scripts != None:
                emails = re.findall("[\w\.]{3,}@[\w\.]{3,}",data.decode(errors="ignore"))
                for email in emails:
                    hits.append(f"{email}: {host}")

                if re.search("type=[\"\']password[\"\']",data.decode(errors="ignore").lower()):
                    hits.append(f"password field: {host}")

                ip_addresses = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",data.decode(errors="ignore"))
                for ip_address in ip_addresses:
                    hits.append(f"potential ip address- {ip_address}: {host}")

            else:
                emails = re.findall("[\w\.]{3,}@[\w\.]{3,}",data)
                for email in emails:
                    hits.append(f"{email}: {host}")

                if re.search("type\s{0,4}=\s{0,4}[\"\']password[\"\']",data.lower()):
                    hits.append(f"password field: {host}")

                ip_addresses = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",data)
                for ip_address in ip_addresses:
                    hits.append(f"potential ip address- {ip_address}: {host}")

        except:
            pass

        for _ in file_list:
            if _ in host:
                hits.append(f"potential interesting file: {host}")
                break

    hits = list(set(hits[:]))
    hits.sort()
    clear()
            
    if len(hits) > 0:
        with open(f"{urllib.parse.urlparse(init_host).netloc}.txt","a") as file:
            for hit in hits:
                file.write(hit + "\n")

        for hit in hits:
            print(GREEN + hit)
