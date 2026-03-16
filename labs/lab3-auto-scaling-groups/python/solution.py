import boto3
import base64

ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")
autoscaling = boto3.client('autoscaling', endpoint_url="http://localhost:4566", region_name="us-east-1")
elbv2 = boto3.client('elbv2', endpoint_url="http://localhost:4566", region_name="us-east-1")

images = ec2.describe_images()
ami_id = images['Images'][0]['ImageId']

sgs = ec2.describe_security_groups()
sg_id = sgs['SecurityGroups'][0]['GroupId']

user_data = '''#!/bin/bash
echo "Hello from LocalStack Web Server!" > index.html
python3 -m http.server 80 &
'''
user_data_b64 = base64.b64encode(user_data.encode('utf-8')).decode('utf-8')

lt_response = ec2.create_launch_template(
    LaunchTemplateName='WebServersLT',
    LaunchTemplateData={
        'ImageId': ami_id,
        'InstanceType': 't3.micro',
        'SecurityGroupIds': [sg_id],
        'UserData': user_data_b64
    }
)
lt_id = lt_response['LaunchTemplate']['LaunchTemplateId']

subnets = ec2.describe_subnets()
subnet_ids = [s['SubnetId'] for s in subnets['Subnets'][:2]]
subnet_ids_str = ",".join(subnet_ids)

target_groups = elbv2.describe_target_groups(Names=['WebTG'])
tg_arn = target_groups['TargetGroups'][0]['TargetGroupArn']

autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='WebASG',
    LaunchTemplate={
        'LaunchTemplateId': lt_id,
        'Version': '1'
    },
    MinSize=1,
    MaxSize=4,
    DesiredCapacity=2,
    VPCZoneIdentifier=subnet_ids_str,
    TargetGroupARNs=[tg_arn]
)
