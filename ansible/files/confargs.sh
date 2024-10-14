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
--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
--conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
--num-executors ${numexecutors} --executor-cores ${executorcores} --executor-memory ${executormemory} \
--conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
--conf spark.shuffle.service.enabled=true \
--conf spark.scheduler.maxRegisteredResourcesWaitingTime=36000s \
--conf spark.scheduler.minRegisteredResourcesRatio=1.0 \
--conf spark.memory.offHeap.enabled=false \
--conf spark.memory.offHeap.size=${offsize} \
--conf spark.executor.memoryOverhead=${overhead} \
--conf spark.driver.memory=4g \
--conf spark.default.parallelism=${parallelism} "

GLUTEN_CONF_ARGS="--deploy-mode client \
--packages com.github.scopt:scopt_2.12:3.7.1,io.delta:delta-core_2.12:2.4.0 \
--conf spark.executorEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--conf spark.yarn.appMasterEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
--conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
--num-executors ${numexecutors} --executor-cores ${executorcores} --executor-memory ${executormemory} \
--conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
--conf spark.shuffle.service.enabled=true \
--conf spark.scheduler.maxRegisteredResourcesWaitingTime=36000s \
--conf spark.scheduler.minRegisteredResourcesRatio=1.0 \
--conf spark.memory.offHeap.enabled=true \
--conf spark.memory.offHeap.size=${offsize} \
--conf spark.plugins=io.glutenproject.GlutenPlugin \
--conf spark.driver.extraClassPath=${GLUTEN_JAR} \
--conf spark.executor.extraClassPath=${GLUTEN_JAR} \
--conf spark.executor.memoryOverhead=${overhead} \
--conf spark.driver.memory=4g \
--conf spark.gluten.sql.columnar.forceShuffledHashJoin=true \
--conf spark.shuffle.manager=org.apache.spark.shuffle.sort.ColumnarShuffleManager \
--conf spark.executorEnv.LIBHDFS3_CONF=/opt/gluten/hdfs-client.xml "

BYR_CONF_ARGS="--deploy-mode client \
--packages com.github.scopt:scopt_2.12:3.7.1,io.delta:delta-core_2.12:2.4.0 \
--conf spark.executorEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--conf spark.yarn.appMasterEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension,com.houdu.FirstSparkSessionExtensions \
--conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
--num-executors ${numexecutors} --executor-cores ${executorcores} --executor-memory ${executormemory} \
--conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
--conf spark.shuffle.service.enabled=true \
--conf spark.scheduler.maxRegisteredResourcesWaitingTime=36000s \
--conf spark.scheduler.minRegisteredResourcesRatio=1.0 \
--conf spark.memory.offHeap.enabled=true \
--conf spark.memory.offHeap.size=${offsize} \
--conf spark.executor.memoryOverhead=${overhead} \
--conf spark.driver.memory=4g \
--jars ${BYR_JAR} "

BYR_GLUTEN_CONF_ARGS="--deploy-mode client \
--packages com.github.scopt:scopt_2.12:3.7.1,io.delta:delta-core_2.12:2.4.0 \
--conf spark.executorEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--conf spark.yarn.appMasterEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension,com.houdu.FirstSparkSessionExtensions \
--conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
--num-executors ${numexecutors} --executor-cores ${executorcores} --executor-memory ${executormemory} \
--conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
--conf spark.shuffle.service.enabled=true \
--conf spark.scheduler.maxRegisteredResourcesWaitingTime=36000s \
--conf spark.scheduler.minRegisteredResourcesRatio=1.0 \
--conf spark.memory.offHeap.enabled=true \
--conf spark.memory.offHeap.size=${offsize} \
--conf spark.plugins=io.glutenproject.GlutenPlugin \
--conf spark.driver.extraClassPath=${GLUTEN_JAR}:${BYR_JAR} \
--conf spark.executor.extraClassPath=${GLUTEN_JAR}:${BYR_JAR} \
--conf spark.gluten.sql.columnar.forceShuffledHashJoin=true \
--conf spark.executor.memoryOverhead=${overhead} \
--conf spark.driver.memory=4g \
--conf spark.shuffle.manager=org.apache.spark.shuffle.sort.ColumnarShuffleManager "

CHUKONU_CONF_ARGS="--deploy-mode client \
--packages com.github.scopt:scopt_2.12:3.7.1,io.delta:delta-core_2.12:2.4.0 \
--conf spark.executorEnv.JAVA_HOME=${JAVA11} \
--conf spark.yarn.appMasterEnv.JAVA_HOME=${JAVA11} \
--conf spark.executorEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--conf spark.yarn.appMasterEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
--conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
--num-executors ${numexecutors} --executor-cores ${executorcores} --executor-memory ${executormemory} \
--conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
--conf spark.shuffle.service.enabled=true \
--conf spark.scheduler.maxRegisteredResourcesWaitingTime=36000s \
--conf spark.scheduler.minRegisteredResourcesRatio=1.0 \
--conf spark.memory.offHeap.enabled=true \
--conf spark.memory.offHeap.size=${offsize} \
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
--jars ${CHUKONU_JAR} "

CHUKONU_BYR_CONF_ARGS="--deploy-mode client \
--packages com.github.scopt:scopt_2.12:3.7.1,io.delta:delta-core_2.12:2.4.0 \
--conf spark.executorEnv.JAVA_HOME=${JAVA11} \
--conf spark.yarn.appMasterEnv.JAVA_HOME=${JAVA11} \
--conf spark.executorEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--conf spark.yarn.appMasterEnv.LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension,com.houdu.FirstSparkSessionExtensions \
--conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
--num-executors ${numexecutors} --executor-cores ${executorcores} --executor-memory ${executormemory} \
--conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
--conf spark.shuffle.service.enabled=true \
--conf spark.scheduler.maxRegisteredResourcesWaitingTime=36000s \
--conf spark.scheduler.minRegisteredResourcesRatio=1.0 \
--conf spark.memory.offHeap.enabled=true \
--conf spark.memory.offHeap.size=${offsize} \
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
--jars ${BYR_JAR},${CHUKONU_JAR} "