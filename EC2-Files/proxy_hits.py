import sys
import time
import mysql.connector
import random

IPs = [
    'master': 'ip-172-31-17-1.ec2.internal',
    'slave1': 'ip-172-31-17-2.ec2.internal',
    'slave2': 'ip-172-31-17-3.ec2.internal',
    'slave3': 'ip-172-31-17-4.ec2.internal'
]


def execute_queries(ip, name, query):
    # Connect to MySQL server through SSH tunnel



    with mysql.connector.connect(
        host=IPs[name],
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
    target = "ip-172-31-30-10.ec2.internal"
    execute_queries('127.0.0.1', 'master', query, target)

def random_hit(query):
    targets = ["ip-172-31-30-11.ec2.internal", "ip-172-31-30-12.ec2.internal","ip-172-31-30-13.ec2.internal"]
    target = random.choice(targets)
    execute_queries('127.0.0.1', 'master', query, target)


if __name__ == "__main__":
    SQL_query = sys.argv[1]
    direct_hit(SQL_query)
    time.sleep(45)
    random_hit(SQL_query)
