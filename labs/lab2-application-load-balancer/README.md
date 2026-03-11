# Lab 2: Layer 7 Application Load Balancer (ALB)

**Goal:** Distribute incoming HTTP traffic across multiple targets (starting with our single instance) using an Application Load Balancer (ALB).

```bash
# 1. Create a Target Group
TG_ARN=$(awslocal elbv2 create-target-group \
  --name WebTG \
  --protocol HTTP --port 80 \
  --vpc-id $VPC_ID \
  --query 'TargetGroups[0].TargetGroupArn' --output text)

# 2. Register our single instance to the Target Group
awslocal elbv2 register-targets \
  --target-group-arn $TG_ARN \
  --targets Id=$INSTANCE_ID

# 3. Create the Application Load Balancer across both subnets
ALB_ARN=$(awslocal elbv2 create-load-balancer \
  --name WebALB \
  --subnets $SUBNET_1 $SUBNET_2 \
  --security-groups $SG_ID \
  --query 'LoadBalancers[0].LoadBalancerArn' --output text)

# 4. Create a Listener to forward port 80 traffic to the Target Group
awslocal elbv2 create-listener \
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
