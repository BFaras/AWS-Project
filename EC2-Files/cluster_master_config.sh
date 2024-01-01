#!/bin/bash

# Update package information and install required dependencies
sudo apt update
sudo apt install libaio1 libmecab2 libncurses5 sysbench -y

# Download and install MySQL Cluster Management Server
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb

# Create a directory for MySQL Cluster
sudo mkdir /var/lib/mysql-cluster

# Configure MySQL Cluster
echo "

[ndb_mgmd]
hostname=ip-172-31-30-10.ec2.internal
datadir=/var/lib/mysql-cluster
NodeId=1

[ndbd default]
NoOfReplicas=3

[ndbd]
hostname=ip-172-31-30-11.ec2.internal
NodeId=2
datadir=/usr/local/mysql/data

[ndbd]
hostname=ip-172-31-30-12.ec2.internal
NodeId=3
datadir=/usr/local/mysql/data

[ndbd]
hostname=ip-172-31-30-13.ec2.internal
NodeId=4
datadir=/usr/local/mysql/data

[mysqld]
nodeid=50
" | sudo tee -a /var/lib/mysql-cluster/config.ini

# Configure MySQL NDB Cluster Management Server as a systemd service inspired from medium page
echo "
[Unit]
Description=MySQL NDB Cluster Management Server
After=network.target auditd.service

[Service]
Type=forking
ExecStart=/usr/sbin/ndb_mgmd -f /var/lib/mysql-cluster/config.ini
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
" | sudo tee -a /etc/systemd/system/ndb_mgmd.service

# Reload systemd and start MySQL NDB Cluster Management Server in order to avoir error 13
sudo systemctl daemon-reload
sudo systemctl enable ndb_mgmd
sudo systemctl start ndb_mgmd

# Download and install MySQL Cluster components
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar
mkdir install
tar -xvf mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar -C install/
cd install

sudo dpkg -i mysql-common_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-client_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-client_7.6.6-1ubuntu18.04_amd64.deb

# Set password and install MySQL Cluster Server
sudo debconf-set-selections <<< 'mysql-cluster-community-server_7.6.6 mysql-cluster-community-server/root-pass password Blank'
sudo debconf-set-selections <<< 'mysql-cluster-community-server_7.6.6 mysql-cluster-community-server/re-root-pass password Blank'
sudo debconf-set-selections <<< "mysql-cluster-community-server_7.6.6 mysql-server/default-auth-override select Use Legacy Authentication Method (Retain MySQL 5.x Compatibility)"

sudo dpkg -i mysql-cluster-community-server_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-server_7.6.6-1ubuntu18.04_amd64.deb

# Configure MySQL Cluster in my.cnf
echo "
[mysqld]
ndbcluster

[mysql_cluster]
ndb-connectstring=ip-172-31-30-10.ec2.internal
" | sudo tee -a /etc/mysql/my.cnf

# Restart and enable MySQL service
sudo systemctl restart mysql
sudo systemctl enable mysql

# Download and install Sakila sample database
cd ~
wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xf sakila-db.tar.gz
rm sakila-db.tar.gz

# Load Sakila schema and data into MySQL Cluster
sudo mysql -u root -pBlank -e "SOURCE sakila-db/sakila-schema.sql;"
sudo mysql -u root -pBlank -e "SOURCE sakila-db/sakila-data.sql;"