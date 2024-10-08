LOCAL_DIR=/opt
queriesDir=${LOCAL_DIR}/tpcds-queries
dsdgenDir=${LOCAL_DIR}/tpcds-kit/tools
scaleFactor=1000
LOCAL_MT_DATA_DIR=${queriesDir}/mt-data-dir
LOCAL_MT_SQL_DIR=${queriesDir}/mt-sql-dir
HDFS_DIR="hdfs://node0:9898/user/byr23/"
DB="byr_tpcds_sf${scaleFactor}_YESdecimal_YESdate_YESnulls"
MT_FLATDATA_DIR="${HDFS_DIR}/${DB}_mt_flat"
CHUKONU_GPP=/usr/bin/g++
CHUKONU_INSTALL=${LOCAL_DIR}/chukonu_install
CHUKONU_STAGING=${LOCAL_DIR}/chukonu_staging
CHUKONU_TMP=${LOCAL_DIR}/chukonu_tmp
CHUKONU_CACHE=${LOCAL_DIR}/chukonu_cache
LD_PRELOAD=${CHUKONU_INSTALL}/lib/libchukonu_preloaded.so
LD_LIBRARY_PATH=${LOCAL_DIR}/chukonu_install/lib:${LD_LIBRARY_PATH}
TPCDSBENCHMARK=${LOCAL_DIR}/tpcds-benchmark
SPARKSUBMIT="spark-submit"
SPARKSQL="spark-sql"
SBT="sbt"
JAR=${TPCDSBENCHMARK}"/target/scala-2.12/tpcds-benchmark_2.12-0.1.0-SNAPSHOT.jar"
MASTER="yarn"
numexecutors=3
executorcores=12
executormemory="30g"
offsize="0g"
parallelism=100

format="delta"
# format="parquet"
dsdgen_partitioned=200
dsdgen_nonpartitioned=10
warehousePath="hdfs://node0:9898/user/byr23/warehouse"
tmp_spark=${LOCAL_DIR}/tmp_spark
tmp_byr=${LOCAL_DIR}/tmp_byr
tmp_glu=${LOCAL_DIR}/tmp_gluten
tmp_glu_byr=${LOCAL_DIR}/tmp_gluten_byr
tmp_chu=${LOCAL_DIR}/tmp_chukonu
tmp_chu_byr=${LOCAL_DIR}/tmp_chukonu_byr


#mail
log_file="/opt/tpcds-benchmark/logs/gluten.log"
user_mail="wangshengdong@houdutech.cn"