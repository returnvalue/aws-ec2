# Lab 3: EC2 Auto Scaling (Launch Templates & ASG)

**Goal:** Automate instance provisioning and ensure high availability by using Launch Templates and Auto Scaling Groups (ASG) to maintain a desired number of healthy instances across multiple AZs.

```bash
# 1. Create the Launch Template JSON payload
USER_DATA_B64=$(base64 < userdata.sh | tr -d '\n')
cat <<EOF > launch-template-data.json
{
  "ImageId": "$AMI_ID",
  "InstanceType": "t3.micro",
  "SecurityGroupIds": ["$SG_ID"],
  "UserData": "$USER_DATA_B64"
}
EOF

# 2. Create the Launch Template
LT_ID=$(awslocal ec2 create-launch-template \
  --launch-template-name WebServersLT \
  --launch-template-data file://launch-template-data.json \
  --query 'LaunchTemplate.LaunchTemplateId' --output text)

# 3. Create an Auto Scaling Group (Minimum 1, Desired 2, Maximum 4)
awslocal autoscaling create-auto-scaling-group \
  --auto-scaling-group-name WebASG \
  --launch-template LaunchTemplateId=$LT_ID,Version=1 \
  --min-size 1 --max-size 4 --desired-capacity 2 \
  --vpc-zone-identifier "$SUBNET_1,$SUBNET_2" \
  --target-group-arns $TG_ARN
```

## 🧠 Key Concepts & Importance

- **Launch Template:** A resource that contains the configuration information (AMI ID, instance type, security groups, user data) to launch an EC2 instance. It allows for versioning and reusability.
- **Auto Scaling Group (ASG):** A collection of EC2 instances that are treated as a logical grouping for the purposes of automatic scaling and management.
- **Self-Healing:** If an instance in the ASG becomes unhealthy or is terminated, the ASG automatically launches a new one to maintain the `Desired Capacity`.
- **Multi-AZ Availability:** By specifying multiple subnets (`VPC Zone Identifier`), the ASG will attempt to balance instances across Availability Zones for fault tolerance.
- **Scaling Policies:** (Optional) You can define policies to increase or decrease the number of instances based on metrics like CPU utilization or request count.
- **Integration with ALB:** The ASG automatically registers new instances with the specified Target Group, allowing the Load Balancer to immediately start routing traffic to them.

## 🛠️ Command Reference

- `awslocal ec2 create-launch-template`: Creates a template containing configuration information to launch an instance.
    - `--launch-template-name`: The name for the launch template.
    - `--launch-template-data`: The JSON file or string containing the configuration data.
- `awslocal autoscaling create-auto-scaling-group`: Creates an Auto Scaling group with specified capacity and networking.
    - `--auto-scaling-group-name`: The name of the ASG.
    - `--launch-template`: Specifies the ID and version of the launch template to use.
    - `--min-size`: The minimum number of instances in the group.
    - `--max-size`: The maximum number of instances in the group.
    - `--desired-capacity`: The initial number of instances to launch.
    - `--vpc-zone-identifier`: A comma-separated list of subnet IDs.
    - `--target-group-arns`: The ARN of the Target Group for integration with a Load Balancer.
