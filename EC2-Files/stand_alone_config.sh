#!/bin/bash

sudo apt-get update
sudo apt install sysbench -y
sudo apt install mysql-server  -y

wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xf sakila-db.tar.gz

sudo mysql -e "SOURCE sakila-db/sakila-schema.sql;"
sudo mysql -e "SOURCE sakila-db/sakila-data.sql;"
sudo mysql -e "USE sakila;"
