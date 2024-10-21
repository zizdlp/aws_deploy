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

# 提取 Chukonu 结果的后半部分
half_index = len(df_chukonu_clean) // 2
df_chukonu_second_half = df_chukonu_clean.iloc[half_index:]

# 合并数据
merged_df = pd.merge(df_spark_clean, df_chukonu_second_half, on="Query", suffixes=('_spark', '_chukonu'))

# 添加耗时对比列（百分比）
merged_df['Time_Difference_Percentage'] = ((merged_df['Runtime_spark'] - merged_df['Runtime_chukonu']) / merged_df['Runtime_chukonu']) * 100

# 设置打印选项以显示所有行
pd.set_option('display.max_rows', None)  # None 表示不限制行数
pd.set_option('display.max_columns', None)  # None 表示不限制列数

# 打印比较结果
print("Query Comparison Results:")
print(merged_df)

# 计算总运行时间
total_runtime_spark = df_spark[df_spark["Query"] == "Power"]["Runtime"].astype(float).values[0]
total_runtime_chukonu = df_chukonu_second_half["Runtime"].sum()  # 使用后半部分的运行时间总和

# 计算差异百分比
percentage_difference = ((total_runtime_spark - total_runtime_chukonu) / total_runtime_chukonu) * 100

# 打印总运行时间对比和百分比差异
print(f"\nTotal Runtime for Spark: {total_runtime_spark}")
print(f"Total Runtime for Chukonu: {total_runtime_chukonu}")
print(f"Difference in total runtime: {percentage_difference:.2f}%")