import boto3

elbv2 = boto3.client('elbv2', endpoint_url="http://localhost:4566", region_name="us-east-1")
ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

vpcs = ec2.describe_vpcs()
vpc_id = vpcs['Vpcs'][0]['VpcId']

tg_response = elbv2.create_target_group(
    Name='WebTG',
    Protocol='HTTP',
    Port=80,
    VpcId=vpc_id
)
tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']

instances = ec2.describe_instances()
instance_id = instances['Reservations'][0]['Instances'][0]['InstanceId']

elbv2.register_targets(
    TargetGroupArn=tg_arn,
    Targets=[{'Id': instance_id}]
)

subnets = ec2.describe_subnets()
subnet_ids = [s['SubnetId'] for s in subnets['Subnets'][:2]]

sgs = ec2.describe_security_groups()
sg_id = sgs['SecurityGroups'][0]['GroupId']

alb_response = elbv2.create_load_balancer(
    Name='WebALB',
    Subnets=subnet_ids,
    SecurityGroups=[sg_id]
)
alb_arn = alb_response['LoadBalancers'][0]['LoadBalancerArn']

elbv2.create_listener(
    LoadBalancerArn=alb_arn,
    Protocol='HTTP',
    Port=80,
    DefaultActions=[{
        'Type': 'forward',
        'TargetGroupArn': tg_arn
    }]
)
