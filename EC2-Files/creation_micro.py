# Imports
import boto3
from credentials import aws_access_key_id, aws_secret_access_key, aws_session_token, aws_region
from security_information import security_group_name , security_group_description

# AWS CLI configuration values
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=aws_region
)

# Initialize the EC2 client
ec2_client = session.client('ec2')

# Launch t2.micro EC2 instances for stand-alone
t2_instance_response_alone = ec2_client.run_instances(
    ImageId='ami-053b0d53c279acc90',
    UserData=open('stand_alone_config.sh').read(),
    PrivateIpAddress = '172.31.30.20',
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    Placement={'AvailabilityZone': 'us-east-1a'},
    KeyName='finalProject',
    SecurityGroups=[security_group_name]
)

# Launch t2.micro 4 EC2 instances for clusters and adresses are important for sh file to work 
t2_instance_response_cluster = ec2_client.run_instances(
    ImageId='ami-053b0d53c279acc90',
    UserData=open('cluster_master_config.sh').read(),
    InstanceType='t2.micro',
    PrivateIpAddress = '172.31.30.10',
    MinCount=1,
    MaxCount=1,
    Placement={'AvailabilityZone': 'us-east-1a'},
    KeyName='finalProject',
    SecurityGroups=[security_group_name]
)

t2_instance_response_cluster = ec2_client.run_instances(
    ImageId='ami-053b0d53c279acc90',
    UserData=open('cluster_slave_config.sh').read(),
    InstanceType='t2.micro',
    PrivateIpAddress = '172.31.30.11',
    MinCount=1,
    MaxCount=1,
    Placement={'AvailabilityZone': 'us-east-1a'},
    KeyName='finalProject',
    SecurityGroups=[security_group_name]
)

t2_instance_response_cluster = ec2_client.run_instances(
    ImageId='ami-053b0d53c279acc90',
    UserData=open('cluster_slave_config.sh').read(),
    InstanceType='t2.micro',
    PrivateIpAddress = '172.31.30.12',
    MinCount=1,
    MaxCount=1,
    Placement={'AvailabilityZone': 'us-east-1a'},
    KeyName='finalProject',
    SecurityGroups=[security_group_name]
)

t2_instance_response_cluster = ec2_client.run_instances(
    ImageId='ami-053b0d53c279acc90',
    InstanceType='t2.micro',
    PrivateIpAddress = '172.31.30.13',
    UserData=open('cluster_slave_config.sh').read(),
    MinCount=1,
    MaxCount=1,
    Placement={'AvailabilityZone': 'us-east-1a'},
    KeyName='finalProject',
    SecurityGroups=[security_group_name]
)

# Extract instance IDs and save to a file
instance_ids_cluster = [instance['InstanceId'] for instance in t2_instance_response_cluster['Instances']]

instance_ids_alone = [instance['InstanceId'] for instance in t2_instance_response_alone['Instances']]

with open('instance_ids.txt', 'w') as f:
    for instance_id in instance_ids_cluster:
        f.write(instance_id + '\n')
    f.write("------------------------------------------------"+ '\n')
    for instance_id in instance_ids_alone:
        f.write(instance_id + '\n')