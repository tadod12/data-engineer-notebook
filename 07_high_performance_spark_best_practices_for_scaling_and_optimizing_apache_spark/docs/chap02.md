# Chapter 2 - How Spark Works

To get the most out of Spark, it is important to understand some of the principles used to design Spark and, at a cursory level, how Spark programs are executed

## How Spark Fits into the Big Data Ecosystem

![A diagram of the data processing ecosystem including Spark](img/spark_in_processing_ecosystem.png)

Spark currently supports three kinds of cluster managers
- Standalone Cluster Manager
- Apache Mesos
- Hadoop YARN

## Spark Components

- Spark Core: The main data processing framework in the Spark ecosystem, has APIs in Scala, Java, Python, and R
- First-party components: Spark SQl, Spark MLlib, Spark ML, Spark Streaming, and GraphX

> Spark SQL has a different query optimizer than Spark Core

_Spark SQL_ is a component that can be used in tandem with Spark Core and has APIs in Scala, Java, Python, and R, and basic SQL queries. Spark SQL defines an interface for a semi-structured data type, called `DataFrames`, and as of Spark 1.6, a semi-structured, typed version of RDDs called `Datasets`

Spark has two machine learning packages
- Spark MLlib: A package of machine learning and statistics algorithms written with Spark
- Spark ML: provides a higher-level API than MLlib with the goal of allowing users to more easily create practical machine learning pipelines

> Spark MLlib is primarily built on top of RDDs and uses functions from Spark Core, while ML is built on top of Spark SQL `DataFrames`. Eventually the Spark community plans to move over to ML and deprecate MLlib

Spark Streaming uses the scheduling of the Spark Core for streaming analytics on minibatches of data

GraphX is a graph processing framework built on top of Spark with an API for graph computations

> This book will focus on optimizing programs written with the Spark Core and Spark SQL

## Spark Model of Parallel Computing: RDDs

Spark represents large datasets as RDDs - immutable, distributed collections of objects - which are stored in the executors (or slave nodes). The objects that comprise RDDs are called partitions and may be (but do not need to be) computed on different nodes of a distributed system

![Starting a Spark application on a distributed system](img/start_spark_application.png)

### Lazy Evaluation

Evaluation of RDDs is completely lazy. Spark does not begin computing the partitions until an action is called

Actions trigger the scheduler, which builds a directed acyclic graph (called the DAG), based on the dependencies between RDD transformations. In other words, Spark evaluates an action by working backward to define the series of steps it has to take to produce each object in the final distributed dataset (each partition)

> Not all transformations are 100% lazy (`sortByKey` involves both a transformation and an action)

**Lazy evaluation and fault tolerance** - If a partition is lost, the RDD has enough information about its lineage to recompute it, and that computation can be parallelized to make recovery faster

**Lazy evaluation and debugging** - ...Even the stack trace will show the failure as first occurring at the collect step, suggesting that the failure came from the collect statement. For this reason it is probably most efficient to develop in an environment that gives you access to complete debugging information

### In-Memory Persistence and Memory Management

Rather than writing to disk between each pass through the data, Spark has the option of keeping the data on the executors loaded into memory

29/356

## Spark Job Scheduling
## The Anatomy of a Spark Job
## Conclusion