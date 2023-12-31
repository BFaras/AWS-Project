#!/usr/bin/env python3

import os
import paramiko

jumpbox_public_addr = '18.215.158.107'
jumpbox_private_addr = '172.31.30.30'
target_addr = '172.31.30.10'

private_key_path = paramiko.RSAKey.from_private_key_file("finalProject.pem")

jumpbox=paramiko.SSHClient()
jumpbox.set_missing_host_key_policy(paramiko.AutoAddPolicy())
jumpbox.connect(jumpbox_public_addr, username='ubuntu', pkey=private_key_path)

jumpbox_transport = jumpbox.get_transport()
src_addr = (jumpbox_private_addr, 22)
dest_addr = (target_addr, 22)
jumpbox_channel = jumpbox_transport.open_channel("direct-tcpip", dest_addr, src_addr)

target=paramiko.SSHClient()
target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
target.connect(target_addr, username='ubuntu', pkey= private_key_path, sock=jumpbox_channel)

stdin, stdout, stderr = target.exec_command("mysql -u root -pClusterPassword -e 'USE sakila;SELECT * FROM store;'")

result = stdout.read().decode("utf-8")

with open('store_result.txt', 'w') as f:
    f.write(result)

target.close()
jumpbox.close()