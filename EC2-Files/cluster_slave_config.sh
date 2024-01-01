#!/bin/bash

sudo apt update
sudo apt install libclass-methodmaker-perl libncurses5 -y

wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb

#This option specifies the location of the MySQL Cluster Manager. I was unable to connect until I added this part
echo "
[mysql_cluster]
# Options for NDB Cluster processes:
ndb-connectstring=ip-172-31-30-10.ec2.internal # location of cluster manager
" | tee -a /etc/my.cnf


sudo mkdir -p /usr/local/mysql/data

#The service unit defines how the ndbd process should be managed by systemd
echo "
[Unit]
Description=MySQL NDB Data Node Daemon
After=network.target auditd.service

[Service]
Type=forking
ExecStart=/usr/sbin/ndbd
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
" | tee -a /etc/systemd/system/ndbd.service

#fix the problem about error 13 couldn t start daemon 
sudo systemctl daemon-reload
sudo systemctl enable ndbd
sudo systemctl start ndbd