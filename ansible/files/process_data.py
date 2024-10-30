import subprocess
import re
import argparse
def process_data(runner):
    # Execute the Hadoop command and get output
    command = "hadoop fs -ls hdfs:///tpcds/tpcds_result"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Parse lines and filter for 'timestamp=' lines
    lines = result.stdout.splitlines()
    timestamp_lines = [line for line in lines if "timestamp=" in line]

    # Extract the timestamp and find the latest one
    latest_timestamp = None

    for line in timestamp_lines:
        match = re.search(r'timestamp=(\d+)', line)
        if match:
            timestamp = int(match.group(1))
            if latest_timestamp is None or timestamp > latest_timestamp:
                latest_timestamp = timestamp

    # Run the bash script with the latest timestamp using sudo
    if latest_timestamp:
        print(f"Running get_tpcds_result.sh with timestamp: {latest_timestamp}")
        subprocess.run(["sudo", "-i", "bash", "get_tpcds_result.sh",runner, str(latest_timestamp)])
    else:
        print("No timestamped directories found.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='process data')
    parser.add_argument('--runner', type=str, default="spark", help='runner type')
    args = parser.parse_args()
    process_data(args.runner)