import boto3

autoscaling = boto3.client('autoscaling', endpoint_url="http://localhost:4566", region_name="us-east-1")

autoscaling.put_scaling_policy(
    AutoScalingGroupName='WebASG',
    PolicyName='CPU-Target-Tracking',
    PolicyType='TargetTrackingScaling',
    TargetTrackingConfiguration={
        'TargetValue': 50.0,
        'PredefinedMetricSpecification': {
            'PredefinedMetricType': 'ASGAverageCPUUtilization'
        }
    }
)
