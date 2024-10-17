import pandas as pd

# 读取下载的结果文件
df_spark = pd.read_csv('spark_result.csv', header=None, names=["Query", "Runtime"])
df_chukonu = pd.read_csv('chukonu_result.csv', header=None, names=["Query", "Runtime"])

# 去除 "Power" 行
df_spark_clean = df_spark[df_spark["Query"] != "Power"]
df_chukonu_clean = df_chukonu[df_chukonu["Query"] != "Power"]

# 转换为浮点数
df_spark_clean["Runtime"] = df_spark_clean["Runtime"].astype(float)
df_chukonu_clean["Runtime"] = df_chukonu_clean["Runtime"].astype(float)

# 合并数据
merged_df = pd.merge(df_spark_clean, df_chukonu_clean, on="Query", suffixes=('_spark', '_chukonu'))

# 添加耗时对比列
merged_df['Time_Difference'] = merged_df['Runtime_spark'] - merged_df['Runtime_chukonu']

# 打印比较结果
print(merged_df)

# 计算总运行时间
total_runtime_spark = df_spark[df_spark["Query"] == "Power"]["Runtime"].astype(float).values[0]
total_runtime_chukonu = df_chukonu[df_chukonu["Query"] == "Power"]["Runtime"].astype(float).values[0]

# 计算差异百分比
percentage_difference = ((total_runtime_spark - total_runtime_chukonu) / total_runtime_chukonu) * 100

# 打印总运行时间对比和百分比差异
print(f"Total Runtime for Spark: {total_runtime_spark}")
print(f"Total Runtime for Chukonu: {total_runtime_chukonu}")
print(f"Difference in total runtime: {percentage_difference:.2f}%")