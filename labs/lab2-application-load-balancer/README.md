# Lab 2: Layer 7 Application Load Balancer (ALB)

**Goal:** Distribute incoming HTTP traffic across multiple targets (starting with our single instance) using an Application Load Balancer (ALB).

```bash
# 1. Create a Target Group
TG_ARN=$(awslocal elbv2 create-target-group \
  --name WebTG \
  --protocol HTTP --port 80 \
  --vpc-id $VPC_ID \
  --query 'TargetGroups[0].TargetGroupArn' --output text)
TG_ARN=$(aws elbv2 create-target-group \
  --name WebTG \
  --protocol HTTP --port 80 \
  --vpc-id $VPC_ID \
  --query 'TargetGroups[0].TargetGroupArn' --output text)

# 2. Register our single instance to the Target Group
awslocal elbv2 register-targets \
  --target-group-arn $TG_ARN \
  --targets Id=$INSTANCE_ID
aws elbv2 register-targets \
  --target-group-arn $TG_ARN \
  --targets Id=$INSTANCE_ID

# 3. Create the Application Load Balancer across both subnets
ALB_ARN=$(awslocal elbv2 create-load-balancer \
  --name WebALB \
  --subnets $SUBNET_1 $SUBNET_2 \
  --security-groups $SG_ID \
  --query 'LoadBalancers[0].LoadBalancerArn' --output text)
ALB_ARN=$(aws elbv2 create-load-balancer \
  --name WebALB \
  --subnets $SUBNET_1 $SUBNET_2 \
  --security-groups $SG_ID \
  --query 'LoadBalancers[0].LoadBalancerArn' --output text)

# 4. Create a Listener to forward port 80 traffic to the Target Group
awslocal elbv2 create-listener \
  --load-balancer-arn $ALB_ARN \
  --protocol HTTP --port 80 \
  --default-actions Type=forward,TargetGroupArn=$TG_ARN
aws elbv2 create-listener \
  --load-balancer-arn $ALB_ARN \
  --protocol HTTP --port 80 \
  --default-actions Type=forward,TargetGroupArn=$TG_ARN
```

## 🧠 Key Concepts & Importance

- **Application Load Balancer (ALB):** Operates at Layer 7 (Application layer) of the OSI model. It is ideal for advanced load balancing of HTTP and HTTPS traffic, providing advanced routing features.
- **Target Group:** Used to route requests to one or more registered targets, such as EC2 instances. You can configure health checks for these targets.
- **Listeners:** A process that checks for connection requests using the protocol and port you configure. The rules that you define for a listener determine how the load balancer routes requests to its registered targets.
- **Cross-Zone Load Balancing:** ALBs are inherently cross-zone, meaning they can distribute traffic to targets in all enabled Availability Zones.
- **High Availability:** By placing the ALB across multiple subnets (Multi-AZ), we ensure the entry point for our application remains available even if one AZ fails.

## 🛠️ Command Reference

- `elbv2 create-target-group`: Creates a target group for routing requests to registered targets.
    - `--name`: The name of the target group.
    - `--protocol`: The protocol to use (e.g., `HTTP`).
    - `--port`: The port to listen on (e.g., `80`).
    - `--vpc-id`: The VPC in which to create the target group.
- `elbv2 register-targets`: Registers one or more targets (instances) with a target group.
    - `--target-group-arn`: The ARN of the target group.
    - `--targets`: The ID(s) of the targets to register.
- `elbv2 create-load-balancer`: Creates an Application Load Balancer.
    - `--name`: The name of the load balancer.
    - `--subnets`: The subnets to associate with the load balancer.
    - `--security-groups`: The security groups to associate with the load balancer.
- `elbv2 create-listener`: Creates a listener for the load balancer to forward traffic.
    - `--load-balancer-arn`: The ARN of the load balancer.
    - `--protocol`: The protocol for the listener.
    - `--port`: The port for the listener.
    - `--default-actions`: The action to take (e.g., `forward` to a target group).

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
