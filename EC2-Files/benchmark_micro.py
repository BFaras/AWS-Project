import paramiko


def benchmarking_alone():
    # Replace these with your actual values
    ec2_instance_ip = '54.167.1.228'
    private_key_path = paramiko.RSAKey.from_private_key_file("finalProject.pem")

    #command used by sysbench for benchmarking 
    prepare_sakila = 'sudo sysbench oltp_read_write --table-size=100000 --mysql-db=sakila --db-driver=mysql --mysql-user=root prepare'
    run_sakila = 'sudo sysbench oltp_read_write --table-size=100000 --mysql-db=sakila --db-driver=mysql --mysql-user=root --num-threads=6 --max-time=60 --max-requests=0 run > standaloneBenchmark.txt'
    clean_up_sakila = 'sudo sysbench oltp_read_write --table-size=100000 --mysql-db=sakila --db-driver=mysql --mysql-user=root cleanup'
    
    # Create an SSH client
    ssh = paramiko.SSHClient()

    # Automatically add the server's host key (this is insecure and should be improved in production)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the EC2 instance using the private key
    ssh.connect(ec2_instance_ip, username='ubuntu', pkey=private_key_path)

    # Run the command to prepare, run and clean up sakila 
    stdin , stdout, stderr = ssh.exec_command(prepare_sakila)
    print(stdout.read())

    stdin , stdout, stderr  = ssh.exec_command(run_sakila)
    print(stdout.read())

    stdin , stdout, stderr = ssh.exec_command(clean_up_sakila)
    print(stdout.read())

    #get file out of EC2 instance
    get_file_EC2_instance(ssh,'/home/ubuntu/standaloneBenchmark.txt',"./stand_alone_benchmarking.txt")

    # Close the SSH connection
    ssh.close()


def benchmarking_cluster():
    # Replace these with your actual values
    ec2_instance_ip = '54.221.8.227'
    private_key_path = paramiko.RSAKey.from_private_key_file("finalProject.pem")

    #command used by sysbench for benchmarking 
    prepare_sakila = "sudo sysbench oltp_read_write --table-size=100000 --mysql-db=sakila --db-driver=mysql --mysql-user=root --mysql-password=ClusterPassword  prepare"
    run_sakila = "sudo sysbench oltp_read_write --table-size=100000 --mysql-db=sakila --db-driver=mysql --mysql-user=root --mysql-password=ClusterPassword  --num-threads=6 --max-time=60 --max-requests=0 run > clusterBenchmark.txt"
    clean_up_sakila = "sudo sysbench oltp_read_write --table-size=100000 --mysql-db=sakila --db-driver=mysql --mysql-user=root --mysql-password=ClusterPassword cleanup"
    
    # Create an SSH client
    ssh = paramiko.SSHClient()

    # Automatically add the server's host key (this is insecure and should be improved in production)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the EC2 instance using the private key
    ssh.connect(ec2_instance_ip, username='ubuntu', pkey=private_key_path)

    # Run the command to prepare, run and clean up sakila 
    stdin , stdout, stderr = ssh.exec_command(prepare_sakila)
    print(stdout.read())

    stdin , stdout, stderr  = ssh.exec_command(run_sakila)
    print(stdout.read())

    stdin , stdout, stderr = ssh.exec_command(clean_up_sakila)
    print(stdout.read())

    #get file out of EC2 instance
    get_file_EC2_instance(ssh,'/home/ubuntu/clusterBenchmark.txt',"./cluster_benchmarking.txt")

    # Close the SSH connection
    ssh.close()


def get_file_EC2_instance(ssh_client,local_path,remote_path):
    ftp_client=ssh_client.open_sftp()
    ftp_client.get(local_path,remote_path)
    ftp_client.close()


if __name__ == "__main__":
    benchmarking_cluster()
