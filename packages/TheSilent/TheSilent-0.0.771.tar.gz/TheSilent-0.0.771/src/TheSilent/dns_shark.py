import itertools
import socket
from TheSilent.clear import clear

CYAN = "\033[1;36m"

def dns_shark(host, attempts=10):
    clear()
    characters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]
    pages = []
    pages.append(host)
    tracker = -1
    attempt = 0
    for attempt in range(attempts):
        combos = itertools.product(characters, repeat=attempt+1)
        for combo in combos:
            my_tuple = ""
            for tuples in combo:
                my_tuple += tuples

            new_host = my_tuple + "." + host
            print(CYAN + f"checking: {new_host}/tcp")
            try:
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                my_socket.settimeout(15)
                my_socket.connect((new_host,80))
                my_socket.close()
                with open("dns_report.txt", "a") as file:
                    file.write(new_host + "/tcp\n")

            except ConnectionRefusedError:
                with open("dns_report.txt", "a") as file:
                    file.write(new_host + "/tcp\n")
                
            except (socket.gaierror, TimeoutError):
                my_socket.close()

            print(CYAN + f"checking: {new_host}/udp")
            try:
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                my_socket.settimeout(15)
                my_socket.sendto(b"",(new_host,80))
                with open("dns_report.txt", "a") as file:
                    file.write(new_host + "/udp\n")

            except ConnectionRefusedError:
                with open("dns_report.txt", "a") as file:
                    file.write(new_host + "/udp\n")

            except (socket.gaierror, TimeoutError):
                continue
