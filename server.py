#!/usr/bin/python3
import subprocess
import re
import pika
import datetime
import time
import socket
import pickle
import struct

h, p, m = " ", 2004, "network.b2a"

def record(v):
    d = [(m, (float(time.time()), float(v)))]
    payload = pickle.dumps(d, protocol=2)
    header = struct.pack("!L", len(payload))
    message = header + payload
    netC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    netC.connect((h, p))
    netC.sendall(message)
    netC.close()
    print(d)


interval = str(3)
port = str(53)
ttl = str(60*60*24*70)
cmd = subprocess.Popen(['iperf', '-s', '-u', '-i', interval, '-p', port, '-t', ttl], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while True:
  line = cmd.stdout.readline().decode('utf-8')
  r=re.search('Mbits\/+sec[\s]+([\d.]+)[\s]+ms', line) 
  if r:
    try:
    	record(r.group(1))
    except:
        print('network error')
