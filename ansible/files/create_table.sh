
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_HOME=/usr/local/spark
export CLASSPATH=.:${JAVA_HOME}/lib
export PATH=$PATH:$JAVA_HOME/bin
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_YARN_HOME=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop/
export HADOOP_COMMON_LIB_NATIVE_DIR=${HADOOP_HOME}/lib/native
export HADOOP_OPTS="-Djava.library.path=${HADOOP_HOME}/lib/native"
export LD_LIBRARY_PATH=$HADOOP_COMMON_LIB_NATIVE_DIR:$LD_LIBRARY_PATH
export LD_PRELOAD=/opt/chukonu_install/lib/libchukonu_preloaded.so:/lib/x86_64-linux-gnu/libjemalloc.so.2
export LD_LIBRARY_PATH=/opt/chukonu_install/lib:${LD_LIBRARY_PATH}:/opt/chukonu_cache
export HDFS_NAMENODE_USER=ubuntu
export HDFS_DATANODE_USER=ubuntu
export HDFS_SECONDARYNAMENODE_USER=ubuntu
export YARN_RESOURCEMANAGER_USER=ubuntu
export YARN_NODEMANAGER_USER=ubuntu
export HIVE_HOME=/usr/local/hive
export PATH=$PATH:$HIVE_HOME/bin
export SCALA_HOME=/usr/local/scala
export PATH=$PATH:$SCALA_HOME/bin
export PATH=$PATH:$SPARK_HOME/bin


cp /usr/local/spark/conf/spark-defaults-$1.conf /usr/local/spark/conf/spark-defaults.conf
/usr/local/spark/bin/spark-submit \
--master yarn \
--deploy-mode client \
--conf spark.sql.catalogImplementation=hive \
--conf spark.executor.instances=3 \
--class com.databricks.spark.sql.perf.tpcds.TPCDSCreateTable \
./spark-sql-perf-assembly-0.5.1-SNAPSHOT.jar -d tpcds_1000_partition -l hdfs://node0:9898/tpcds/tpcds_1000_partition -f parquet

#--jars general-test-1.0-SNAPSHOT.jar \
#--conf spark.extraListeners=com.houdutech.ChukonuFallbackListener
