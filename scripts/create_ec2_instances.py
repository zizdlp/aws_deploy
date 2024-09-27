import boto3
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize EC2 client
ec2 = boto3.resource('ec2', region_name='cn-northwest-1')

def get_commit_hash():
    # Get the current Git commit hash
    commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
    return commit_hash

def create_instance(index):
    commit_hash = get_commit_hash()  # Get current commit hash

    user_data_script = '''#!/bin/bash
    # Set hostname
    hostnamectl set-hostname node{0}
    '''.format(index)
    
    instance = ec2.create_instances(
        ImageId='ami-063dbdfa885edce48',  # Replace with your AMI ID
        MinCount=1,
        MaxCount=1,
        InstanceType='i4i.4xlarge',  # Choose instance type
        KeyName='local_test',  # Your EC2 key pair
        SecurityGroupIds=['sg-01afc3b646b79f84b'],  # Replace with your security group ID
        # SubnetId='subnet-0b387a115a4176faa',  # Replace with your subnet ID
        IamInstanceProfile={
            'Name': 's3_read'  # Replace with your IAM role name
        },
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sda1',  # Root volume
                'Ebs': {
                    'VolumeSize': 100,  # Size in GiB
                    'VolumeType': 'gp3',  # Volume type
                    'DeleteOnTermination': True  # Delete volume on instance termination
                }
            }
        ],
        # Placement={
        #     'AvailabilityZone': 'cn-northwest-1c'  # Choose availability zone
        # },
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                        {'Key': 'Name', 'Value': f'SparkNode-{commit_hash}'},
                        {'Key': 'Index', 'Value': f'{index}'}
                         ]
            }
        ],
        UserData=user_data_script  # Add UserData script to set hostname
    )[0]
    
    # Wait for the instance to be running
    instance.wait_until_running()
    
    # Reload the instance to get updated information
    instance.reload()
    
    return instance

# Function to manage parallel instance creation
def parallel_create_instances(num_instances):
    instances = []
    with ThreadPoolExecutor(max_workers=num_instances) as executor:
        # Submit tasks for parallel execution
        future_to_index = {executor.submit(create_instance, index): index for index in range(num_instances)}
        
        # Process results as they complete
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                instance = future.result()
                instances.append(instance)
                print(f'Instance {instance.id} launched as node{index}. Public DNS: {instance.public_dns_name}')
            except Exception as e:
                print(f'Error launching instance {index}: {e}')
    
    return instances

# Launch 4 instances in parallel
instances = parallel_create_instances(4)