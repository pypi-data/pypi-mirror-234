import random
import socket
import time
from TheSilent.clear import clear

CYAN = "\033[1;36m"

def kiwi(host,delay=0):
    clear()
    hits = []
    init_hosts = []
    hosts = []

    subdomains = ["adfs","analytics","athletics","autodiscover","barracuda","ckm","ckm01","ckr01","clinksso","covid","covidash","cpanel","cpcalendars","cpcontacts","destiny","dns1","eac","eduphoria","email","eschool","exchange","expe","filter","forms","ftp","gp","gradebook","gradespeed","hac","hhs","hr","hs","hslibrary","iron","is","library","lightspeed","mail","mail2","mdm","mileage","moodle","ms","my","ns1","ns2","old","owa","portal","register","skyward","sso","student","tech","tems","timeclock","transfinder","travel","ttc","vpn","webapps","webctrl","webdisk","webmail","www"]

    subdomains = random.sample(subdomains,len(subdomains))
    for _ in subdomains:
        # check reverse dns
        print(CYAN + f"checking for reverse dns on {_}.{host}")
        dns_host = f"{_}.{host}"
        time.sleep(delay)
        try:
            hits.append(f"reverse dns {_}.{host}: {socket.gethostbyaddr(dns_host)}")
        except:
            pass
        # check if host is up
        print(CYAN + f"checking {_}.{host}")
        try:
            my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            my_socket.settimeout(1.25)
            my_socket.connect((f"{_}.{host}",80))
            my_socket.close()
            hits.append(f"found {_}.{host}")
        except ConnectionRefusedError:
            hits.append(f"found {_}.{host}")
        except socket.timeout:
            hits.append(f"found {_}.{host}")
        except:
            pass

    clear()
    hits.sort()
    for hit in hits:
        print(CYAN + hit)

    print(CYAN + f"{len(hits)} results")
