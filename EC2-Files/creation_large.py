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

# Launch t2.large EC2 instances for stand-alone
proxy_instance = ec2_client.run_instances(
    ImageId='ami-053b0d53c279acc90',
    UserData=open('proxy_config.sh').read(),
    PrivateIpAddress = '172.31.30.30',
    InstanceType='t2.large',
    MinCount=1,
    MaxCount=1,
    Placement={'AvailabilityZone': 'us-east-1a'},
    KeyName='finalProject',
    SecurityGroups=[security_group_name]
)

gatekeeper_instance = ec2_client.run_instances(
    ImageId='ami-053b0d53c279acc90',
    PrivateIpAddress = '172.31.30.35',
    InstanceType='t2.large',
    MinCount=1,
    MaxCount=1,
    Placement={'AvailabilityZone': 'us-east-1a'},
    KeyName='finalProject',
    SecurityGroups=[security_group_name]
)


trusted_host_instance = ec2_client.run_instances(
    ImageId='ami-053b0d53c279acc90',
    PrivateIpAddress = '172.31.30.40',
    InstanceType='t2.large',
    MinCount=1,
    MaxCount=1,
    Placement={'AvailabilityZone': 'us-east-1a'},
    KeyName='finalProject',
    SecurityGroups=[security_group_name]
)