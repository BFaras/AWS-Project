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

#slaves
#initialize database
cd /opt/mysqlcluster/home/mysqlc
sudo scripts/mysql_install_db --datadir=/opt/mysqlcluster/deploy/mysqld_data

#run database
cd /opt/mysqlcluster/home/mysqlc/bin
sudo mkdir -p /usr/local/mysql/mysql-cluster
sudo chown -R $USER:$USER /usr/local/mysql/mysql-cluster
sudo chown -R $USER:$USER /opt/mysqlcluster/deploy/ndb_data

#connect to master
sudo mkdir -p /opt/mysqlcluster/deploy/ndb_data
ndbd -c ip-172-31-30-117.ec2.internal:1186





#sakila set up
cd ~
wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xf sakila-db.tar.gz

sudo mysql -u root -e "SOURCE sakila-db/sakila-schema.sql;"
sudo mysql -u root  -e "SOURCE sakila-db/sakila-data.sql;"