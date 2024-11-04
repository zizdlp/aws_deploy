import boto3

def create_aws_instance(region,instance_type,instance_zone,ami,key_pair,security_group_id,subnet_id,instance_index,
                         runner,run_number,commit_hash):
    # 1.Initialize EC2 client
    ec2 = boto3.resource('ec2', region_name=region)

    # 2. set hostname
    user_data_script = '''#!/bin/bash
    # Set hostname
    hostnamectl set-hostname node{0}
    '''.format(instance_index)
    
    # 3. create instance
    instance = ec2.create_instances(
        ImageId=ami,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,            # Pass instance type from the command line
        KeyName=key_pair,                      # Your EC2 key pair
        SecurityGroupIds=[security_group_id],  # Replace with your security group ID
        SubnetId=subnet_id,                    # Replace with your subnet ID
        IamInstanceProfile={
            'Name': 's3_read_profile'          # 使用实例配置文件的名称
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
            'AvailabilityZone': instance_zone  # Choose availability zone 
        },
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                        {'Key': 'Name', 'Value': f'SparkNode-{run_number}-{commit_hash}-{runner}'},
                        {'Key': 'Index', 'Value': f'{instance_index}'}
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