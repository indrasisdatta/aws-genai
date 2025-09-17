import boto3 

ssm = boto3.client('ssm', region_name='eu-west-1')

def lambda_handler(event, context):
    print(event)
    param = ssm.get_parameter('AWS_S3_UPLOAD_BUCKET')
    print('SSM param:', param)



