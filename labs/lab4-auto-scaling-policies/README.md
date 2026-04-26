# Lab 4: Auto Scaling Policies (Target Tracking)

**Goal:** Implement dynamic scaling for our Auto Scaling Group using Target Tracking policies. This ensures that the fleet size adjusts automatically based on real-time metrics like CPU utilization.
```bash
# 1. Define the target tracking logic
cat <<EOF > scaling-policy.json
{
  "TargetValue": 50.0,
  "PredefinedMetricSpecification": {
    "PredefinedMetricType": "ASGAverageCPUUtilization"
  }
}
EOF

# 2. Attach the scaling policy to the Auto Scaling Group
awslocal autoscaling put-scaling-policy \
  --auto-scaling-group-name WebASG \
  --policy-name CPU-Target-Tracking \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration file://scaling-policy.json
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name WebASG \
  --policy-name CPU-Target-Tracking \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration file://scaling-policy.json
```

## 🧠 Key Concepts & Importance

- **Dynamic Scaling:** Unlike manual scaling, dynamic scaling automatically changes the number of EC2 instances in your ASG based on actual load.
- **Target Tracking Scaling:** This is similar to a thermostat; you choose a metric (like average CPU) and set a target value (like 50%). AWS handles the math to add or remove instances to keep the metric at that target.
- **Predefined Metrics:** AWS provides standard metrics for ASGs, including:
    - `ASGAverageCPUUtilization`
    - `ASGAverageNetworkIn`
    - `ASGAverageNetworkOut`
    - `ALBRequestCountPerTarget`
- **Cooldown Periods:** Helps prevent the ASG from launching or terminating additional instances before the previous scaling activity takes effect, avoiding "flapping."
- **Cost vs. Performance:** Target tracking ensures you have enough capacity for peak demand while saving costs by scaling down during low-traffic periods.

## 🛠️ Command Reference

- `autoscaling put-scaling-policy`: Adds or updates a scaling policy for an Auto Scaling group.
    - `--auto-scaling-group-name`: The name of the Auto Scaling group.
    - `--policy-name`: A descriptive name for the policy.
    - `--policy-type`: The type of scaling policy (e.g., `TargetTrackingScaling`).
    - `--target-tracking-configuration`: Specifies the metric and target value for the policy.

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
