# Chapter 1. What Is Apache Spark

Apache Spark is a unified computing engine and a set of libraries for parallel data processing on computer clusters.

![spark toolkit.png](spark%20toolkit.png)

## Apache Spark's Philosophy

- Unified: Spark is designed to support a wide range of data analytics tasks, ranging from simple data loading and SQL
  queries to machine learning and streaming computation, over the same computing engine and with a consistent set of
  APIs.

- Computing engine: Spark handles loading data from storage systems and performing computation on it, not permanent
  storage as the end itself. You can use Spark with a wide variety of persistent storage systems, including cloud
  storage systems such as Azure Storage and Amazon S3, distributed file systems such as Apache Hadoop, key-value
  stores such as Apache Cassandra, and message buses such as Apache Kafka.

- Libraries: Spark supports both standard libraries that ship with the engine and a wide array of external libraries
  published as third-party packages by the open source communities. Spark includes libraries for SQL and structured
  data (Spark SQL), machine learning (MLlib), stream processing (Spark Streaming and the newer Structured Streaming),
  and graph analytics (GraphX).

## Running Spark

### Downloading Spark Locally

I'm using Spark 3.1.2 and Hadoop 3.2.2

### Launching Spark's Interactive Consoles

#### Launching the Python console

    > pyspark

#### Launching the Scala console

    > spark-shell

#### Launching the SQL console

    > spark-sql

## Running Spark in the Cloud

Using Databricks Community Edition

## Data Used

https://github.com/databricks/Spark-The-Definitive-Guide
