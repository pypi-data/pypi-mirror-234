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

    subdomains = ["ac","acc","adfs","admin","analytics","athletics","autodiscover","barracuda","bus","chs","ckm","ckm01","ckr01","classlink","classroom","clinkproxy","clinksso","cms","cognos","compass","connect","covid","covidash","cpanel","cpcalendars","cpcontacts","csa","cte","daep","destiny","dns1","eac","ecc","eduphoria","email","es","eschool","eschoolplus","exchange","expe","fe","filter","forms","freeandreduced","fs","ftp","gp","gradebook","gradespeed","hac","helpdesk","hhs","homeaccess","hr","hs","hslibrary","iboss","iron","is","jobs","kronos","ldap","ldaps","legacy","library","lightspeed","mail","mail2","mdm","media","metasys","mileage","mobile","moodle","ms","mss","my","news","ns1","ns2","ns3","old","oneroster","owa","passwordreset","pdas","portal","prtg","ps","pwe","recruitment","register","remote","remotesupport","rocket","safari","schools","security","selfservice","sftp","sis","skyward","skyweb","spam","sslvpn","sso","statements","student","stvtsync","support","tac","tech","technology","tems","timeclock","tms","transfinder","travel","ttc","vdi","versatrans","volunteer","vpn","webapps","webcenter","webctrl","webdisk","webmail","www","www2"]
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
