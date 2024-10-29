import pandas as pd
import argparse
def compare_result(spark,chukonu):
    # 读取下载的结果文件
    df_spark = pd.read_csv(spark, header=None, names=["Query", "Runtime"])
    df_chukonu = pd.read_csv(chukonu, header=None, names=["Query", "Runtime"])

    # 去除 "Power" 行
    df_spark_clean = df_spark[df_spark["Query"] != "Power"]
    df_chukonu_clean = df_chukonu[df_chukonu["Query"] != "Power"]

    # 转换为浮点数
    df_spark_clean["Runtime"] = df_spark_clean["Runtime"].astype(float)
    df_chukonu_clean["Runtime"] = df_chukonu_clean["Runtime"].astype(float)

    # 提取 Chukonu 结果的前半部分和后半部分
    half_index = len(df_chukonu_clean) // 2
    df_chukonu_first_half = df_chukonu_clean.iloc[:half_index]  # 提取前半部分
    df_chukonu_second_half = df_chukonu_clean.iloc[half_index:]  # 提取后半部分

    # 分别合并数据
    merged_first_half = pd.merge(df_spark_clean, df_chukonu_first_half, on="Query", suffixes=('_spark', '_chukonu_first'))
    merged_second_half = pd.merge(df_spark_clean, df_chukonu_second_half, on="Query", suffixes=('_spark', '_chukonu_second'))

    # 将两个合并结果连接在一起
    merged_df = pd.merge(merged_first_half, merged_second_half, on="Query", suffixes=('', '_dup'))

    # 添加耗时对比列（百分比）
    merged_df['Time_Difference_First_Half_Percentage'] = (
        (merged_df['Runtime_spark']) / merged_df['Runtime_chukonu_first']
    ) * 100

    merged_df['Time_Difference_Second_Half_Percentage'] = (
        (merged_df['Runtime_spark']) / merged_df['Runtime_chukonu_second']
    ) * 100

    # 设置打印选项以显示所有行
    pd.set_option('display.max_rows', None)  # None 表示不限制行数
    pd.set_option('display.max_columns', None)  # None 表示不限制列数

    # 打印比较结果
    print("Query Comparison Results:")
    print(merged_df)

    # 计算总运行时间
    total_runtime_spark = df_spark[df_spark["Query"] == "Power"]["Runtime"].astype(float).values[0]
    total_runtime_chukonu_first_half = df_chukonu_first_half["Runtime"].sum()  # 前半部分的运行时间总和
    total_runtime_chukonu_second_half = df_chukonu_second_half["Runtime"].sum()  # 后半部分的运行时间总和

    # 计算差异百分比
    percentage_difference_first_half = ((total_runtime_spark) / total_runtime_chukonu_first_half) * 100
    percentage_difference_second_half = ((total_runtime_spark) / total_runtime_chukonu_second_half) * 100

    # 打印总运行时间对比和百分比差异
    print(f"\nTotal Runtime for Spark: {total_runtime_spark}")
    print(f"Total Runtime for Chukonu (First Half): {total_runtime_chukonu_first_half}")
    print(f"Total Runtime for Chukonu (Second Half): {total_runtime_chukonu_second_half}")
    print(f"Difference in total runtime for First Half: {percentage_difference_first_half:.2f}%")
    print(f"Difference in total runtime for Second Half: {percentage_difference_second_half:.2f}%")

    # Save the merged DataFrame to a CSV file
    merged_df.to_csv(f'tpcds_result.csv', index=False)

    print(f"Merged DataFrame has been saved to tpcds_result.csv")

    # Main function to parse command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch EC2 instances.')
    parser.add_argument('--spark', type=str, default="spark_result.csv", help='Number of instances to launch')
    parser.add_argument('--chukonu', type=str, default='chukonu_result.csv', help='EC2 instance type')

    
    args = parser.parse_args()
    compare_result(args.spark,args.chukonu)