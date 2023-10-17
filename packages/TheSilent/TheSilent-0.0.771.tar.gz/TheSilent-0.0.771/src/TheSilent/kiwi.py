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

    subdomains = ["adfs","aes","airwatch","aplus","asg","cl","destiny","docefill","documentservices","ees","ess","etcentral","etsts","exchange","filewave","filter","finance","helpdesk","iboss","inow","inowhome","intranet","lib","library","mail","moodle","parentportal","payroll","portal","rocket","sets","sis","staffportal","studentportal","transportation","vpn","webmail","websets","wiki","www"]
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
