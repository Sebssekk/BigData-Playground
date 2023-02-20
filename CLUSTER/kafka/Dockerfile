FROM alpine

RUN apk add --no-cache shadow && \
    apk add --no-cache openjdk11 &&\
    apk add --no-cache bash

ARG UID=1000
ARG GID=1000
ARG KAFKA_INSTALL_DIR="/opt/kafka"
RUN groupadd -g ${GID} kafka || groupmod -n kafka $(getent group ${GID} | cut -d: -f1) \
    && useradd --shell /bin/bash -u ${UID} -g ${GID} -m kafka \
    && mkdir -p ${KAFKA_INSTALL_DIR} && chown -R kafka:kafka ${KAFKA_INSTALL_DIR}

WORKDIR $KAFKA_INSTALL_DIR

ENV KAFKA_VERSION=3.3.2
ENV SCALA_VERSION=2.13

RUN wget https://downloads.apache.org/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
    && tar -xzf kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz --strip 1 \
    && rm kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz

USER kafka

ENTRYPOINT ["bin/kafka-server-start.sh" , "config/server.properties"]
