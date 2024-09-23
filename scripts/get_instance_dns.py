import boto3
import subprocess

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

# 获取标签键为 Name 且值完全匹配 SparkNode-{commit_hash} 的实例
commit_hash = get_commit_hash()  # 获取当前 commit hash
tag_value = f'SparkNode-{commit_hash}'  # 定义要搜索的标签值
instances = get_instances_by_tag('Name', tag_value)

# 保存节点信息到一个文件
with open('./scripts/nodes_info.txt', 'w') as f:
    for instance in instances:
        # 查找标签中的 Index
        tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
        index = tags.get('Index', 'unknown')

        # 提取 Public DNS 和 Private IP
        public_dns = instance.get('PublicDnsName', 'No Public DNS assigned')
        private_ip = instance.get('PrivateIpAddress', 'No Private IP assigned')

        # 保存节点信息到文件，每一行格式为：node{index} {Public DNS} {Private IP}
        f.write(f'node{index} {public_dns} {private_ip}\n')

print('Node information has been saved to ./scripts/nodes_info.txt')