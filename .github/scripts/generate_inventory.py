import json
import subprocess
import os
import time

# 确保 ~/.ssh 目录存在
ssh_dir = os.path.expanduser("~/.ssh")
os.makedirs(ssh_dir, exist_ok=True)

# 确保 known_hosts 文件存在
known_hosts_path = os.path.join(ssh_dir, "known_hosts")
if not os.path.exists(known_hosts_path):
    with open(known_hosts_path, 'w') as f:
        pass  # 创建空文件

# 读取节点信息
nodes_info = []
with open('./scripts/nodes_info.txt', 'r') as f:
    nodes_info = [line.strip() for line in f]
    print(f"nodes_info is: {nodes_info}")

# 查找 node0 作为 master 节点
master_node = next(node for node in nodes_info if node.startswith('node0'))

# 解析剩下的节点作为 worker 节点
worker_nodes = [node for node in nodes_info if not node.startswith('node0')]

# 获取 master 和 worker 的 DNS、Private IP 和 Public IP 信息
master_index, master_public_dns, master_private_ip, master_public_ip = master_node.split()
worker_details = [node.split() for node in worker_nodes]

# 生成 inventory.ini 文件内容
inventory_content = f"""[master]
node0

[worker]
"""
for worker in worker_details:
    index, worker_public_dns, _, worker_public_ip = worker
    inventory_content += f"{index}\n"

# 生成节点 Private IP 映射（nodes_ip_map 仍然保存 Private IP）
nodes_ip_map = {}
for node in nodes_info:
    index, _, private_ip, _ = node.split()  # 这里依旧存储的是 Private IP
    nodes_ip_map[f"{index}"] = private_ip

# 添加 [all:vars] 部分，包含节点 Private IP 映射变量
inventory_content += """
[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=/home/runner/.ssh/local_test.pem
nodes_ip_map='"""
# 将字典转换为 JSON 字符串
inventory_content += json.dumps(nodes_ip_map)
inventory_content += """'
"""

# 写入 inventory.ini 文件
with open('./ansible/inventory.ini', 'w') as f:
    f.write(inventory_content)

print('Inventory file has been generated at ./ansible/inventory.ini')

# 直接追加 Public IP 映射到 /etc/hosts
for node in nodes_info:
    index, _, _, public_ip = node.split()  # 使用 Public IP 追加到 /etc/hosts
    command = f"echo '{public_ip} {index}' | sudo tee -a /etc/hosts"
    try:
        subprocess.run(command, shell=True, check=True)
        print(f'Added {index} ({public_ip}) to /etc/hosts.')
    except subprocess.CalledProcessError as e:
        print(f'Error adding {index} to /etc/hosts: {e}')

print('/etc/hosts has been updated with node Public IP mappings.')

# 使用 ssh-keyscan 将节点主机名添加到 known_hosts
def add_to_known_hosts(hostname, retries=5, delay=5):
    for attempt in range(retries):
        try:
            # 执行 ssh-keyscan 命令并追加到 known_hosts 文件
            subprocess.run(f'ssh-keyscan -H {hostname} >> {known_hosts_path}', shell=True, check=True)
            print(f'Added {hostname} to known_hosts.')
            return  # 成功后退出函数
        except subprocess.CalledProcessError as e:
            print(f'Error adding {hostname} to known_hosts: {e}')
            if attempt < retries - 1:  # 如果不是最后一次尝试
                print(f'Retrying in {delay} seconds...')
                time.sleep(delay)  # 等待指定的时间后重试
    print(f'Failed to add {hostname} to known_hosts after {retries} attempts.')

# 遍历所有节点并添加到 known_hosts
for hostname in nodes_ip_map.keys():
    add_to_known_hosts(hostname)

print('All nodes (by hostname) have been added to ~/.ssh/known_hosts.')

# 生成 ./ansible/files/workers 文件
workers_file_path = './ansible/files/workers'

# 确保目标目录存在
os.makedirs(os.path.dirname(workers_file_path), exist_ok=True)

with open(workers_file_path, 'w') as workers_file:
    for i in range(1, len(worker_nodes) + 1):
        workers_file.write(f'node{i}\n')

print(f'Workers file has been generated at {workers_file_path}')