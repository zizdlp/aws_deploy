#!/bin/bash
set -x
source confargs.sh

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





if [ $# -ne 4 ]; then
  echo "./run.sh Load Power Throughput Maintenance"
  echo "example ./run.sh true true true true"
  exit 1
fi

cd ${TPCDSBENCHMARK}
${SBT} +package

cd ${LOCAL_DIR}

if [ "$1" = "true" ]; then
  # Load Test
  ${SPARKSUBMIT} --master ${MASTER} ${CHUKONU_CONF_ARGS} --class com.houdu.tpcds.Load ${JAR} ${scaleFactor} ${format} ${dsdgenDir} ${dsdgen_partitioned} ${dsdgen_nonpartitioned} ${warehousePath} ${tmp_chu}
else
  echo "not Load"
fi

if [ "$2" = "true" ]; then
  # Power Test
  ${SPARKSUBMIT} --master ${MASTER} ${CHUKONU_CONF_ARGS} --class com.houdu.tpcds.Power ${JAR} ${queriesDir} ${DB} ${warehousePath} ${tmp_chu}

else
  echo "not Power"
fi

#Throughput Test
if [ "$3" = "true" ]; then
  ${SPARKSUBMIT} --master ${MASTER} ${CHUKONU_CONF_ARGS} --class com.houdu.tpcds.Throughput ${JAR} ${queriesDir} ${DB} ${warehousePath} ${tmp_chu} 1 4
else
  echo "not Throughput"
fi


#Maintenance Test
if [ "$4" = "true" ]; then
  for i in {1..4}; do
    ${SPARKSQL} --master ${MASTER} ${CHUKONU_CONF_ARGS} -f ${LOCAL_MT_SQL_DIR}/${i}/create_mt_tables.sql --hivevar DB=${DB} --hivevar ROUND=$i --hivevar LOCATION=${MT_FLATDATA_DIR}
  done

  for REFRESH_ID in {1..4}; do
    DATE=$(cat ${LOCAL_MT_DATA_DIR}/delete_${REFRESH_ID}.dat | sed "s/|$//g" | sed "s/|/,/g" | xargs | sed "s/ /:/g")
    IDATE=$(cat ${LOCAL_MT_DATA_DIR}/inventory_delete_${REFRESH_ID}.dat | sed "s/|$//g" | sed "s/|/,/g" | xargs | sed "s/ /:/g")
    ${SPARKSUBMIT} --master ${MASTER} ${CHUKONU_CONF_ARGS} --class com.houdu.tpcds.Maintenance ${JAR} ${LOCAL_MT_SQL_DIR}/${REFRESH_ID} ${DB} ${warehousePath} ${tmp_chu} ${REFRESH_ID} ${DATE} ${IDATE}
  done
else
  echo "not Maintenance"
fi