#!/bin/bash
set -x
source confargs.sh

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
  ${SPARKSUBMIT} --master ${MASTER} ${CONF_ARGS} --class com.houdu.tpcds.Load ${JAR} ${scaleFactor} ${format} ${dsdgenDir} ${dsdgen_partitioned} ${dsdgen_nonpartitioned} ${warehousePath} ${tmp_spark}
else
  echo "not Load"
fi

if [ "$2" = "true" ]; then
  # Power Test
  ${SPARKSUBMIT} --master ${MASTER} ${CONF_ARGS} --class com.houdu.tpcds.Power ${JAR} ${queriesDir} ${DB} ${warehousePath} ${tmp_spark}
  #${SPARKSUBMIT} --master ${MASTER} ${BYR_CONF_ARGS} --class com.houdu.tpcds.Power ${JAR} ${queriesDir} ${DB} ${warehousePath} ${tmp_byr}
  #${SPARKSUBMIT} --master ${MASTER} ${CHUKONU_CONF_ARGS} --class com.houdu.tpcds.Power ${JAR} ${queriesDir} ${DB} ${warehousePath} ${tmp_chu}
  #${SPARKSUBMIT} --master ${MASTER} ${CHUKONU_BYR_CONF_ARGS} --class com.houdu.tpcds.Power ${JAR} ${queriesDir} ${DB} ${warehousePath} ${tmp_chu_byr}
  #${SPARKSUBMIT} --master ${MASTER} ${GLUTEN_CONF_ARGS} --class com.houdu.tpcds.Power ${JAR} ${queriesDir} ${DB} ${warehousePath} ${tmp_glu}
  #${SPARKSUBMIT} --master ${MASTER} ${BYR_GLUTEN_CONF_ARGSGLUTEN_CONF_ARGS} --class com.houdu.tpcds.Power ${JAR} ${queriesDir} ${DB} ${warehousePath} ${tmp_glu_byr}

else
  echo "not Power"
fi

#Throughput Test
if [ "$3" = "true" ]; then
  #${SPARKSUBMIT} --master ${MASTER} ${GLUTEN_CONF_ARGS} --class com.houdu.tpcds.Throughput ${JAR} ${queriesDir} ${DB} ${warehousePath} ${tmp_glu} 1 4
  ${SPARKSUBMIT} --master ${MASTER} ${CONF_ARGS} --class com.houdu.tpcds.Throughput ${JAR} ${queriesDir} ${DB} ${warehousePath} ${tmp_spark} 1 4
else
  echo "not Throughput"
fi


#Maintenance Test
if [ "$4" = "true" ]; then
  for i in {1..4}; do
    ${SPARKSQL} --master ${MASTER} ${CONF_ARGS} -f ${LOCAL_MT_SQL_DIR}/${i}/create_mt_tables.sql --hivevar DB=${DB} --hivevar ROUND=$i --hivevar LOCATION=${MT_FLATDATA_DIR}
  done

  for REFRESH_ID in {1..4}; do
    DATE=$(cat ${LOCAL_MT_DATA_DIR}/delete_${REFRESH_ID}.dat | sed "s/|$//g" | sed "s/|/,/g" | xargs | sed "s/ /:/g")
    IDATE=$(cat ${LOCAL_MT_DATA_DIR}/inventory_delete_${REFRESH_ID}.dat | sed "s/|$//g" | sed "s/|/,/g" | xargs | sed "s/ /:/g")
    ${SPARKSUBMIT} --master ${MASTER} ${CONF_ARGS} --class com.houdu.tpcds.Maintenance ${JAR} ${LOCAL_MT_SQL_DIR}/${REFRESH_ID} ${DB} ${warehousePath} ${tmp_spark} ${REFRESH_ID} ${DATE} ${IDATE}
  done
else
  echo "not Maintenance"
fi

#Throughput Test
# if [ "$3" = "true" ]; then
#   ${SPARKSUBMIT} --master ${MASTER} ${BYR_CONF_ARGS} --class com.houdu.tpcds.Throughput ${JAR} ${queriesDir} ${DB} ${warehousePath} ${tmp_byr} 1 4
# else
#   echo "not Throughput"
# fi

#Maintenance Test
# if [ "$4" = "true" ]; then
#   for i in {1..4}; do
#     ${SPARKSQL} --master ${MASTER} ${CONF_ARGS} -f ${LOCAL_MT_SQL_DIR}/${i}/create_mt_tables.sql --hivevar DB=${DB} --hivevar ROUND=$i --hivevar LOCATION=${MT_FLATDATA_DIR}
#   done

#   for REFRESH_ID in {1..4}; do
#     DATE=$(cat ${LOCAL_MT_DATA_DIR}/delete_${REFRESH_ID}.dat | sed "s/|$//g" | sed "s/|/,/g" | xargs | sed "s/ /:/g")
#     IDATE=$(cat ${LOCAL_MT_DATA_DIR}/inventory_delete_${REFRESH_ID}.dat | sed "s/|$//g" | sed "s/|/,/g" | xargs | sed "s/ /:/g")
#     ${SPARKSUBMIT} --master ${MASTER} ${CONF_ARGS} --class com.houdu.tpcds.Maintenance ${JAR} ${LOCAL_MT_SQL_DIR}/${REFRESH_ID} ${DB} ${warehousePath} ${tmp_byr} ${REFRESH_ID} ${DATE} ${IDATE}
#   done
# else
#   echo "not Maintenance"
# fi
#send mail
