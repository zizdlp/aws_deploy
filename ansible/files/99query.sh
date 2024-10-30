cp /usr/local/spark/conf/spark-defaults-$1.conf /usr/local/spark/conf/spark-defaults.conf
/usr/local/spark/bin/spark-submit \
--master yarn \
--deploy-mode client \
--conf spark.sql.catalogImplementation=hive \
--conf spark.executor.instances=3 \
--class com.databricks.spark.sql.perf.tpcds.TPCDSRunMain \
./spark-sql-perf-assembly-0.5.1-SNAPSHOT.jar -d tpcds_1000_partition -l hdfs:///tpcds/tpcds_result

#--jars general-test-1.0-SNAPSHOT.jar \
#--conf spark.extraListeners=com.houdutech.ChukonuFallbackListener
