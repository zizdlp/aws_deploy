import os
import stat
import xml.etree.ElementTree as ET

# 定义要匹配并替换/追加的变量及其默认值
spark_variables = {
    "spark.driver.memory":os.environ.get("SPARK_DRIVER_MEMORY", "4g"),
    "spark.executor.cores": os.environ.get("SPARK_EXECUTOR_CORES", 12),
    "spark.executor.memory": os.environ.get("SPARK_EXECUTOR_MEMORY", "90g"),
    "spark.executor.memoryOverhead": os.environ.get("SPARK_OVERHEAD", "6g"),
}

spark_conf_path = './ansible/files/spark-defaults-spark.conf'


chukonu_variables = {
    "spark.driver.memoryOverhead":os.environ.get("CHUKONU_DRIVER_OVERHEAD", "4g"),
    "spark.driver.memory":os.environ.get("CHUKONU_DRIVER_MEMORY", "4g"),
    "spark.executor.cores": os.environ.get("CHUKONU_EXECUTOR_CORES", 12),
    "spark.executor.memory": os.environ.get("CHUKONU_EXECUTOR_MEMORY", "48g"),
    "spark.executor.memoryOverhead": os.environ.get("CHUKONU_OVERHEAD", "46g"),
}

chukonu_conf_path = './ansible/files/spark-defaults-chukonu.conf'

def update_spark_conf(variables,conf_path):

    # 用于存储新的文件内容
    new_lines = []

    # 读取文件中的现有行
    if os.path.exists(conf_path):
        with open(conf_path, 'r') as var_file:
            existing_lines = var_file.readlines()
    else:
        existing_lines = []

    # 标记哪些变量已匹配
    updated_vars = {var: False for var in variables}

    # 逐行检查并更新现有行
    for line in existing_lines:
        updated = False
        for var_name, var_value in variables.items():
            if line.startswith(f"{var_name}="):  # 匹配到以变量名开头的行
                new_lines.append(f"{var_name}={var_value}\n")  # 用新的值替换
                updated_vars[var_name] = True  # 标记为已更新
                updated = True
                print(f"Updated {var_name} to {var_value}")
                break
        if not updated:
            new_lines.append(line)  # 保留未匹配到的行

    # 追加未匹配到的变量（新变量）
    for var_name, var_value in variables.items():
        if not updated_vars[var_name]:
            new_lines.append(f"{var_name}={var_value}\n")
            print(f"Appended {var_name} with value {var_value}")

    # 写回 conf 文件
    with open(conf_path, 'w') as var_file:
        var_file.writelines(new_lines)

    # 确保 conf 文件具有可执行权限
    st = os.stat(conf_path)
    os.chmod(conf_path, st.st_mode | stat.S_IEXEC)  # 添加执行权限
    print(f"Set {conf_path} as an executable.")


update_spark_conf(spark_variables,spark_conf_path)
update_spark_conf(chukonu_variables,chukonu_conf_path)

# 定义要替换的 YARN 配置属性及其默认值
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