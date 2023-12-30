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


# Create Security Group
security_group_response = ec2_client.create_security_group(
    GroupName=security_group_name,
    Description=security_group_description,
)

security_group_id = security_group_response['GroupId']

# Authorize Security Group Ingress for SSH and HTTP
ec2_client.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpProtocol='tcp',
    FromPort=22,
    ToPort=22,
    CidrIp='0.0.0.0/0'
)

ec2_client.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpProtocol='tcp',
    FromPort=80,
    ToPort=80,
    CidrIp='0.0.0.0/0'
)

# Launch t2.micro EC2 instances
t2_instance_response = ec2_client.run_instances(
    ImageId='ami-053b0d53c279acc90',
    InstanceType='t2.micro',
    MinCount=4,
    MaxCount=4,
    Placement={'AvailabilityZone': 'us-east-1a'},
    KeyName='finalProject',
    SecurityGroups=[security_group_name]
)

# Save the created security group id to a file for future reference
with open('security_group_id.txt', 'w') as f:
    f.write(security_group_id)
