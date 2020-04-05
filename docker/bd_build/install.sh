#!/bin/bash
set -e
set -x
cd /etc/apt && mv sources.list sources.list.bck  && cp /bd_build/sources.list /etc/apt/sources.list  && \
apt-get update && DEBIAN_FRONTEND=noninteractive && \
apt -y upgrade && \
apt-get install -y --no-install-recommends net-tools libsasl2-dev curl wget procps netcat git libnss3-tools && \
apt-get install -y freetds-bin freetds-common freetds-dev libct4 libsybdb5 python3-dev python3 python3-setuptools python3-pip build-essential unzip python-dev libaio-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python && python --version \
  && cd /etc && cp /bd_build/pip.conf . && cd - \
  && python -m pip install pip --upgrade \
  && python -m pip install wheel && \
cd /opt && cp /bd_build/pyapi.1.1.2.tar.gz . && tar -xzf pyapi.1.1.2.tar.gz && rm pyapi.1.1.2.tar.gz && \
cd /opt/pyAPI && chmod 755 mkcert-v1.4.1-linux-amd64 && mv mkcert-v1.4.1-linux-amd64 /bin/mkcert && mkdir -p /opt/pyAPI/log /opt/pyAPI/cert && \
mkcert -install && \
mkcert -cert-file /opt/pyAPI/cert/cert.pem -key-file /opt/pyAPI/cert/cert-key.pem zino.com "*.zino.com" zino.test localhost 127.0.0.1 ::1 && \
pip install virtualenv  && \
virtualenv venv && \
. venv/bin/activate && \
cd /opt/ && \
wget https://download.oracle.com/otn_software/linux/instantclient/19600/instantclient-basic-linux.x64-19.6.0.0.0dbru.zip && \
wget https://download.oracle.com/otn_software/linux/instantclient/19600/instantclient-sdk-linux.x64-19.6.0.0.0dbru.zip && \
unzip instantclient-basic-linux.x64-19.6.0.0.0dbru.zip  && \
unzip instantclient-sdk-linux.x64-19.6.0.0.0dbru.zip  && \
mv instantclient_19_6 instantclient && \
ls instantclient/ && \
rm instantclient-basic-linux.x64-19.6.0.0.0dbru.zip && \
rm instantclient-sdk-linux.x64-19.6.0.0.0dbru.zip  && \
export ORACLE_HOME=/opt/instantclient && \
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME && \
echo "ORACLE_HOME=/opt/instantclient" > /etc/ld.so.conf.d/oracle.conf && \
ldconfig  && \
cd /opt/pyAPI && \
pip install -r requirments.txt && \
pip install dataset && \
pip install fastapi[all] && \
pip install pyhive[hive] && \
pip install pyhive[presto] && \
pip install elasticsearch-dbapi && \
pip install sqlalchemy-clickhouse && \
cp /bd_build/entrypoint.sh  /opt/ && \
rm /opt/pyAPI/venv/lib/python3.6/site-packages/sqlalchemy_clickhouse/connector.py && \
cp /bd_build/connector.py  /opt/pyAPI/venv/lib/python3.6/site-packages/sqlalchemy_clickhouse/connector.py
rm /opt/pyAPI/venv/lib/python3.6/site-packages/sqlalchemy_clickhouse/base.py && \
cp /bd_build/base.py  /opt/pyAPI/venv/lib/python3.6/site-packages/sqlalchemy_clickhouse/base.py
#cp /bd_build/config_template.py  /opt/pyAPI/config/config_template.py




