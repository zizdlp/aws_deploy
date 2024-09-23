import boto3
import subprocess

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
        InstanceType='c5d.2xlarge',  # Choose instance type
        KeyName='local_test',  # Your EC2 key pair
        SecurityGroupIds=['sg-01afc3b646b79f84b'],  # Replace with your security group ID
        SubnetId='subnet-050fe41bd0d816003',  # Replace with your subnet ID
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
        Placement={
            'AvailabilityZone': 'cn-northwest-1b'  # Choose availability zone
        },
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

instances = []
for index in range(4):
    instance = create_instance(index)
    instances.append(instance)

# Print EC2 instance IDs and public DNS
for instance in instances:
    print(f'Instance {instance.id} launched as node{instance.id[-1]}. Public DNS: {instance.public_dns_name}')