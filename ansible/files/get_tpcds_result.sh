cp /usr/local/spark/conf/spark-defaults-$1.conf /usr/local/spark/conf/spark-defaults.conf
/usr/local/spark/bin/spark-submit \
--master local[*] \
--deploy-mode client \
--conf spark.sql.catalogImplementation=hive \
--conf spark.executor.instances=1 \
--conf spark.executor.cores=1 \
--conf spark.executor.memory=2G \
--conf spark.executor.memoryOverhead=200M \
--class com.databricks.spark.sql.perf.tpcds.TPCDSGetResult \
./spark-sql-perf-assembly-0.5.1-SNAPSHOT.jar -t $2 -l hdfs:///tpcds/tpcds_result/timestamp=$2 -r hdfs:///tpcds/tpcds_result/time/$2

hadoop fs -get hdfs:///tpcds/tpcds_result/time/$2

#--jars general-test-1.0-SNAPSHOT.jar \
#--conf spark.extraListeners=com.houdutech.ChukonuFallbackListener
