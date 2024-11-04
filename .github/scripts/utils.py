import boto3
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
def get_commit_hash():
    # Get the current Git commit hash
    commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
    return commit_hash
def create_aws_instance(instance_index,region,instance_type,instance_zone,ami,key_pair,security_group_id,subnet_id,
                        use_nvme,run_number,run_type):
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
        BlockDeviceMappings= [
            {
                'DeviceName': '/dev/sda1',  # Root volume
                'Ebs': {
                    'VolumeSize': 300,  # Size in GiB
                    'VolumeType': 'gp3',  # Volume type
                    'DeleteOnTermination': True  # Delete volume on instance termination
                }
            }
        ] if use_nvme else [],
        Placement={
            'AvailabilityZone': instance_zone  # Choose availability zone 
        },
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                        {'Key': 'Name', 'Value': f'{run_number}-{run_type}-{get_commit_hash()}'},
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


def parallel_create_instances(num_instances,region,instance_type,instance_zone,ami,key_pair,security_group_id,subnet_id,
                        use_nvme,run_number,run_type):
    instances = []
    with ThreadPoolExecutor(max_workers=num_instances) as executor:
        # Submit tasks for parallel execution
        future_to_index = {executor.submit(create_aws_instance,instance_index,region,instance_type,instance_zone,ami,key_pair,security_group_id,subnet_id,
                        use_nvme,run_number,run_type): instance_index for instance_index in range(num_instances)}
        
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

def get_instances_by_tag(tag_key, tag_value):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': f'tag:{tag_key}',
                'Values': [tag_value]
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    # 返回所有符合条件的实例
    instances = [i for r in response['Reservations'] for i in r['Instances']]
    return instances

def save_info(run_type,run_number):
    tag_value = f'{run_number}-{run_type}-{get_commit_hash()}'
    instances = get_instances_by_tag('Name', tag_value)

    # 保存节点信息到一个文件，包含 Public IP 地址
    with open('./.github/scripts/nodes_info.txt', 'w') as f:
        for instance in instances:
            # 查找标签中的 Index
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            index = tags.get('Index', 'unknown')

            # 提取 Public DNS、Private IP 和 Public IP
            public_dns = instance.get('PublicDnsName', 'No Public DNS assigned')
            private_ip = instance.get('PrivateIpAddress', 'No Private IP assigned')
            public_ip = instance.get('PublicIpAddress', 'No Public IP assigned')

            # 保存节点信息到文件，每一行格式为：node{index} {Public DNS} {Private IP} {Public IP}
            f.write(f'node{index} {public_dns} {private_ip} {public_ip}\n')

    print('Node information with Public IPs has been saved to ./.github/scripts/nodes_info.txt')



def terminate_instance(instance):
    # 终止指定实例并等待终止完成
    instance.terminate()
    print(f'Terminating instance {instance.id}')
    instance.wait_until_terminated()
    print(f'Instance {instance.id} has been terminated.')
    return instance.id

def terminate_instances(region,run_type,run_number):
    ec2 = boto3.resource('ec2', region_name=region)
    
    # 根据标签过滤实例
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': [f'{run_number}-{run_type}-{get_commit_hash()}']}]
    )

    instance_list = list(instances)  # 转换为列表以便并行处理

    if not instance_list:
        print("No instances found with the specified tag.")
        return
    
    # 使用 ThreadPoolExecutor 并行终止实例
    with ThreadPoolExecutor(max_workers=len(instance_list)) as executor:
        futures = [executor.submit(terminate_instance, instance) for instance in instance_list]
        
        # 处理每个完成的任务
        for future in as_completed(futures):
            try:
                instance_id = future.result()
                print(f'Instance {instance_id} has been successfully terminated.')
            except Exception as e:
                print(f'Error terminating instance: {e}')

