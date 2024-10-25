import boto3
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
def get_commit_hash():
    # 使用 subprocess 来获取当前 Git commit hash
    commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
    return commit_hash

def terminate_instance(instance):
    # 终止指定实例并等待终止完成
    instance.terminate()
    print(f'Terminating instance {instance.id}')
    instance.wait_until_terminated()
    print(f'Instance {instance.id} has been terminated.')
    return instance.id

def terminate_instances(runner,spark,chukonu):
    if runner=="chukonu" and chukonu!='0':
        print("not run instances for chukonu")
        return
    elif runner=="spark" and spark!='0':
        print("not run instances for spark")
        return
    commit_hash = get_commit_hash()  # 获取当前 commit hash
    ec2 = boto3.resource('ec2', region_name='cn-northwest-1')
    
    # 根据标签过滤实例
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': [f'SparkNode-{commit_hash}-{runner}']}]
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



# Main function to parse command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Terminate instances.')
    parser.add_argument('--runner', type=str, default='all', help='runner case for spark or ?')
    parser.add_argument('--spark', type=str, default='0', help='runn spark')
    parser.add_argument('--chukonu', type=str, default='0', help='run chukonu')

    args = parser.parse_args()
    terminate_instances(args.runner,args.spark,args.chukonu)