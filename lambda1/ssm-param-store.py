import boto3 
import os 

# ssm = boto3.client('ssm', region_name='eu-west-1')

# Test code
session = boto3.Session(profile_name=os.getenv('AWS_PROFILE'), region_name="ap-south-1")
# session = boto3.Session(profile_name="awsapp-role-ap696l85", region_name="ap-south-1")
ssm = session.client('ssm')
params = ssm.get_parameters(Names=['MY_AWS_S3_BUCKET'])
print('SSM params:', params)

def lambda_handler(event, context):
    print(event)
    param = ssm.get_parameter('AWS_S3_UPLOAD_BUCKET')
    print('SSM param:', param)



