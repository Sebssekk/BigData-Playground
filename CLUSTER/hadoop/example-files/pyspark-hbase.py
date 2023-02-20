from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Hbase test").getOrCreate()

catalog = ''.join("""
{
  'table':{
    'namespace':'default',
    'name' : 'emp'
  },
  'rowkey' : 'key',
  'columns' : {
      'name' : {'cf':'personal data','col':'name','type':'string'}
    }
}
""".split())

h_table = spark.read\
    .options(catalog=catalog)\
    .format('org.apache.hadoop.hbase.spark')\
    .load()
h_table.show()
