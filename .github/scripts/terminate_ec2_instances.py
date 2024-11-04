import argparse
from utils import terminate_instances


# Main function to parse command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Terminate instances.')
    parser.add_argument('--region', type=str, default="us-west-1", help='实例所在区域')
    parser.add_argument('--run-number', type=str, default="0", help='github action run number')
    parser.add_argument('--run-type', type=str, default="spark", help='运行任务类型')
    parser.add_argument('--ignore', type=bool, default=False, help='是否应该忽略，而不终止实例')
    args = parser.parse_args()
    terminate_instances(args.region,args.run_type,args.run_number,args.ignore)