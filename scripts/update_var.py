import os

# 设置 var.sh 文件路径
var_file_path = './ansible/files/var.sh'

# 从环境变量获取 SCALE_FACTOR，默认为 100
scale_factor = os.getenv('SCALE_FACTOR', '100')

# 读取 var.sh 文件内容
with open(var_file_path, 'r') as file:
    lines = file.readlines()

# 更新 scaleFactor 行
with open(var_file_path, 'w') as file:
    for line in lines:
        if line.startswith('scaleFactor='):
            file.write(f'scaleFactor={scale_factor}\n')  # 用新的值替换
        else:
            file.write(line)

print(f'scaleFactor updated to {scale_factor} in {var_file_path}.')