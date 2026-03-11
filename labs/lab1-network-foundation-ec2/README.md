# Lab 1: Network Foundation & EC2 Provisioning

**Goal:** Create a highly available network foundation (VPC, Subnets, Internet Gateway) and launch an EC2 instance with an automated web server bootstrap using User Data.

```bash
# 1. Create a VPC and two Subnets for High Availability
VPC_ID=$(awslocal ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
SUBNET_1=$(awslocal ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --query 'Subnet.SubnetId' --output text)
SUBNET_2=$(awslocal ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 --availability-zone us-east-1b --query 'Subnet.SubnetId' --output text)

# 2. Add an Internet Gateway and configure routing
IGW_ID=$(awslocal ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
awslocal ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID
RT_ID=$(awslocal ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)
awslocal ec2 create-route --route-table-id $RT_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID
awslocal ec2 associate-route-table --subnet-id $SUBNET_1 --route-table-id $RT_ID
awslocal ec2 associate-route-table --subnet-id $SUBNET_2 --route-table-id $RT_ID

# 3. Create a Security Group to allow HTTP traffic
SG_ID=$(awslocal ec2 create-security-group --group-name WebSG --description "Allow HTTP" --vpc-id $VPC_ID --query 'GroupId' --output text)
awslocal ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0

# 4. Fetch a valid AMI ID and launch an initial On-Demand EC2 instance
AMI_ID=$(awslocal ec2 describe-images --query 'Images[0].ImageId' --output text)
echo "Using AMI: $AMI_ID"

cat <<EOF > userdata.sh
#!/bin/bash
echo "Hello from LocalStack Web Server!" > index.html
python3 -m http.server 80 &
EOF

INSTANCE_ID=$(awslocal ec2 run-instances \
  --image-id $AMI_ID \
  --instance-type t3.micro \
  --security-group-ids $SG_ID \
  --subnet-id $SUBNET_1 \
  --user-data file://userdata.sh \
  --query 'Instances[0].InstanceId' --output text)
```

## 🧠 Key Concepts & Importance

- **High Availability (Multi-AZ):** By creating subnets in different Availability Zones (`us-east-1a` and `us-east-1b`), we prepare the infrastructure for fault tolerance.
- **Internet Gateway (IGW):** Provides a target in your VPC route tables for internet-routable traffic and performs network address translation (NAT) for instances that have been assigned public IPv4 addresses.
- **Security Groups:** Act as a virtual firewall for your EC2 instances to control incoming and outgoing traffic. They are **stateful** (if you send a request from your instance, the response traffic is allowed to flow in regardless of inbound security group rules).
- **User Data:** A script that runs once when the instance is first launched. This is used for **bootstrapping** applications (installing updates, packages, or configuring services).
- **AMI (Amazon Machine Image):** Provides the information required to launch an instance. You must specify an AMI when you launch an instance.

## 🛠️ Command Reference

- `ec2 create-vpc`: Creates a Virtual Private Cloud with a specified CIDR block.
    - `--cidr-block`: The IP range for the VPC.
- `ec2 create-subnet`: Creates a subnet within a VPC in a specific Availability Zone.
    - `--vpc-id`: The VPC to associate with the subnet.
    - `--cidr-block`: The IP range for the subnet.
    - `--availability-zone`: The AZ for the subnet.
- `ec2 create-internet-gateway`: Creates an Internet Gateway for VPC internet access.
- `ec2 attach-internet-gateway`: Attaches an Internet Gateway to a VPC.
- `ec2 create-route-table`: Creates a route table for a VPC.
- `ec2 create-route`: Adds a route to a route table (e.g., a default route to an IGW).
    - `--destination-cidr-block`: The destination traffic range (e.g., `0.0.0.0/0`).
    - `--gateway-id`: The ID of the gateway to route traffic through.
- `ec2 associate-route-table`: Associates a route table with a subnet.
- `ec2 create-security-group`: Creates a security group to control traffic.
    - `--group-name`: The name of the security group.
    - `--description`: A brief description of the security group.
- `ec2 authorize-security-group-ingress`: Adds an inbound rule to a security group.
    - `--protocol`: The network protocol (e.g., `tcp`).
    - `--port`: The destination port (e.g., `80`).
    - `--cidr`: The source IP range allowed.
- `ec2 describe-images`: Lists available AMIs based on filters.
- `ec2 run-instances`: Launches a new EC2 instance with specified parameters.
    - `--user-data`: A script to run on instance launch.
