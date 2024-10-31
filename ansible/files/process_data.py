import subprocess
import re
import os
import shutil
import argparse
# Set environment variables
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
os.environ["SPARK_HOME"] = "/usr/local/spark"
os.environ["CLASSPATH"] = ".:" + os.path.join(os.environ["JAVA_HOME"], "lib")
os.environ["PATH"] = os.environ["PATH"] + ":" + os.path.join(os.environ["JAVA_HOME"], "bin")
os.environ["HADOOP_HOME"] = "/usr/local/hadoop"
os.environ["PATH"] += f":{os.environ['HADOOP_HOME']}/bin:{os.environ['HADOOP_HOME']}/sbin"
os.environ["HADOOP_COMMON_HOME"] = os.environ["HADOOP_HOME"]
os.environ["HADOOP_HDFS_HOME"] = os.environ["HADOOP_HOME"]
os.environ["HADOOP_YARN_HOME"] = os.environ["HADOOP_HOME"]
os.environ["HADOOP_MAPRED_HOME"] = os.environ["HADOOP_HOME"]
os.environ["HADOOP_CONF_DIR"] = os.path.join(os.environ["HADOOP_HOME"], "etc", "hadoop")
os.environ["HADOOP_COMMON_LIB_NATIVE_DIR"] = os.path.join(os.environ["HADOOP_HOME"], "lib", "native")
os.environ["HADOOP_OPTS"] = "-Djava.library.path=" + os.environ["HADOOP_COMMON_LIB_NATIVE_DIR"]
os.environ["LD_LIBRARY_PATH"] = f"{os.environ['HADOOP_COMMON_LIB_NATIVE_DIR']}:{os.environ.get('LD_LIBRARY_PATH', '')}"
os.environ["LD_PRELOAD"] = "/opt/chukonu_install/lib/libchukonu_preloaded.so:/lib/x86_64-linux-gnu/libjemalloc.so.2"
os.environ["LD_LIBRARY_PATH"] = f"/opt/chukonu_install/lib:{os.environ['LD_LIBRARY_PATH']}:/opt/chukonu_cache"
os.environ["HDFS_NAMENODE_USER"] = "ubuntu"
os.environ["HDFS_DATANODE_USER"] = "ubuntu"
os.environ["HDFS_SECONDARYNAMENODE_USER"] = "ubuntu"
os.environ["YARN_RESOURCEMANAGER_USER"] = "ubuntu"
os.environ["YARN_NODEMANAGER_USER"] = "ubuntu"
os.environ["HIVE_HOME"] = "/usr/local/hive"
os.environ["PATH"] += f":{os.environ['HIVE_HOME']}/bin"
os.environ["SCALA_HOME"] = "/usr/local/scala"
os.environ["PATH"] += f":{os.environ['SCALA_HOME']}/bin"
os.environ["PATH"] += f":{os.environ['SPARK_HOME']}/bin"
def process_data(runner):
    result = subprocess.run(["hadoop fs -ls hdfs:///tpcds/tpcds_result"], shell=True, capture_output=True, text=True)

    # Parse lines and filter for 'timestamp=' lines
    lines = result.stdout.splitlines()
    timestamp_lines = [line for line in lines if "timestamp=" in line]
    print(lines)
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
        subprocess.run(["sudo", "bash", "get_tpcds_result.sh", runner, str(latest_timestamp)])

        # Define the path to the timestamped directory
        timestamped_dir = f"{latest_timestamp}"  # Adjust this path as needed

        # Find the .csv file in the directory
        for file in os.listdir(timestamped_dir):
            if file.endswith(".csv"):
                csv_path = os.path.join(timestamped_dir, file)

                # Copy and rename the .csv file to the current directory
                shutil.copy(csv_path, f"{runner}_result.csv")
                print(f"CSV file copied to current directory as {runner}_result.csv")
                break
        else:
            print("No CSV file found in the timestamped directory.")
    else:
        print("No timestamped directories found.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='process data')
    parser.add_argument('--runner', type=str, default="spark", help='runner type')
    args = parser.parse_args()
    process_data(args.runner)