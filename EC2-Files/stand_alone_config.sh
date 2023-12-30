#!/bin/bash

sudo apt-get update
sudo apt install sysbench -y
sudo apt install mysql-server  -y

echo "sysbench and mysql-server ready "

wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xf sakila-db.tar.gz

echo "sakila downloaded in $(pwd)"

sudo mysql -e "SOURCE sakila-db/sakila-schema.sql;"
sudo mysql -e "SOURCE sakila-db/sakila-data.sql;"
sudo mysql -e "USE sakila;"

echo "sakila databse is ready to use"