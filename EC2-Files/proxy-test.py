#!/usr/bin/env python3

import paramiko
import sys
import time
import random
import subprocess

def direct_hit(query):
    proxy_public_addr = '18.215.158.107'
    proxy_private_addr = '172.31.30.30'
    target_addr = '172.31.30.10'

    private_key_path = paramiko.RSAKey.from_private_key_file("finalProject.pem")

    proxy=paramiko.SSHClient()
    proxy.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    proxy.connect(proxy_public_addr, username='ubuntu', pkey=private_key_path)

    proxy_transport = proxy.get_transport()
    src_addr = (proxy_private_addr, 22)
    dest_addr = (target_addr, 22)
    proxy_channel = proxy_transport.open_channel("direct-tcpip", dest_addr, src_addr)

    target=paramiko.SSHClient()
    target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    target.connect(target_addr, username='ubuntu', pkey= private_key_path, sock=proxy_channel)

    stdin, stdout, stderr = target.exec_command(f"mysql -u root -pBlank -e 'USE sakila;{query};'")

    result = stdout.read().decode("utf-8")

    with open('direct-sql-query.txt', 'w') as f:
        f.write(result)

    target.close()
    proxy.close()

def random_hit(query):
    proxy_public_addr = '18.212.208.229'
    proxy_private_addr = '172.31.30.30'
    target_addr = random.choice(['172.31.30.11','172.31.30.12','172.31.30.13'])

    private_key_path = paramiko.RSAKey.from_private_key_file("finalProject.pem")

    proxy=paramiko.SSHClient()
    proxy.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    proxy.connect(proxy_public_addr, username='ubuntu', pkey=private_key_path)

    proxy_transport = proxy.get_transport()
    src_addr = (proxy_private_addr, 22)
    dest_addr = (target_addr, 22)
    proxy_channel = proxy_transport.open_channel("direct-tcpip", dest_addr, src_addr)

    target=paramiko.SSHClient()
    target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    target.connect(target_addr, username='ubuntu', pkey= private_key_path, sock=proxy_channel)

    stdin, stdout, stderr = target.exec_command(f"mysql -u root -pBlank -e 'USE sakila;{query};'")

    result = stdout.read().decode("utf-8")

    with open('random-sql-query.txt', 'w') as f:
        f.write(result)

    target.close()
    proxy.close()


def measure_ping_time(host):
    # Run the ping command and capture the output
    result = subprocess.run(['ping', '-c', '3', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
    lines = result.stdout.splitlines()
    # Extract the average round-trip time (RTT)
    rtt_line = lines[-1]
    rtt = float(rtt_line.split('/')[4])
    return rtt

def customized_hit(query):
    proxy_public_addr = '18.212.208.229'
    proxy_private_addr = '172.31.30.30'
    target_addrs = ['172.31.30.10', '172.31.30.11', '172.31.30.12', '172.31.30.13']

    private_key_path = paramiko.RSAKey.from_private_key_file("finalProject.pem")

    # Measure ping times for all target servers
    ping_times = {target: measure_ping_time(target) for target in target_addrs}

    # Choose the target with the lowest ping time
    target_addr = min(ping_times, key=ping_times.get())

    proxy = paramiko.SSHClient()
    proxy.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    proxy.connect(proxy_public_addr, username='ubuntu', pkey=private_key_path)

    proxy_transport = proxy.get_transport()
    src_addr = (proxy_private_addr, 22)
    dest_addr = (target_addr, 22)
    proxy_channel = proxy_transport.open_channel("direct-tcpip", dest_addr, src_addr)

    target = paramiko.SSHClient()
    target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    target.connect(target_addr, username='ubuntu', pkey=private_key_path, sock=proxy_channel)

    stdin, stdout, stderr = target.exec_command(f"mysql -u root -pBlank -e 'USE sakila;{query};'")

    result = stdout.read().decode("utf-8")

    with open('customized-sql-query.txt', 'w') as f:
        f.write(f"Selected target: {target_addr}\n")
        f.write(result)

    target.close()
    proxy.close()

if __name__ == "__main__":
    #parameter needs to be single quote
    SQL_query = sys.argv[1]
    direct_hit(SQL_query)
    time.sleep(30)
    random_hit(SQL_query)
    time.sleep(30)
    customized_hit(SQL_query)

