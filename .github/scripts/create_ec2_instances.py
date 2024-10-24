import boto3
import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize EC2 client
ec2 = boto3.resource('ec2', region_name='cn-northwest-1')

def get_commit_hash():
    # Get the current Git commit hash
    commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
    return commit_hash

def create_instance(index, instance_type,runner):
    commit_hash = get_commit_hash()  # Get current commit hash

    user_data_script = '''#!/bin/bash
    # Set hostname
    hostnamectl set-hostname node{0}
    '''.format(index)
    
    instance = ec2.create_instances(
        ImageId='ami-063dbdfa885edce48',  # Replace with your AMI ID:'ami-092169ca69a0bfc8a'
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,  # Pass instance type from the command line
        KeyName='local_test',  # Your EC2 key pair
        SecurityGroupIds=['sg-01afc3b646b79f84b'],  # Replace with your security group ID
        SubnetId='subnet-09117acf49a3d9a6b',  # Replace with your subnet ID
        IamInstanceProfile={
            'Name': 's3_read'  # Replace with your IAM role name
        },
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sda1',  # Root volume
                'Ebs': {
                    'VolumeSize': 300,  # Size in GiB
                    'VolumeType': 'gp3',  # Volume type
                    'DeleteOnTermination': True  # Delete volume on instance termination
                }
            }
        ],
        Placement={
            'AvailabilityZone': 'cn-northwest-1a'  # Choose availability zone
        },
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                        {'Key': 'Name', 'Value': f'SparkNode-{commit_hash}-{runner}'},
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
def parallel_create_instances(num_instances, instance_type,runner):
    instances = []
    with ThreadPoolExecutor(max_workers=num_instances) as executor:
        # Submit tasks for parallel execution
        future_to_index = {executor.submit(create_instance, index, instance_type,runner): index for index in range(num_instances)}
        
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

# Main function to parse command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch EC2 instances.')
    parser.add_argument('--num-instances', type=int, default=4, help='Number of instances to launch')
    parser.add_argument('--instance-type', type=str, default='i4i.4xlarge', help='EC2 instance type')
    parser.add_argument('--runner', type=str, default='all', help='runner case for spark or ?')
    
    args = parser.parse_args()
    
    # Launch instances based on command line inputs
    instances = parallel_create_instances(args.num_instances, args.instance_type,args.runner)