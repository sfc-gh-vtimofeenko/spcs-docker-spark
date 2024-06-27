# Jars are only for 3.4
# FROM apache/spark:3.5.1-scala2.12-java17-python3-r-ubuntu
FROM apache/spark:3.4.2-scala2.12-java11-python3-r-ubuntu
EXPOSE 8081/tcp
ENTRYPOINT /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077
