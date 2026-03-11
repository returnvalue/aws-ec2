# AWS Elastic Compute Cloud (EC2) Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-EC2_Compute-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains hands-on labs demonstrating core Amazon EC2 concepts, from foundational networking and instance provisioning to high availability and automated scaling. Using [LocalStack Pro](https://localstack.cloud/), we simulate a complete AWS compute environment locally.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS best practices (SAA-C03), these labs cover:
* **Network Foundation:** Provisioning custom VPCs, public/private subnets, and internet gateways.
* **EC2 Provisioning:** Launching On-Demand instances with optimized AMI selection.
* **Security & Access:** Implementing stateful Security Groups and instance-level bootstrapping via User Data.
* **High Availability:** Designing for fault tolerance using Multi-AZ deployments.
* **Scaling & Load Balancing:** (Upcoming) Exploring Launch Templates, Auto Scaling Groups, and Elastic Load Balancers.
* **Cost Optimization:** (Upcoming) Leveraging Spot Instances and Savings Plans logic.

## ⚙️ Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & Docker Compose
* [LocalStack Pro](https://app.localstack.cloud/) account and Auth Token
* [`awslocal` CLI](https://github.com/localstack/awscli-local) (a wrapper around the AWS CLI for LocalStack)

## 🚀 Environment Setup

1. Configure your LocalStack Auth Token in `.env`:
   ```bash
   echo "YOUR_TOKEN=your_auth_token_here" > .env
   ```

2. Start LocalStack Pro:
   ```bash
   docker-compose up -d
   ```

> [!IMPORTANT]
> **Cumulative Architecture:** These labs are designed as a cumulative scenario. You are building an evolving infrastructure.
>
> **Session Persistence:** These labs rely on bash variables (like `$VPC_ID`, `$SG_ID`, `$AMI_ID`, etc.). Run all commands in the same terminal session to maintain context.

## 📚 Labs Index
1. [Lab 1: Network Foundation & EC2 Provisioning](./labs/lab1-network-foundation-ec2/README.md)
2. [Lab 2: Layer 7 Application Load Balancer (ALB)](./labs/lab2-application-load-balancer/README.md)
