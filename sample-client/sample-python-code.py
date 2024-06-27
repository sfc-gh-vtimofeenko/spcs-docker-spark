"""Sample pyspark code that authenticates using Snowpark container services token and runs simple queries."""

from pyspark.sql import SparkSession
import snowflake.connector

import os


# SPCS injects an oauth token into the container and generates a per-service user.
# This code first retrieves the per-service user and then authenticates over JDBC using the token.
try:
    SPARK_MASTER = os.environ["SPARK_MASTER_URL"]
except KeyError:
    print(
        """SPARK_MASTER_URL is not specified as an environment variable.

          If this container is running in the same service in SPCS as master
          -- value could be 'spark://statefulset-0:7077'."""
    )
    raise

SNOWFLAKE_SOURCE_NAME = "net.snowflake.spark.snowflake"
# Auth stuff
SNOW_TOKEN_PATH = "/snowflake/session/token"
SNOW_HOST = os.getenv("SNOWFLAKE_HOST")
SNOW_PORT = os.getenv("SNOWFLAKE_PORT")
SNOW_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOW_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOW_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOW_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")


def _get_login_token():
    try:
        with open(SNOW_TOKEN_PATH, "r") as f:
            return f.read()
    except FileNotFoundError:
        print("""Looks like the token does not exist. Is this code running in SPCS?""")


token = _get_login_token()


def _get_snowflake_python_connection():
    return snowflake.connector.connect(
        host=SNOW_HOST,
        account=SNOW_ACCOUNT,
        token=token,
        # warehouse=SNOW_WAREHOUSE,
        authenticator="OAUTH",
        # role=SNOW_ROLE,
        client_session_keep_alive=True,
    )


snowflake_conn = _get_snowflake_python_connection()
snowflake_cur = snowflake_conn.cursor()
snowflake_cur.execute("SELECT CURRENT_USER()")
SNOW_USER = snowflake_cur.fetchall()[0][0]


sf_options = {
    "sfURL": SNOW_HOST + ":" + SNOW_PORT,
    "sfUser": SNOW_USER,
    "sfAccount": SNOW_ACCOUNT,
    "sfAuthenticator": "oauth",
    "sfToken": token,
    "sfDatabase": SNOW_DATABASE,
    "sfSchema": SNOW_SCHEMA,
    # "sfWarehouse" : SNOW_WAREHOUSE,
}

dependencies = []


# Sample code
def main(spark):
    """Show first 20 rows from sample dataset."""
    df = (
        spark.read.format(SNOWFLAKE_SOURCE_NAME)
        .options(**sf_options)
        .option("dbtable", "SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER")
        .load()
    )
    df.show()


if __name__ == "__main__":
    builder = (
        SparkSession.builder.appName("sample_spcs")
        .master(SPARK_MASTER)
        .config("spark.driver.extraClassPath", ":".join(dependencies))
        .getOrCreate()
    )

    main(builder)
