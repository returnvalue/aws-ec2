import boto3

ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

images = ec2.describe_images()
ami_id = images['Images'][0]['ImageId']

subnets = ec2.describe_subnets()
subnet_id = subnets['Subnets'][0]['SubnetId']

ec2.run_instances(
    ImageId=ami_id,
    InstanceType='c5.large',
    SubnetId=subnet_id,
    MinCount=1,
    MaxCount=1,
    InstanceMarketOptions={
        'MarketType': 'spot'
    },
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'BatchProcessorSpot'}]
        }
    ]
)
