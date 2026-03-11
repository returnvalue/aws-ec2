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

- `awslocal autoscaling put-scaling-policy`: Adds or updates a scaling policy for an Auto Scaling group.
    - `--auto-scaling-group-name`: The name of the Auto Scaling group.
    - `--policy-name`: A descriptive name for the policy.
    - `--policy-type`: The type of scaling policy (e.g., `TargetTrackingScaling`).
    - `--target-tracking-configuration`: Specifies the metric and target value for the policy.
