# Lab 5: Cost Optimization (Spot Instances)

**Goal:** Deploy a highly optimized compute instance for fault-tolerant batch processing using heavily discounted Spot instances, which can save up to 90% over On-Demand pricing.

```bash
# Request a Spot Instance for fault-tolerant workloads
awslocal ec2 run-instances \
  --image-id $AMI_ID \
  --instance-type c5.large \
  --subnet-id $SUBNET_1 \
  --instance-market-options '{"MarketType":"spot"}' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=BatchProcessorSpot}]' \
  --query 'Instances[0].InstanceId' --output text
aws ec2 run-instances \
  --image-id $AMI_ID \
  --instance-type c5.large \
  --subnet-id $SUBNET_1 \
  --instance-market-options '{"MarketType":"spot"}' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=BatchProcessorSpot}]' \
  --query 'Instances[0].InstanceId' --output text
```

## 🧠 Key Concepts & Importance

- **EC2 Spot Instances:** Allow you to take advantage of unused EC2 capacity in the AWS cloud. Spot instances are available at up to a 90% discount compared to On-Demand prices.
- **Interruptible Nature:** AWS can reclaim Spot instances with a two-minute notification if it needs the capacity back. This makes them ideal for workloads that are fault-tolerant, stateless, or flexible.
- **Ideal Use Cases:**
    - Batch processing and data analysis.
    - Containerized workloads (ECS/EKS).
    - High-performance computing (HPC).
    - CI/CD pipelines and testing environments.
- **Spot Price:** The price for a Spot instance fluctuates based on supply and demand for the instance type in the specific Availability Zone.
- **Market Options:** By specifying `MarketType: spot`, you tell AWS to provision the instance from the Spot pool rather than the On-Demand pool.

## 🛠️ Command Reference

- `ec2 run-instances`: Launches a new EC2 instance with specified parameters.
    - `--image-id`: The AMI ID to use.
    - `--instance-type`: The type of instance (e.g., `c5.large`).
    - `--subnet-id`: The subnet to launch into.
    - `--instance-market-options`: Specifies market options, such as `MarketType: spot` for discounted instances.
    - `--tag-specifications`: Adds tags to the instance at launch.
    - `--query`: Filters the output to return specific fields.
    - `--output`: Sets the output format (e.g., `text`).

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
