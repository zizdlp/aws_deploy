import json

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

# 添加 [all:vars] 部分，包含节点 IP 映射变量和 SSH 密钥
inventory_content += """
[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=/home/runner/.ssh/local_test.pem
nodes_ip_map='"""
# 将字典转换为 JSON 字符串
inventory_content += json.dumps(nodes_ip_map)
inventory_content += """'"""


# 写入 inventory.ini 文件
with open('./ansible/inventory.ini', 'w') as f:
    f.write(inventory_content)

print('Inventory file has been generated at ./ansible/inventory.ini')