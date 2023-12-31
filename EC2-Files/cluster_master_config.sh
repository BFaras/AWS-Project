
#all nodes set up to install sql-cluster and link mysqlc to cluster
sudo apt-get update && sudo apt-get -y install libncurses5

sudo mkdir -p /opt/mysqlcluster/home
cd /opt/mysqlcluster/home
sudo wget http://dev.mysql.com/get/Downloads/MySQL-Cluster-7.2/mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz
sudo tar xvf mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz
sudo ln -s mysql-cluster-gpl-7.2.1-linux2.6-x86_64 mysqlc
echo 'export MYSQLC_HOME=/opt/mysqlcluster/home/mysqlc' | sudo tee /etc/profile.d/mysqlc.sh
echo 'export PATH=$MYSQLC_HOME/bin:$PATH' | sudo tee -a /etc/profile.d/mysqlc.sh
source /etc/profile.d/mysqlc.sh

#master set up
mkdir -p /opt/mysqlcluster/deploy
cd /opt/mysqlcluster/deploy
mkdir conf
mkdir mysqld_data
mkdir ndb_data
cd conf

echo '[mysqld]
ndbcluster
datadir=/opt/mysqlcluster/deploy/mysqld_data
basedir=/opt/mysqlcluster/home/mysqlc
port=3306' | sudo tee /opt/mysqlcluster/deploy/conf/my.cnf

echo '[ndb_mgmd]
hostname=ip-172-31-30-117.ec2.internal
datadir=/opt/mysqlcluster/deploy/ndb_data
nodeid=1

[ndbd default]
noofreplicas=3
datadir=/opt/mysqlcluster/deploy/ndb_data

[ndbd]
hostname=ip-172-31-31-180.ec2.internal
nodeid=2

[ndbd]
hostname=ip-172-31-16-239.ec2.internal
nodeid=3

[ndbd]
hostname=ip-172-31-25-143.ec2.internal
nodeid=4

[mysqld]
nodeid=50' | sudo tee /opt/mysqlcluster/deploy/conf/config.ini

#initialize database
cd /opt/mysqlcluster/home/mysqlc
sudo scripts/mysql_install_db --datadir=/opt/mysqlcluster/deploy/mysqld_data

#run database
cd /opt/mysqlcluster/home/mysqlc/bin
sudo mkdir -p /usr/local/mysql/mysql-cluster
sudo chown -R $USER:$USER /usr/local/mysql/mysql-cluster
sudo chown -R $USER:$USER /opt/mysqlcluster/deploy/ndb_data
ndb_mgmd -f /opt/mysqlcluster/deploy/conf/config.ini –initial –configdir=/opt/mysqlcluster/deploy/conf




#sakila set up
cd ~
wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xf sakila-db.tar.gz
rm sakila-db.tar.gz

sudo mysql -u root --e "SOURCE sakila-db/sakila-schema.sql;"
sudo mysql -u root --e "SOURCE sakila-db/sakila-data.sql;"