from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("TestJob").getOrCreate()
data = [("Alice", 29), ("Bob", 31), ("Catherine", 25)]
df = spark.createDataFrame(data, ["Name", "Age"])
df.show()

spark.stop()