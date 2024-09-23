import boto3
import subprocess
def get_commit_hash():
    # 使用 subprocess 来获取当前 Git commit hash
    commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
    return commit_hash
def terminate_instances():
    commit_hash = get_commit_hash()  # 获取当前 commit hash
    ec2 = boto3.resource('ec2', region_name='cn-northwest-1')
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': [f'SparkNode-{commit_hash}']}]
    )
    for instance in instances:
        instance.terminate()
        print(f'Terminating instance {instance.id}')
        instance.wait_until_terminated()
        print(f'Instance {instance.id} has been terminated.')

terminate_instances()