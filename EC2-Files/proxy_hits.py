import sys
import time
import mysql.connector
import paramiko
import random

def create_ssh_tunnel(ssh_host, ssh_username, ssh_key_path, target_host, target_port):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(ssh_host, username=ssh_username, pkey=ssh_key_path)

    tunnel = ssh.get_transport().open_channel(
        'direct-tcpip', (target_host, target_port), ('127.0.0.1', 0)
    )

    return tunnel
def execute_queries(ip, name, query,target):

    with mysql.connector.connect(
        host=target,
        user='ubuntu',
        password='finalProject.pem',
        database='sakila',
        port=22,
        autocommit=True,
        ssh_pkey='finalProject.pem',
        use_pure=True
    ) as connection:
        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query)
            # Fetch and process results if needed
            for result in cursor.fetchall():
                print(result)


def direct_hit(query):
     # SSH tunnel configuration
    ip_host = '18.212.249.223'
    ssh_username = 'ubuntu'
    ssh_key_path = 'finalProject.pem'

    # Target MySQL server configuration
    target_host = 'ip-172-31-30-10.ec2.internal'
    target_port = 3306

    # Create an SSH tunnel
    ssh_tunnel = create_ssh_tunnel(ip_host, ssh_username, ssh_key_path, target_host, target_port)

    target = "ip-172-31-30-10.ec2.internal"
    execute_queries('127.0.0.1', 'master', query, target_host)

def random_hit(query):
    targets = ["ip-172-31-30-11.ec2.internal", "ip-172-31-30-12.ec2.internal","ip-172-31-30-13.ec2.internal"]
    target = random.choice(targets)
    execute_queries('127.0.0.1', 'master', query, target)


if __name__ == "__main__":
    SQL_query = sys.argv[1]
    
    direct_hit(SQL_query)

