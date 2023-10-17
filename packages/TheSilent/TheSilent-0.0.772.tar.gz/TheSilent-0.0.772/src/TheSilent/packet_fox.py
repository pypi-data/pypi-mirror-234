import binascii
import socket
import threading
from TheSilent.clear import clear

CYAN = "\033[1;36m"
RED = "\033[1;31m"

def packet_thread(interface):
    sniffer_socket = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.ntohs(3))
    sniffer_socket.bind((interface[1],0))
    print(CYAN + f"listening on interface {interface[1]}")
    while True:
        try:
            packet = sniffer_socket.recv(65536)
            data = binascii.hexlify(packet).decode()
            with open("hex_dump.txt", "a") as file:
                file.write(data + "\n")

        except OSError:
            print(RED + f"interface {interface[1]} is down")
            break

def packet_fox():
    clear()
    interfaces = socket.if_nameindex()
    for interface in interfaces:
        if "lo" not in interface[1] and "bond" not in interface[1]:
            my_thread = threading.Thread(target=packet_thread, args=[interface]).start()

packet_fox()
