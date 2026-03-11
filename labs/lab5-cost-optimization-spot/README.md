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
