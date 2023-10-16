import re
import time
import urllib.parse
import TheSilent.puppy_requests as puppy_requests
from TheSilent.clear import clear

CYAN = "\033[1;36m"

def kitten_crawler(host,delay=0):
    clear()
    hosts = [host]
    progress = -1
    while True:
        hosts = list(dict.fromkeys(hosts))
        progress += 1
        time.sleep(delay)
        try:
            print(CYAN + hosts[progress])
        except IndexError:
            break
        try:
            data = puppy_requests.text(hosts[progress])
            links = re.findall("href\s?=\s?[\"\'](\S+)[\"\']",data)
            for link in links:
                if link.startswith("http://") and urllib.parse.urlparse(host).netloc in link or link.startswith("https://") and urllib.parse.urlparse(host).netloc in link:
                    if not re.search("script|\'|\"",link.lower()):
                        new_link = link.rstrip("/")
                        hosts.append(link)
                elif link.startswith("/"):
                    if not re.search("script|\'|\"",link.lower()):
                        new_link = f"{host}{link}"
                        new_link = new_link.rstrip("/")
                        hosts.append(new_link)
                elif not link.startswith("http://") and not link.startswith("https://"):
                    if not re.search("script|\'|\"",link.lower()):
                        new_link = f"{host}/{link}"
                        new_link = new_link.rstrip("/")
                        hosts.append(new_link)
        except:
            continue

    return hosts
