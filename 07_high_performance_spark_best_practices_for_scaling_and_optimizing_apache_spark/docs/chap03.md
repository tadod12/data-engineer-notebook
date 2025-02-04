# Chapter 3 - DataFrames, Datasets, and Spark SQL

Spark SQL and its DataFrames and Datasets interfaces are the future of Spark performance, with more efficient storage options, advanced optimizer, and direct operations on serialized data

![Relative performance for RDD versus DataFrames based on SimplePerfTest computing aggregate average fuzziness of pandas](img/dataframes_versus_rdds.png)

> This chapter focus on how to best use Spark SQL's tools and how to intermix Spark SQL with traditional Spark operations

Like RDDs, `DataFrames` and `Datasets` represent distributed collections, with additional schema information not found in RDDs, provide a more efficient
- Storage layer (Tungsten)
- Optimization (Catalyst can perform additional optimizations)

> `DataFrames` are `Datasets` of a special Row object, which doesn’t provide any compile-time type checking

## Getting Started with the SparkSession (or Hive Context or SQLContext)

Much as the `SparkContext` is the entry point for all Spark applications, and the `StreamingContext` is for all streaming applications, the `SparkSession` serves as the entry point for Spark SQL

One of the more important shortcuts is `enableHiveSupport()`, which will give you access to Hive UDFs and _does not require_ a Hive installation—but does require certain extra JARs

    val spark = SparkSession
        .builder()
        .appName("chap03-01")
        .master("spark://spark-master:7077")
        .config("spark.executor.memory", "512m")
        .enableHiveSupport()
        .getOrCreate()

## Spark SQL Dependencies

Add Spark SQL and Hive component to sbt build
    
    libraryDependencies ++= Seq(
        "org.apache.spark" %% "spark-sql" % "2.0.0",
        "org.apache.spark" %% "spark-hive" % "2.0.0")

Add Spark SQL and Hive component to Maven pom file

    <dependency> <!-- Spark dependency -->
        <groupId>org.apache.spark</groupId>
        <artifactId>spark-sql_2.11</artifactId>
        <version>2.0.0</version>
    </dependency>
    <dependency> <!-- Spark dependency -->
        <groupId>org.apache.spark</groupId>
        <artifactId>spark-hive_2.11</artifactId>
        <version>2.0.0</version>
    </dependency>

## Basics of Schemas

The schema information, and the optimizations it enables, is one of the core differences between Spark SQL and core Spark

`printSchema()` will show us the schema of a DataFrame and is most commonly used when working in the shell to figure out what you are working with

    case class StructField(
        name: String,
        dataType: DataType,
        nullable: Boolean = true,
        metadata: Metadata = Metadata.empty)
    ....

The first part is a `StructType`, which contains a list of fields. It’s important to note you can nest `StructTypes`, like how a case class can contain additional case classes. The fields in the `StructType` are defined with `StructField`, which specifies the name, type and a Boolean indicating if the field may be null/missing

## DataFrame API

52/356

## Data Representation in DataFrames and Datasets

## Data Loading and Saving Functions

## Datasets

## Extending with User-Defined Functions and Aggregate Functions (UDFs, UDAFs)

## Query Optimizer

## Debugging Spark SQL Queries

## JDBC/ODBC Server

## Conclusion