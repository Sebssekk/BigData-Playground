from pyspark.sql import SparkSession

spark= SparkSession.builder.appName("Python Spark Kafka integration").getOrCreate()

df=spark.readStream.format("kafka")\
  .option("kafka.bootstrap.servers","kafka:9092")\
  .option("subscribe", "spark-topic")\
  .option("startingOffsets","earliest")\
  .load()\

#df.selectExpr("CAST(key AS STRING)","CAST(value AS STRING)")
#df.printSchema()

query = df.select(df.value).selectExpr("CAST(value AS STRING)")\
  .writeStream\
  .format("console")\
  .trigger(processingTime="2 seconds")\
  .option("checkpointLocation","hdfs://namenode:9000/spark-logs/test")\
  .start()
   
query.awaitTermination()
