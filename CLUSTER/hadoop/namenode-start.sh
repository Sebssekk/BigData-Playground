#!/bin/bash
## HDFS
echo "########## HSFD - format & start"
hdfs namenode -format && start-dfs.sh 
## YARN
echo "########## YARN - start"
start-yarn.sh
#httpfs.sh 
echo "########## HTTPFS - start"
hdfs --daemon start httpfs 
## HIVE
echo "########## HIVE - setup"
hdfs dfs -mkdir -p /tmp 
hdfs dfs -mkdir -p /user/hive/warehouse
schematool -dbType mysql -initSchema
echo "########## HIVESERVER2 - start"
nohup hiveserver2 > hiveserver2.log &
hdfs dfs -mkdir -p /hbase
hdfs dfs -mkdir -p /flume01 
## SPARK
hdfs dfs -mkdir -p /spark-logs
echo "########## SPARK - runall"
${SPARK_HOME}/sbin/start-history-server.sh
${SPARK_HOME}/sbin/start-all.sh
echo "########## JUPYTER - run"
nohup jupyter notebook \
--ip 0.0.0.0 \
--port 8888 \
--no-browser \
--NotebookApp.token='' \
--NotebookApp.password='' \
> jupyter-error.log &
## LIVY Server
echo "########## LIVY - server start"
livy-server start
## HBASE
echo "########## HBASE - start"
start-hbase.sh
hbase-daemon.sh start thrift -p 9090 --infoport 9095 
hbase-daemon.sh start rest -p 8090 --infoport 8095 
## SQOOP - DEPRECATED
#sqoop2-server start
echo "########## READY"
tail -f /dev/null
