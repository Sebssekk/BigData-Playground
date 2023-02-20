FROM ubuntu AS base

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Rome

RUN apt update -y \
    && apt -y install ssh \
    && apt -y install unzip \
    && apt -y install openjdk-8-jdk \
    && apt-get -y install sudo

FROM alpine as hadoop-dev
ENV HADOOP_VERSION=hadoop-3.3.4
RUN wget https://dlcdn.apache.org/hadoop/common/${HADOOP_VERSION}/${HADOOP_VERSION}.tar.gz \
    && tar -xzf ${HADOOP_VERSION}.tar.gz && mv ${HADOOP_VERSION} /hadoop
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/" >>\
    /hadoop/etc/hadoop/hadoop-env.sh
FROM base as hadoop
ARG UID=1000
ARG GID=1000
ARG HADOOP_INSTALL_DIR="/opt/hadoop"
RUN groupadd -g ${GID} hadoop || groupmod -n hadoop $(getent group ${GID} | cut -d: -f1) \
    && useradd --shell /bin/bash -u ${UID} -g ${GID} -m hadoop \
    && echo "hadoop ALL=NOPASSWD: /usr/sbin/service" >> /etc/sudoers \
    # && echo -e "hadoop\nhadoop" | passwd hadoop \
    #&& echo -e "PasswordAuthentication no" >> /etc/ssh/sshd_config \
    && mkdir -p ${HADOOP_INSTALL_DIR} && chown -R hadoop:hadoop ${HADOOP_INSTALL_DIR}

WORKDIR $HADOOP_INSTALL_DIR
COPY --chown=hadoop:hadoop --from=hadoop-dev /hadoop .

FROM alpine as hive-dev
ENV HIVE_VERSION=hive-3.1.2
RUN wget https://dlcdn.apache.org/hive/${HIVE_VERSION}/apache-${HIVE_VERSION}-bin.tar.gz \
    && tar -xzf apache-${HIVE_VERSION}-bin.tar.gz \
    && mv apache-${HIVE_VERSION}-bin hive
RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-j-8.0.32.tar.gz &&\
    tar -xzf  mysql-connector-j-8.0.32.tar.gz &&\
    mv mysql-connector-j-8.0.32/mysql-connector-j-8.0.32.jar /hive/lib/mysql-connector-java.jar


FROM hadoop as hive
ARG HIVE_INSTALL_DIR="/opt/hive"
RUN mkdir -p ${HIVE_INSTALL_DIR} && chown -R hadoop:hadoop ${HIVE_INSTALL_DIR}
WORKDIR $HIVE_INSTALL_DIR
COPY --chown=hadoop:hadoop --from=hive-dev /hive .
RUN echo "export HADOOP_HOME=/opt/hadoop" >> $HIVE_INSTALL_DIR/bin/hive-config.sh 
RUN rm lib/guava-* && cp /opt/hadoop/share/hadoop/hdfs/lib/guava* lib/

FROM alpine as spark-dev
ENV SPARK_VERSION=spark-3.2.3
RUN wget https://dlcdn.apache.org/spark/${SPARK_VERSION}/${SPARK_VERSION}-bin-hadoop3.2.tgz \
    && tar -xf ${SPARK_VERSION}-bin-hadoop3.2.tgz \
    && mv ${SPARK_VERSION}-bin-hadoop3.2 /spark


FROM hive as hive-spark 
ENV PYTHONUNBUFFERED=1
RUN  apt-get -y install python3-pip 
# RUN apt-get -y install scala 
RUN wget https://downloads.lightbend.com/scala/2.12.17/scala-2.12.17.deb
RUN apt-get -y install ./scala-2.12.17.deb && rm scala-2.12.17.deb
RUN pip3 install --upgrade pip
RUN pip3 install pyspark==3.2.3 \
    && pip3 install Jupyter \
    && pip3 install jupyter_contrib_nbextensions \
    && pip3 install jupyter_nbextensions_configurator
RUN jupyter contrib nbextension install --symlink  \
    && jupyter nbextensions_configurator enable 
ARG SPARK_INSTALL_DIR="/opt/spark"
RUN mkdir -p ${SPARK_INSTALL_DIR} && chown -R hadoop:hadoop ${SPARK_INSTALL_DIR}
WORKDIR $SPARK_INSTALL_DIR
COPY --chown=hadoop:hadoop --from=spark-dev /spark .
RUN cp ${HIVE_INSTALL_DIR}/lib/mysql-connector-java.jar ${SPARK_INSTALL_DIR}/jars/

FROM alpine as livy-dev
ENV LIVY_VERSION=0.8.0
#RUN wget https://dlcdn.apache.org/incubator/livy/${LIVY_VERSION}-incubating/apache-livy-${LIVY_VERSION}-incubating-bin.zip &&\
#    unzip apache-livy-${LIVY_VERSION}-incubating-bin.zip &&\
#    mv apache-livy-${LIVY_VERSION}-incubating-bin /livy
ADD  ./livy/incubator-livy.tgz ./
RUN mv /incubator-livy /livy

RUN echo "export PYTHONPATH=/opt/spark/python/lib/py4j-0.10.9.5-src.zip:/opt/spark/python/:$PYTHONPATH" \
    >> /livy/conf/livy-env.sh

FROM hive-spark as hive-spark-livy
ARG LIVY_INSTALL_DIR="/opt/livy"
RUN mkdir -p ${LIVY_INSTALL_DIR} && chown -R hadoop:hadoop ${LIVY_INSTALL_DIR}
WORKDIR $LIVY_INSTALL_DIR
COPY --chown=hadoop:hadoop --from=livy-dev /livy .

FROM alpine as hbase-dev
ENV HBASE_VERSION=2.5.2
RUN wget https://dlcdn.apache.org/hbase/${HBASE_VERSION}/hbase-${HBASE_VERSION}-hadoop3-bin.tar.gz \
    && tar -xzf hbase-${HBASE_VERSION}-hadoop3-bin.tar.gz \
    && mv hbase-${HBASE_VERSION}-hadoop3 /hbase

FROM hive-spark-livy AS hive-spark-hbase
ARG HBASE_INSTALL_DIR="/opt/hbase"
RUN mkdir -p ${HBASE_INSTALL_DIR} && chown -R hadoop:hadoop ${HBASE_INSTALL_DIR}
WORKDIR $HBASE_INSTALL_DIR
COPY --chown=hadoop:hadoop --from=hbase-dev /hbase .

FROM alpine as flume-dev
ENV FLUME_VERSION=1.11.0
RUN wget https://dlcdn.apache.org/flume/${FLUME_VERSION}/apache-flume-${FLUME_VERSION}-bin.tar.gz \
    && tar -xzf apache-flume-${FLUME_VERSION}-bin.tar.gz \
    && mv apache-flume-${FLUME_VERSION}-bin /flume

FROM hive-spark-hbase as hive-spark-hbase-flume
ARG FLUME_INSTALL_DIR="/opt/flume"
RUN mkdir -p ${FLUME_INSTALL_DIR} && chown -R hadoop:hadoop ${FLUME_INSTALL_DIR}
WORKDIR $FLUME_INSTALL_DIR
COPY --chown=hadoop:hadoop --from=flume-dev /flume .
RUN rm lib/guava-* && cp /opt/hadoop/share/hadoop/hdfs/lib/guava* lib/

FROM hive-spark-hbase-flume as runtime
USER hadoop
WORKDIR /home/hadoop
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa \
    && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys 
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/ 
# --- HADOOP VAR
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop 
ENV PATH=${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin 
# --- HIVE VAR
ENV HIVE_HOME=/opt/hive
ENV PATH=${PATH}:${HIVE_HOME}/bin
# --- SPARK VAR
ENV SPARK_HOME=/opt/spark
ENV LD_LIBRARY_PATH=${HADOOP_HOME}/lib/native:$LD_LIBRARY_PATH
ENV PATH=${PATH}:$SPARK_HOME/bin
# --- LIVY VAR
ENV LIVY_HOME=/opt/livy
ENV PATH=${PATH}:$LIVY_HOME/bin
# --- HBASE VAR
ENV HBASE_HOME=/opt/hbase
ENV PATH=$PATH:$HBASE_HOME/bin
# FUME
ENV FLUME_HOME=/opt/flume
ENV PATH=$PATH:$FLUME_HOME/bin

COPY ./hadoop-entrypoint.sh .
ENTRYPOINT ["/bin/bash","./hadoop-entrypoint.sh"]  
