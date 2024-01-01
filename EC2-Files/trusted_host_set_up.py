import paramiko

# Set your SSH key and trusted host details
private_key_path = 'finalProject'
trusted_host_ip = '54.34.10.21'

# Connect to the trusted host
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(trusted_host_ip, username='ubuntu', key_filename=private_key_path)

# Implement iptables rules (customize as needed)
iptables_rules = [
    'sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT',  # Allow SSH
    'sudo iptables -A INPUT -p tcp --dport 3306 -j ACCEPT',  # Allow MySQL
    'sudo iptables -A INPUT -j DROP'  # Drop all other incoming traffic
]

# Execute iptables rules
for rule in iptables_rules:
    stdin, stdout, stderr = ssh.exec_command(rule)
    print(stdout.read().decode("utf-8"))

# Disconnect from the trusted host
ssh.close()