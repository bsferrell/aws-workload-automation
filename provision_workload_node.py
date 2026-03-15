import boto3
import os

def provision_compliant_ec2():
    print("Initiating strict-compliance EC2 provisioning sequence...")

    # Boto3 automatically looks for the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY 
    # environment variables in the background. No hardcoding required!
    ec2_client = boto3.client('ec2', region_name='us-east-1')

    # Standard Amazon Linux 2023 AMI (us-east-1)
    # In a real environment, this would be a hardened, company-approved image
    AMI_ID = 'ami-0c101f26f147fa7fd' 

    try:
        response = ec2_client.run_instances(
            ImageId=AMI_ID,
            InstanceType='t2.micro',
            SubnetId='subnet-05701ad464c56924c',  
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'Automated-Workload-Node'},
                        {'Key': 'Environment', 'Value': 'Production'},
                        {'Key': 'Owner', 'Value': 'Platform-Engineering'},
                        {'Key': 'CostCenter', 'Value': 'DevOps-010'},
                    ]
                }
            ]
        )
        
        instance_id = response['Instances'][0]['InstanceId']
        print(f"Success! EC2 Instance {instance_id} is booting up.")
        print("Required compliance and cost-tracking tags successfully applied.")
        
        return instance_id

    except Exception as e:
        print(f"Provisioning Failed: {e}")

if __name__ == "__main__":
    provision_compliant_ec2()