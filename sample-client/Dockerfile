# Jars are only for 3.4
# FROM apache/spark:3.5.1-scala2.12-java17-python3-r-ubuntu
FROM apache/spark:3.4.2-scala2.12-java11-python3-r-ubuntu
USER root
RUN apt-get update
RUN apt-get install -y software-properties-common && \
    add-apt-repository universe && \
    apt-get install -y neovim && \
    apt-get install -y wget && \
    apt-get install -y python3 python3-pip python3-venv

# Install binary version of ttyd
RUN bash -c 'set -ex && \
wget https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.$(uname -m) -O /opt/ttyd ;'
RUN chmod a+x /opt/ttyd

# This part is only needed for sample python code.
# Set up venv, install dependencies and pack the virtual environment using venv-pack
RUN mkdir -p /opt/sample-code
WORKDIR /opt/sample-code
RUN python3 -m venv .
RUN bash -c 'set -ex && \
source bin/activate && \
pip install pyspark snowflake-snowpark-python[pandas] venv-pack && \
venv-pack -o pyspark_venv.tar.gz;'
# spark-submit needs permissions on this file
RUN chmod a+rw pyspark_venv.tar.gz

# Get jars
RUN mkdir -p /opt/sample-code/jars
WORKDIR /opt/sample-code/jars
RUN wget https://repo1.maven.org/maven2/net/snowflake/spark-snowflake_2.12/2.16.0-spark_3.4/spark-snowflake_2.12-2.16.0-spark_3.4.jar
RUN wget https://repo1.maven.org/maven2/net/snowflake/snowflake-jdbc/3.16.1/snowflake-jdbc-3.16.1.jar

# Place code
COPY ./sample-python-code.py /opt/sample-code

# Place sample runner
COPY ./sample-spark-submit /opt/sample-code
RUN chmod a+x /opt/sample-code/sample-spark-submit

USER spark
EXPOSE 7681/tcp
ENV PATH="${PATH}:/opt/spark/bin"
WORKDIR /opt/sample-code
ENTRYPOINT /opt/ttyd --writable bash
