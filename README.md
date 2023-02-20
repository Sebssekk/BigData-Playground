# **Big data Playground**

This Repo contain a simple and pocket lab for your BigData experiments.

The lab is composed by :

- Three container acting as **datanode** for HDFS cluster
- One container acting as **namenode** for HDFS cluster. On this container you can run:
  - **hdfs** commands (hadoop 3)
  - **MapReduce** jobs (scheduling on YARN)
  - **HIVE2** (working MR by default) tables
  - **SPARK** 3 tasks
  - There's a running **Jupyter Notebook** for better files editing and Pyspark tests
  - **HBASE** shell
  - HBASE thrift and rest servers are also enabled (for python happybase tests)
  - **SQOOP2**
  - **FLUME**
- 3 **ZooKeeper** nodes
- A container running **HUE** UI
- A container runinng **Kafka** for Streamig tests
- A Container running **Kudu master** node
- 3 containers running **Kudu tservers** nodes
- A container running **Impala** with Kudu integration

At the moment everything runs on docker-compose. The _cluster.sh_ utility make the interaction with docker-compose a bit easyer
