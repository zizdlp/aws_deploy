import argparse
from utils import save_info
# Main function to parse command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='save node info')
    parser.add_argument('--region', type=str, default="us-west-1", help='实例所在区域')
    parser.add_argument('--run-number', type=str, default="0", help='github action run number')
    parser.add_argument('--run-type', type=str, default="spark", help='运行任务类型')
    args = parser.parse_args()
    
    # Launch instances based on command line inputs
    save_info(args.region,args.run_type,args.run_number)