#!/usr/bin/python3
import socket
import sys
import threading
import time

usage = "Usage: python3 port_scan.py TARGET START_PORT END_PORT"

print("_" * 70)
print("
███╗░░██╗░░██╗██╗██╗░░░██╗███████╗░░██╗██╗███╗░░██╗░█████╗░██╗░░██╗░█████╗░░█████╗░
████╗░██║░██╔╝██║██║░░░██║██╔════╝░██╔╝██║████╗░██║██╔══██╗╚██╗██╔╝██╔══██╗██╔══██╗
██╔██╗██║██╔╝░██║╚██╗░██╔╝█████╗░░██╔╝░██║██╔██╗██║██║░░██║░╚███╔╝░██║░░██║██║░░██║
██║╚████║███████║░╚████╔╝░██╔══╝░░███████║██║╚████║██║░░██║░██╔██╗░██║░░██║██║░░██║
██║░╚███║╚════██║░░╚██╔╝░░███████╗╚════██║██║░╚███║╚█████╔╝██╔╝╚██╗╚█████╔╝╚█████╔╝
╚═╝░░╚══╝░░░░░╚═╝░░░╚═╝░░░╚══════╝░░░░░╚═╝╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝░╚════╝░░╚════╝░ ")

start_time = time.time()

if len(sys.argv) != 4:
    print(usage)
    sys.exit()

try:
    target = socket.gethostbyname(sys.argv[1])
except socket.gaierror:
    print("Name resolution error")
    sys.exit()

start_port = int(sys.argv[2])
end_port = int(sys.argv[3])

print("Scanning target", target)

open_ports = []

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    conn = s.connect_ex((target, port))
    if conn == 0:
        open_ports.append(port)
    s.close()

threads = []

for port in range(start_port, end_port + 1):
    thread = threading.Thread(target=scan_port, args=(port,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

if open_ports:
    print("Open ports:", open_ports)
else:
    print("No open ports found.")

end_time = time.time()
print("Time elapsed:", end_time - start_time)
