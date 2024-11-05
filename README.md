# AWS spark 集群部署测试

<div align="center">

[![Actions Status](https://github.com/zizdlp/aws_deploy/workflows/TEST_TPCDS/badge.svg)](https://github.com/zizdlp/aws_deploy/actions)

</div>

curl -H "Authorization: token <YOUR_GITHUB_TOKEN>" \
  <https://api.github.com/repos/><OWNER>/<REPO>/actions/runs/<RUN_ID>/artifacts

curl -L -H "Authorization: token <YOUR_GITHUB_TOKEN>" \
  -o spark_result_53_100.zip \
  <https://api.github.com/repos/><OWNER>/<REPO>/actions/artifacts/<ARTIFACT_ID>/zip

## try self host

## 在ami中预安装依赖

```sh
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install -y tmux unzip git byacc flex bison locales tzdata ccache cmake ninja-build build-essential llvm-11-dev clang-11 libiberty-dev libdwarf-dev libre2-dev libz-dev libssl-dev libboost-all-dev libcurl4-openssl-dev openjdk-11-jdk maven libtbb-dev libjemalloc-dev libspdlog-dev g++ g++-9 g++-10 libmsgsl-dev libgtest-dev nfs-common nfs-kernel-server pkg-config libbenchmark-dev python3 python3-pip mysql-server python3-pymysql
```

```sh
wget https://apt.llvm.org/llvm.sh
chmod +x llvm.sh
sudo ./llvm.sh 18 all
ls /usr/bin/ | grep clang
```

```sh
pip install boto3
pip install botocore
```
