import paramiko

proxy_public_addr = '18.215.158.107'
proxy_private_addr = '172.31.30.30'
target_addr = '172.31.30.10'

private_key_path = paramiko.RSAKey.from_private_key_file("finalProject.pem")

proxy=paramiko.SSHClient()
proxy.set_missing_host_key_policy(paramiko.AutoAddPolicy())
proxy.connect(proxy_public_addr, username='ubuntu', pkey=private_key_path)

proxy_transport = proxy.get_transport()
src_addr = (proxy_private_addr, 22)
dest_addr = (target_addr, 22)
proxy_channel = proxy_transport.open_channel("direct-tcpip", dest_addr, src_addr)

target=paramiko.SSHClient()
target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
target.connect(target_addr, username='ubuntu', pkey= private_key_path, sock=proxy_channel)

stdin, stdout, stderr = target.exec_command(f"mysql -u root -pBlank -e 'USE sakila;{query};'")

result = stdout.read().decode("utf-8")

with open('direct-sql-query.txt', 'w') as f:
    f.write(result)

target.close()
proxy.close()