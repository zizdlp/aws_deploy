import pandas as pd
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def compare(spark_path,chukonu_path):
    # Load the two CSV files
    file1 = pd.read_csv(spark_path, header=None)
    file2 = pd.read_csv(chukonu_path, header=None)

    # Extract the required columns
    result = pd.DataFrame({
        'Query Name': file1.iloc[:, 0],                  # First column from file1 as query names
        'Spark Result': file1.iloc[:, -2],               # Last column from file1
        'Chukonu Result': file2.iloc[:, -2]              # Last column from file2
    })

    # Calculate the Spark/Chukonu ratio
    result['Spark/Chukonu'] = result['Spark Result'] / result['Chukonu Result']

    # Calculate the sum row for the Spark Result and Chukonu Result columns
    sum_row = pd.DataFrame({
        'Query Name': ['sum'],
        'Spark Result': [result['Spark Result'].sum()],
        'Chukonu Result': [result['Chukonu Result'].sum()],
        'Spark/Chukonu': [result['Spark Result'].sum() / result['Chukonu Result'].sum()]  # Ratio of the sums
    })

    # Print total times for Spark and Chukonu
    print(f"======= total time: Spark: {sum_row['Spark Result'].iloc[0]}, Chukonu: {sum_row['Chukonu Result'].iloc[0]},Spark/Chukonu: {sum_row['Spark/Chukonu'].iloc[0]}")

    # Append the sum row to the result DataFrame
    result = pd.concat([result, sum_row], ignore_index=True)

    # Save the result to a new CSV file
    result.to_csv('tpcds_result.csv', index=False, header=True)


# Main function to parse command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch EC2 instances.')
    parser.add_argument('--spark', type=str, default='spark_result_first.csv', help='test')
    parser.add_argument('--chukonu', type=str, default='chukonu_result_second.csv', help='test')

    args = parser.parse_args()
    
    # Launch instances based on command line inputs
    instances = compare(args.spark, args.chukonu)