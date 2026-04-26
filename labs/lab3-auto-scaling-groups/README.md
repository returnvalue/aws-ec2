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
LT_ID=$(aws ec2 create-launch-template \
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
aws autoscaling create-auto-scaling-group \
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

- `ec2 create-launch-template`: Creates a template containing configuration information to launch an instance.
    - `--launch-template-name`: The name for the launch template.
    - `--launch-template-data`: The JSON file or string containing the configuration data.
- `autoscaling create-auto-scaling-group`: Creates an Auto Scaling group with specified capacity and networking.
    - `--auto-scaling-group-name`: The name of the ASG.
    - `--launch-template`: Specifies the ID and version of the launch template to use.
    - `--min-size`: The minimum number of instances in the group.
    - `--max-size`: The maximum number of instances in the group.
    - `--desired-capacity`: The initial number of instances to launch.
    - `--vpc-zone-identifier`: A comma-separated list of subnet IDs.
    - `--target-group-arns`: The ARN of the Target Group for integration with a Load Balancer.

---

💡 **Pro Tip: Using `aws` instead of `awslocal`**

If you prefer using the standard `aws` CLI without the `awslocal` wrapper or repeating the `--endpoint-url` flag, you can configure a dedicated profile in your AWS config files.

### 1. Configure your Profile
Add the following to your `~/.aws/config` file:
```ini
[profile localstack]
region = us-east-1
output = json
# This line redirects all commands for this profile to LocalStack
endpoint_url = http://localhost:4566
```

Add matching dummy credentials to your `~/.aws/credentials` file:
```ini
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```

### 2. Use it in your Terminal
You can now run commands in two ways:

**Option A: Pass the profile flag**
```bash
aws iam create-user --user-name DevUser --profile localstack
```

**Option B: Set an environment variable (Recommended)**
Set your profile once in your session, and all subsequent `aws` commands will automatically target LocalStack:
```bash
export AWS_PROFILE=localstack
aws iam create-user --user-name DevUser
```

### Why this works
- **Precedence**: The AWS CLI (v2) supports a global `endpoint_url` setting within a profile. When this is set, the CLI automatically redirects all API calls for that profile to your local container instead of the real AWS cloud.
- **Convenience**: This allows you to use the standard documentation commands exactly as written, which is helpful if you are copy-pasting examples from AWS labs or tutorials.
