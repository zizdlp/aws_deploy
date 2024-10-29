import boto3
import subprocess
import argparse
# 初始化 EC2 客户端
ec2 = boto3.client('ec2')

# 获取带有特定标签的实例
def get_instances_by_tag(tag_key, tag_value):
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

def get_commit_hash():
    # 获取当前 Git commit hash
    commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
    return commit_hash
def save_info(runner,run_number):
    # 获取标签键为 Name 且值完全匹配 SparkNode-{commit_hash} 的实例
    commit_hash = get_commit_hash()  # 获取当前 commit hash
    tag_value = f'SparkNode-{run_number}-{commit_hash}-{runner}'  # 定义要搜索的标签值
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


# Main function to parse command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='save node info')
    parser.add_argument('--runner', type=str, default='all', help='runner case for spark or ?')
    parser.add_argument('--run-number', type=str, default='0', help='github action run number')
    args = parser.parse_args()
    
    # Launch instances based on command line inputs
    save_info(args.runner,args.run_number)