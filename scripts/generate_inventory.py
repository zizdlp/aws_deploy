import json
import subprocess

# 读取节点信息
nodes_info = []
with open('./scripts/nodes_info.txt', 'r') as f:
    nodes_info = [line.strip() for line in f]

# 查找 node0 作为 master 节点
master_node = next(node for node in nodes_info if node.startswith('node0'))

# 解析剩下的节点作为 worker 节点
worker_nodes = [node for node in nodes_info if not node.startswith('node0')]

# 获取 master 和 worker 的 DNS 和 IP 信息
master_index, master_public_dns, master_private_ip = master_node.split()
worker_details = [node.split() for node in worker_nodes]

# 生成 inventory.ini 文件内容
inventory_content = f"""[master]
{master_public_dns}

[worker]
"""
for worker in worker_details:
    _, worker_public_dns, _ = worker
    inventory_content += f"{worker_public_dns}\n"

# 生成节点 IP 映射
nodes_ip_map = {}
for node in nodes_info:
    index, _, private_ip = node.split()
    nodes_ip_map[f"{index}"] = private_ip

# 添加 [all:vars] 部分，包含节点 IP 映射变量
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



# 直接追加 IP 映射到 /etc/hosts

# 直接使用 subprocess 调用 sudo 来修改 /etc/hosts
for index, private_ip in nodes_ip_map.items():
    command = f"echo '{private_ip} {index}' | sudo tee -a /etc/hosts"
    try:
        subprocess.run(command, shell=True, check=True)
        print(f'Added {index} ({private_ip}) to /etc/hosts.')
    except subprocess.CalledProcessError as e:
        print(f'Error adding {index} to /etc/hosts: {e}')
        
print('/etc/hosts has been updated with node IP mappings.')

for hostname in nodes_ip_map.keys():
    try:
        # 执行 ssh-keyscan 命令并追加到 known_hosts 文件
        subprocess.run(f'ssh-keyscan -H {hostname} >> ~/.ssh/known_hosts', shell=True, check=True)
        print(f'Added {hostname} to known_hosts.')
    except subprocess.CalledProcessError as e:
        print(f'Error adding {hostname} to known_hosts: {e}')

print('All nodes (by hostname) have been added to ~/.ssh/known_hosts.')