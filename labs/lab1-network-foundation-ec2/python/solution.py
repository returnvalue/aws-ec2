import boto3

ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

vpc_response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = vpc_response['Vpc']['VpcId']

subnet1_response = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24', AvailabilityZone='us-east-1a')
subnet1_id = subnet1_response['Subnet']['SubnetId']

subnet2_response = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.2.0/24', AvailabilityZone='us-east-1b')
subnet2_id = subnet2_response['Subnet']['SubnetId']

igw_response = ec2.create_internet_gateway()
igw_id = igw_response['InternetGateway']['InternetGatewayId']

ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=igw_id)

rt_response = ec2.create_route_table(VpcId=vpc_id)
rt_id = rt_response['RouteTable']['RouteTableId']

ec2.create_route(RouteTableId=rt_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)

ec2.associate_route_table(SubnetId=subnet1_id, RouteTableId=rt_id)
ec2.associate_route_table(SubnetId=subnet2_id, RouteTableId=rt_id)

sg_response = ec2.create_security_group(GroupName='WebSG', Description='Allow HTTP', VpcId=vpc_id)
sg_id = sg_response['GroupId']

ec2.authorize_security_group_ingress(GroupId=sg_id, IpProtocol='tcp', FromPort=80, ToPort=80, CidrIp='0.0.0.0/0')

images = ec2.describe_images()
ami_id = images['Images'][0]['ImageId']

user_data = '''#!/bin/bash
echo "Hello from LocalStack Web Server!" > index.html
python3 -m http.server 80 &
'''

instance_response = ec2.run_instances(
    ImageId=ami_id,
    InstanceType='t3.micro',
    SecurityGroupIds=[sg_id],
    SubnetId=subnet1_id,
    UserData=user_data,
    MinCount=1,
    MaxCount=1
)
instance_id = instance_response['Instances'][0]['InstanceId']
