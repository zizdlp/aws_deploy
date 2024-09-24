export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_OPTS="--add-opens=java.base/java.lang=ALL-UNNAMED $HADOOP_OPTS"
export HADOOP_SSH_OPTS="-i /root/.ssh/id_rsa -o StrictHostKeyChecking=no"