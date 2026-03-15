# Automated AWS Workload Scheduling & Compliance Pipeline

## Executive Summary
An event-driven Infrastructure as Code (IaC) pipeline designed to provision AWS EC2 compute resources while strictly enforcing the AWS Well-Architected Framework's pillars of Security and Cost Optimization. 

This project demonstrates the ability to execute end-to-end cloud administration tasks, replacing manual console operations with automated, Python-based pipeline stages.

## Core Technologies
*  AWS (EC2, IAM, VPC)
*  Python 3.11 (`boto3`)
*  GitLab CI
*  Git

## Security & Compliance Features
* **No Hardcoded Secrets:** AWS authentication is handled dynamically via secure CI/CD environment variables.
* **Least Privilege IAM:** Custom JSON policies restrict the deployment pipeline strictly to EC2 provisioning and EventBridge scheduling. Role-passing is restricted using `iam:PassedToService` condition keys to prevent privilege escalation.
* **Mandatory Tagging:** Resources are automatically tagged upon creation (`Environment`, `Owner`, `CostCenter`) to ensure strict financial tracking and resource governance.

## Pipeline Architecture (The "Tivoli/IWS" Alternative)
This repository replaces traditional manual scheduling with a 3-stage GitLab CI/CD pipeline:

1. **`provision` (Manual Trigged Cron):** to deploy a compliant EC2 instance into a designated VPC subnet.
2. **`stop` Executes `stop_workloads.py` nightly. It queries the AWS API for any instances tagged `Environment: Production` and shuts them down to eliminate off-hour compute waste.
3. **`cleanup` (Manual Trigger):** Executes `terminate_workload.py` to destroy ephemeral environments, ensuring zero orphaned resources and a minimized attack surface.

## How to Run Locally
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Export your AWS CLI credentials to your terminal session.
4. Execute individual stages: `python scripts/provision_workload.py`