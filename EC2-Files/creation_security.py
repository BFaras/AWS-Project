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

# Authorize Security Group Ingress for SSH 
ec2_client.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpProtocol='tcp',
    FromPort=22,
    ToPort=22,
    CidrIp='0.0.0.0/0'
)
