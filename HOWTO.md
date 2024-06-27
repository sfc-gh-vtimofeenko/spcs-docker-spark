# Setup

## Prerequisites

1. `snowcli`: [install instructions][snow-install]
2. `docker` (with `compose`)
3. `make`
4. Snowflake account with SPCS
5. SNOWFLAKE_SAMPLE_DATA dataset that is accessible to PUBLIC role

## Running locally

1. Clone this repo
2. `make run`
3. Open http://localhost:7681 (the "sample-client" port) in your browser
4. `pyspark --master spark://spark-master:7077`
5. Run in Python:

    ```python
    n = sc.parallelize(range(1000))
    print(n.map(lambda x: x*x).collect())

    ```
6. Observe via spark-master's webui at http://localhost:8080

## Running in SPCS

1. Clone this repo
2. [Configure `snow` connection][snow-config]
3. Set up your Snowflake environment
    - [Image registry][image-registry]
    - [Compute pool][compute-pool]
4. On your local machine:
    1. Add `REPOSITORY_URL` pointing to your SPCS repository to your shell
       environment (for example, `export
       REPOSITORY_URL="<orgName>-<accName>/spcs/repo/spcs_repo"`)
    2. Run `make all`
5. In Snowflake, create a `SERVICE`.

    Replace "`/spcs/repo/spcs_repo`" with the path to your image repository.

    <details>
      <summary>Service creation command</summary>
      
      ```sql
    CREATE SERVICE SPARK_STANDALONE
      IN COMPUTE POOL SCRATCH_COMPUTE_POOL
      QUERY_WAREHOUSE = <whName>
      FROM SPECIFICATION $$
    spec:
      containers:
        - name: spark-master
          image: /spcs/repo/spcs_repo/spark-master:latest
        - name: spark-worker
          image: /spcs/repo/spcs_repo/spark-worker:latest
          command:
            - /opt/spark/bin/spark-class
            - org.apache.spark.deploy.worker.Worker
            - spark://statefulset-0:7077
        - name: sample-client
          image: /spcs/repo/spcs_repo/sample-client:latest
      endpoints:
        - name: webshell
          port: 7681
          public: true
        - name: spark-master
          port: 7077
          protocol: TCP
        - name: spark-master-webui
          port: 8080
          public: true
        - name: spark-worker-webui
          port: 8081
      networkPolicyConfig:
        allowInternetEgress: true
    $$;
    ```
    </details>

5. Wait for the service to come online (`SELECT
   SYSTEM$GET_SERVICE_STATUS('SPARK_STANDALONE')`)
6. Access `webshell` endpoint (see `SHOW ENDPOINTS IN SERVICE SPARK_STANDALONE`) for the shell session and `spark-master-webui` for the master webui
7. Run `export SPARK_MASTER_URL="spark://$(hostname):7077"; source bin/activate; ./sample-spark-submit`
8. Monitor the console output for a set of rows from sample data

# Customizing

## Running as multiple services and/or multiple compute pools

Services in Snowflake can communicate over non-public endpoints. An approach to
scale the workers is to use [service-to-service][service-to-service]
communications and service scaling. The spark master URL can be passed to the
services as they start.

More information:

- Scaling compute pool nodes
- Scaling services

## Customizing the client environment

If you are not planning on using the shell environment, you can replace the
client with a jupyterlab container. The master URL can be provided as in
multiple services scenario above


[snow-install]: https://docs.snowflake.com/developer-guide/snowflake-cli-v2/installation/installation
[snow-config]: https://docs.snowflake.com/en/developer-guide/snowflake-cli-v2/connecting/connect
[image-registry]: https://docs.snowflake.com/developer-guide/snowpark-container-services/working-with-registry-repository
[compute-pool]: https://docs.snowflake.com/en/developer-guide/snowpark-container-services/working-with-compute-pool
[service-to-service]: https://docs.snowflake.com/en/developer-guide/snowpark-container-services/tutorials/advanced/tutorial-3#introduction
[compute-pool-scaling]: https://docs.snowflake.com/en/developer-guide/snowpark-container-services/working-with-compute-pool#autoscaling-of-compute-pool-nodes
[service-scaling]: https://docs.snowflake.com/en/developer-guide/snowpark-container-services/working-with-services#create-multiple-service-instances-and-configure-autoscaling
