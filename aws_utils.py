import os 
import boto3 

region_name='ap-south-1'

# Setup default boto3 session
aws_profile = os.getenv('AWS_PROFILE')
if aws_profile:
    # Local
    boto3.setup_default_session(profile_name=aws_profile, region_name='ap-south-1')
    print("Load AWS_PROFILE for boto3")
else:
    # EC2 IAM role
    boto3.setup_default_session(region_name=region_name)  
    print("AWS_PROFILE not found, use IAM role for boto3")

# SSM helper to load params into env
def load_ssm_params(param_names):
    ssm = boto3.client('ssm', region_name=region_name)
    # Check if any param requires decryption
    secure_params = []
    for name in param_names:
        param_type = ssm.get_parameter(Name=name)['Parameter']['Type']
        if param_type == 'SecureString':
            secure_params.append(name)
        
    # Only request decryption for secure params
    param_names = list(set(param_names) - set(secure_params))
    if secure_params:
        secure_response = ssm.get_parameters(Names=secure_params, WithDecryption=True)
        response = ssm.get_parameters(Names=param_names, WithDecryption=False)
        response['Parameters'].extend(secure_response['Parameters'])
    else:
        response = ssm.get_parameters(Names=param_names, WithDecryption=False)
    response = ssm.get_parameters(Names=param_names, WithDecryption=True)
    print('SSM params: ', response)
    for param in response['Parameters']:
        key = param['Name'].split('/')[-1] 
        os.environ[key] = param['Value']