import argparse
from utils import parallel_create_instances

# Main function to parse command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch EC2 instances')
    parser.add_argument('--num-instances', type=int, default=4, help='实例数')
    parser.add_argument('--region', type=str, default="us-west-1", help='实例所在区域')
    parser.add_argument('--instance-type', type=str, default="i4i.4xlarge", help='实例类型')
    parser.add_argument('--instance-zone', type=str, default="us-west-1a", help='实例具体区域')
    parser.add_argument('--ami', type=str, default="ami-0819a8650d771b8be", help='启动镜像')
    parser.add_argument('--key-pair', type=str, default="aws_test", help='ssh连接密钥名')
    parser.add_argument('--security-group-id', type=str, default="sg-015b9bb06f0a09b38", help='安全组')
    parser.add_argument('--subnet-id', type=str, default="subnet-07a2f99a594ac6b0a", help='子网')
    parser.add_argument('--use-nvme', type=bool, default=True, help='是否使用nvme,需要实例类型支持')
    parser.add_argument('--run-number', type=str, default="0", help='github action run number')
    parser.add_argument('--run-type', type=str, default="spark", help='运行任务类型')
    
    args = parser.parse_args()
    
    # Launch instances based on command line inputs
    instances = parallel_create_instances(
            num_instances=args.num_instances,
            region=args.region,
            instance_type=args.instance_type,
            instance_zone=args.instance_zone,
            ami=args.ami,
            key_pair=args.key_pair,
            security_group_id=args.security_group_id,
            subnet_id=args.subnet_id,
            use_nvme=args.use_nvme,
            run_number=args.run_number,
            run_type=args.run_type)
       