set -x
source var.sh

ALLJARS=/opt/all_jars/
LD_PRELOAD=$CHUKONU_INSTALL/lib/libchukonu_preloaded.so:/lib/x86_64-linux-gnu/libjemalloc.so.2
GLUTEN_JAR=${ALLJARS}/gluten-velox-bundle-spark3.4_2.12-ubuntu_20.04-1.1.0-SNAPSHOT.jar
BYR_JAR=${ALLJARS}/learnoptimizeskewed_2.12-0.1.0-SNAPSHOT.jar
CHUKONU_JAR=${ALLJARS}/chukonu_2.12-0.5.1.jar
JAVA8=/usr/lib/jvm/java-1.8.0-openjdk-amd64
JAVA11=/usr/lib/jvm/java-11-openjdk-amd64

CONF_ARGS="--deploy-mode client \
--packages com.github.scopt:scopt_2.12:3.7.1,io.delta:delta-core_2.12:2.4.0 \
--conf spark.executorEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--conf spark.yarn.appMasterEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--num-executors ${spark_numexecutors} --executor-cores ${spark_executorcores} --executor-memory ${spark_executormemory} \
--conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
--conf spark.shuffle.service.enabled=true \
--conf spark.scheduler.maxRegisteredResourcesWaitingTime=36000s \
--conf spark.scheduler.minRegisteredResourcesRatio=1.0 \
--conf spark.memory.offHeap.enabled=false \
--conf spark.memory.offHeap.size=${spark_offsize} \
--conf spark.executor.memoryOverhead=${spark_overhead} \
--conf spark.driver.memory=4g \
--conf spark.default.parallelism=${parallelism} "

CHUKONU_CONF_ARGS="--deploy-mode client \
--packages com.github.scopt:scopt_2.12:3.7.1,io.delta:delta-core_2.12:2.4.0 \
--conf spark.executorEnv.JAVA_HOME=${JAVA11} \
--conf spark.yarn.appMasterEnv.JAVA_HOME=${JAVA11} \
--conf spark.executorEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--conf spark.yarn.appMasterEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--num-executors ${chukonu_numexecutors} --executor-cores ${chukonu_executorcores} --executor-memory ${chukonu_executormemory} \
--conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
--conf spark.shuffle.service.enabled=true \
--conf spark.scheduler.maxRegisteredResourcesWaitingTime=36000s \
--conf spark.scheduler.minRegisteredResourcesRatio=1.0 \
--conf spark.memory.offHeap.enabled=true \
--conf spark.memory.offHeap.size=${chukonu_offsize} \
--conf spark.executor.memoryOverhead=${chukonu_overhead} \
--conf spark.kryo.unsafe=true \
--conf spark.executor.processTreeMetrics.enabled=true \
--conf spark.plugins=org.pacman.chukonu.ChukonuPlugin \
--conf spark.chukonu.enableNativeCodegen=true \
--conf spark.chukonu.root=${CHUKONU_INSTALL} \
--conf spark.chukonu.cxx=${CHUKONU_GPP} \
--conf spark.chukonu.stagingdir=${CHUKONU_STAGING} \
--conf spark.chukonu.compileCacheDir=${CHUKONU_CACHE} \
--conf spark.executorEnv.LD_LIBRARY_PATH=${CHUKONU_INSTALL}/lib:${LD_LIBRARY_PATH} \
--conf spark.yarn.appMasterEnv.LD_LIBRARY_PATH=${CHUKONU_INSTALL}/lib:${LD_LIBRARY_PATH} \
--conf spark.executorEnv.LD_PRELOAD=${CHUKONU_INSTALL}/lib/libchukonu_preloaded.so:${LD_PRELOAD} \
--conf spark.yarn.appMasterEnv.LD_PRELOAD=${CHUKONU_INSTALL}/lib/libchukonu_preloaded.so:${LD_PRELOAD} \
--conf spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold=512MB \
--conf spark.eventLog.enabled=true --conf spark.eventLog.dir=~/logs \
--jars ${CHUKONU_JAR} "
