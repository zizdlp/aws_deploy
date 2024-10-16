import os
import xml.etree.ElementTree as ET
# 定义要替换的变量及其默认值
variables = {
    "scaleFactor": os.environ.get("SCALE_FACTOR", 100),  # 从环境变量中获取
    "spark_numexecutors": os.environ.get("SPARK_NUM_EXECUTORS", 3),
    "spark_executorcores": os.environ.get("SPARK_EXECUTOR_CORES", 12),
    "spark_executormemory": os.environ.get("SPARK_EXECUTOR_MEMORY", "90g"),
    "spark_offsize": os.environ.get("SPARK_OFFSIZE", "0g"),
    "spark_overhead": os.environ.get("SPARK_OVERHEAD", "6g"),
    "chukonu_numexecutors": os.environ.get("CHUKONU_NUM_EXECUTORS", 3),
    "chukonu_executorcores": os.environ.get("CHUKONU_EXECUTOR_CORES", 12),
    "chukonu_executormemory": os.environ.get("CHUKONU_EXECUTOR_MEMORY", "47g"),
    "chukonu_offsize": os.environ.get("CHUKONU_OFFSIZE", "1g"),
    "chukonu_overhead": os.environ.get("CHUKONU_OVERHEAD", "48g"),
}

# 更新 var.sh 文件
var_file_path = './ansible/files/var.sh'

with open(var_file_path, 'w') as var_file:
    for var_name, var_value in variables.items():
        var_file.write(f"{var_name}={var_value}\n")
        print(f'Updated {var_name} to {var_value} in {var_file_path}.')
print(f'Updated {var_file_path} with dynamic variables.')


# 定义要替换的属性及其默认值
yarn_config_updates = {
    "yarn.nodemanager.resource.memory-mb": os.environ.get("NODEMANAGER_MEMORY_MB", 102400),
    "yarn.scheduler.maximum-allocation-mb": os.environ.get("MAXIMUM_ALLOCATION_MB", 307200),
    "yarn.scheduler.minimum-allocation-mb": os.environ.get("MINIMUM_ALLOCATION_MB", 2048),
    "yarn.scheduler.maximum-allocation-vcores": os.environ.get("MAXIMUM_ALLOCATION_VCORES", 45),
}

# 更新 yarn-site.xml 文件
yarn_file_path = './ansible/files/yarn-site.xml'

# 解析 XML 文件
tree = ET.parse(yarn_file_path)
root = tree.getroot()

# 更新指定的属性
for property_name, property_value in yarn_config_updates.items():
    for prop in root.findall('property'):
        name = prop.find('name').text
        if name == property_name:
            prop.find('value').text = str(property_value)
            print(f'Updated {property_name} to {property_value} in {yarn_file_path}.')

# 写回更新后的 XML 文件
tree.write(yarn_file_path, xml_declaration=True, encoding='utf-8')

print(f'Updated {yarn_file_path} with new YARN configuration values.')