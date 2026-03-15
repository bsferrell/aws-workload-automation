import boto3

def terminate_workloads():
    print("Initiating automated workload termination sequence...")

    ec2_client = boto3.client('ec2', region_name='us-east-1')
    
    # We don't hardcode Instance IDs. We dynamically search for the tags!
    target_tags = [
        {'Name': 'tag:Environment', 'Values': ['Production']},
        {'Name': 'instance-state-name', 'Values': ['stopped', 'running']}
    ]
    
    try:
        # Step 1: Find all running instances with the Production tag
        response = ec2_client.describe_instances(Filters=target_tags)

        instances_to_terminate = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances_to_terminate.append(instance['InstanceId'])

        # Step 2: Stop them if any are found
        if instances_to_terminate:
            print(f"Found {len(instances_to_terminate)} production workloads. Issuing terminate command...")
            ec2_client.terminate_instances(InstanceIds=instances_to_terminate)
            for i_id in instances_to_terminate:
                print(f"Successfully triggered termination for: {i_id}")
        else:
            print("No production workloads found. Cost compliance maintained.")
            
    except Exception as e:
        print(f"Automation Failed: {e}")

if __name__ == "__main__":
    terminate_workloads()