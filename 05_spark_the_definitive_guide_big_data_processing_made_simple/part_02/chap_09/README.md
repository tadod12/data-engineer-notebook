# Chapter 9. Data Sources

## The Structure of the Data Sources API

### Read API Structure

The core structure for reading data

    DataFrameReader.format(...).option("key", "value").schema(...).load()

- `format` is optional because by default Spark will use the Parquet format
- `option` allows you to set key-value configuration to parameterize how you will read data
- `schema` is optional if the date source provides a schema or if you intend to use schema inference

### Basics of Reading Data

`DataFrameReader` can be accessed through the `SparkSession` via the `read` attribute

    spark.read

After we have a DataFrame reader, we specify several values: The _format_, _schema_, _read mode_, series of _option_

    spark.read.format("csv")
      .option("mode", "FAILFAST")
      .option("inferSchema", "true")
      .option("path", "path/to/file(s)")
      .schema(someSchema)
      .load()

**Read modes (option "mode")**

- `permissive`: (default) Set all fields to `null` when it encounters a corrupted record and places all corrupted
  records in a string called `_corrupt_record`
- `dropMalformed`: Drops the row that contains malformed records
- `failFast`: Fails immediately upon encountering malformed records

> _malformed_ - Không đúng định dạng

### Write API Structure

The core structure of writing data

    DataFrameWriter.format(...).option(...).partitionBy(...).bucketBy(...).sortBy(...).save()

- `format` is optional because Spark will use the parquet format by default
- `option` configures how to write our given data
- `partitionBy` and `sortBy` work only for file-based data sources

### Basics of Writing Data

Access the DataFrameWriter on a per-`DataFrame` basis via the `write` attribute

    dataFrame.write

    dataFrame.write.format("csv")
      .option("mode", "OVERWRITE")
      .option("dateFormat", "yyyy-MM-dd")
      .option("path", "path/to/file(s)")
      .save()

**Save modes**

- `append`: Appends the output files to the list of files that already exist at that location
- `overwrite`: Completely overwrite any data that already exists there
- `errorIfExists` : Throws an error and fails the write if data or files already exist at the specified location
- `ignore`: If data or files exist at the location, do nothing with the current DataFrame

## CSV Files

CSV stands for comma-separated values. This is a common text file format in which each line represents a single record,
and commas separate each field within a record. CSV files, while seeming well-structured, are actually one of the
trickiest file formats you will encounter because not many assumptions can be made in production scenarios about what
they contain or how they are structured

CSV Options: https://spark.apache.org/docs/latest/sql-data-sources-csv.html

### Reading CSV Files

First create a `DataFrameReader`

    spark.read.format("csv")

Using option to specify ...

    spark.read.format("csv")
      .option("header", "true")
      .option("mode", "FAILFAST")
      .option("inferSchema", "true")
      .load("some/path/to/file.csv")

Using schema we create

    val myManualSchema = new StructType(Array(
      new StructField("DEST_COUNTRY_NAME", StringType, true),
      new StructField("ORIGIN_COUNTRY_NAME", StringType, true),
      new StructField("count", LongType, false)
    ))

    spark.read.format("csv")
      .option("header", "true")
      .option("mode", "FAILFAST")
      .schema(myManualSchema)
      .load("D:\\repo_books\\book_sparkthedefinitiveguide\\data\\flight-data\\csv\\2010-summary.csv")
      .show(5, truncate = false)

### Writing CSV Files

    csvDF.write.format("csv")
      .mode("overwrite")
      .option("sep", "\t")
      .save("D:\\repo_books\\spark_chap09\\output\\my-tsv-files")  // folder

`my-tsv-files` is a folder with numerous files within it. This actually reflects the number of partitions in our
DataFrame at the time we write it out. If we were to repartition our data before then, we would end up with a different
number of files

## JSON Files

In Spark, when we refer to JSON files, we refer to _line-delimited_ JSON files

JSON data source options: https://spark.apache.org/docs/latest/sql-data-sources-json.html

Line-delimited JSON is actually a much more stable format because it allows you to append to a file with a new record (
rather than having to read in an entire file and then write it out), which is what we recommend that you use

    spark.read.format("json")

### Reading JSON Files

    spark.read.format("json")
      .option("mode", "FAILFAST")
      .schema(myManualSchema)
      .load("D:\\repo_books\\book_sparkthedefinitiveguide\\data\\flight-data\\json\\2010-summary.json")
      .show(5)

### Writing JSON Files

Writing JSON files is just as simple as reading them, and, as you might expect, the data source does not matter.
Therefore, we can reuse the CSV DataFrame that we created earlier to be the source for our JSON file

    // json writer
    csvDF.write.format("json")
      .mode("overwrite")
      .save("D:\\repo_books\\spark_chap09\\output\\my-json-files")

## Parquet Files (Apache Spark default format)

Parquet is an open source column-oriented data store that provides a variety of storage optimizations, especially for
analytics workload.It provides columnar compression, which saves storage space and allows for reading individual columns
instead of entire files. Another advantage of Parquet is that it supports complex types. This means that if your column
is an array (which would fail with a CSV file, for example), map, or struct, you’ll still be able to read and write that
file without issue

    spark.read.format("parquet")

### Reading Parquet Files

Parquet has very few options because it enforces its own schema when storing data. Thus, all you need to set is the
format, and you are good to go

![parquet source options.png](parquet%20source%20options.png)

### Writing Parquet Files

    // parquet writer
    csvDF.write.format("parquet").mode("overwrite")
      .save("D:\\repo_books\\spark_chap09\\output\\my-parquet-files")

![parquet write auto.png](parquet%20write%20auto.png)

## ORC Files

ORC is a self-describing, type-aware columnar file format designed for Hadoop workloads. It is optimized for large
streaming reads, but with integrated support for finding required rows quickly. ORC actually has no options for reading
in data because Spark understands the file format quite well.

> The fundamental difference is that Parquet is further optimized for use with Spark, whereas ORC is further optimized
> for Hive

### Reading Orc Files

    // orc reader
    spark.read.format("orc")
      .load("D:\\repo_books\\book_sparkthedefinitiveguide\\data\\flight-data\\orc\\2010-summary.orc")
      .show(5)

### Writing Orc Files

    // orc writer
    csvDF.write.format("orc").mode("overwrite")
      .save("output/my-orc-files")

## SQL Databases

SQL data sources are one of the more powerful connectors because there are a variety of systems to which you can
connect (as long as that system speaks SQL)

SQLite

    // sqlite reader
    val dbDataFrame = spark.read.format("jdbc")
      .option("url", "jdbc:sqlite:D:\\repo_books\\spark_chap09\\sql-input\\my-sqlite.db")
      .option("dbtable", "flight_info")
      .option("driver", "org.sqlite.JDBC")
      .load()
    dbDataFrame.show(5, truncate = false)
    // or: .option("url", "jdbc:sqlite:sql-input/my-sqlite.db")

> quit sqlite3 cmd: `.quit` + `ENTER`

### Query Pushdown

Spark makes a best-effort attempt to filter data in the database itself before creating the DataFrame

    db.DataFrame.select("DEST_COUNTRY_NAME").distinct().explain

    == Physical Plan ==
    AdaptiveSparkPlan isFinalPlan=false
    +- HashAggregate(keys=[DEST_COUNTRY_NAME#93], functions=[])
      +- Exchange hashpartitioning(DEST_COUNTRY_NAME#93, 200), ENSURE_REQUIREMENTS, [plan_id=113]
        +- HashAggregate(keys=[DEST_COUNTRY_NAME#93], functions=[])
          +- Scan JDBCRelation(flight_info) [numPartitions=1] [DEST_COUNTRY_NAME#93] PushedFilters: [], ReadSchema: struct<DEST_COUNTRY_NAME:string>

Spark can actually do better than this on certain queries. If we specify a filter on our DataFrame, Spark will push that
filter down into the database:

    dbDataFrame.filter("DEST_COUNTRY_NAME in ('Anguilla', 'Sweden')").explain

    == Physical Plan ==
    *(1) Scan JDBCRelation(flight_info) [numPartitions=1] [DEST_COUNTRY_NAME#93,ORIGIN_COUNTRY_NAME#94,count#95] 
    PushedFilters: [*In(DEST_COUNTRY_NAME, [Anguilla,Sweden])], 
    ReadSchema: struct<DEST_COUNTRY_NAME:string,ORIGIN_COUNTRY_NAME:string,count:decimal(20,0)>

Spark can’t translate all of its own functions into the functions available in the SQL database in which you’re working.
Therefore, sometimes you’re going to want to pass an entire query into your SQL that will return the results as a
DataFrame

    // pass entire query into sql for pushdown
    val pushdownQuery = """
      (SELECT DISTINCT(DEST_COUNTRY_NAME) FROM flight_info)
      AS flight_info
    """

    val dbDataFrame1 = spark.read.format("jdbc")
      .option("url", "jdbc:sqlite:sql-input/my-sqlite.db")
      .option("dbtable", pushdownQuery)
      .option("driver", "org.sqlite.JDBC")
      .load()

    dbDataFrame1.explain()

    == Physical Plan ==
    *(1) Scan JDBCRelation((SELECT DISTINCT(DEST_COUNTRY_NAME) FROM flight_info)
    AS flight_info) [numPartitions=1] [DEST_COUNTRY_NAME#113] PushedFilters: [], 
    ReadSchema: struct<DEST_COUNTRY_NAME:string>

**Reading from databases in parallel**

All throughout this book, we have talked about partitioning and its importance in data processing. Spark has an
underlying algorithm that can read multiple files into one partition, or conversely, read multiple partitions out of one
file, depending on the file size and the “splitability” of the file type and compression

    val dbDataFrame = spark.read.format("jdbc")
      .option("url", "jdbc:sqlite:sql-input/my-sqlite.db")
      .option("dbtable", "flight_info")
      .option("driver", "org.sqlite.JDBC")
      .option("numPartitions", 10).load()

In this case, this will still remain as one partition because there is not too much data. However, this configuration
can help you ensure that you do not overwhelm the database when reading and writing data

This optimization allows you to control the physical location of certain data in certain partitions by specifying
predicates. We only need data from two countries in our data: Anguilla and Sweden. We could filter these down and have
them pushed into the database, but we can also go further by having them arrive in their own partitions in Spark. We do
that by specifying a list of predicates when we create the data source

    // in Scala
    val props = new java.util.Properties
    props.setProperty("driver", "org.sqlite.JDBC")
    val predicates = Array(
      "DEST_COUNTRY_NAME = 'Sweden' OR ORIGIN_COUNTRY_NAME = 'Sweden'",
      "DEST_COUNTRY_NAME = 'Anguilla' OR ORIGIN_COUNTRY_NAME = 'Anguilla'")
    spark.read.jdbc(url, tablename, predicates, props).show()
    spark.read.jdbc(url, tablename, predicates, props).rdd.getNumPartitions // 2

**Partition based on a sliding window**

Let’s take a look to see how we can partition based on predicates. In this example, we’ll partition based on our
numerical count column. Here, we specify a minimum and a maximum for both the first partition and last partition.
Anything outside of these bounds will be in the first partition or final partition. Then, we set the number of
partitions we would like total (this is the level of parallelism). Spark then queries our database in parallel and
returns numPartitions partitions

    // partition sliding window
    val colName = "count"
    val lowerBound = 0L
    val upperBound = 348113L // max count in database
    val numPartitions = 10

    spark.read.jdbc(
      url = "jdbc:sqlite:sql-input/my-sqlite.db",
      table = "flight_info", colName,
      lowerBound = lowerBound,
      upperBound = upperBound,
      numPartitions = numPartitions,
      props
    ).count()

### Writing to SQL Database

You simply specify the URI and write out the data according to the specified write mode that you want

    // writing to sql databases
    val newPath = "jdbc:sqlite:sql-output/my-sqlite.db"
    csvDF.write.mode("overwrite").jdbc(newPath, table = "flight_info", props)
    // check
    spark.read.jdbc(newPath, table = "flight_info", props).count()

    // append
    csvDF.write.mode("append").jdbc(newPath, table = "flight_info", props)
    spark.read.jdbc(newPath, "flight_info", props).count()

## Text Files

Each line in the file becomes a record in the DataFrame. Text files make a great argument for the Dataset API due to its
ability to take advantage of the flexibility of native types

### Reading Text Files

Reading text files is straightforward: you simply specify the type to be `textFile`. With `textFile`, partitioned
directory names are ignored. To read and write text files according to partitions, you should use `text`, which respects
partitioning on reading and writing

    // text files reader
    spark.read.textFile("D:\\repo_books\\book_sparkthedefinitiveguide\\data\\flight-data\\csv\\2010-summary.csv")
      .show()

    spark.read.textFile("D:\\repo_books\\book_sparkthedefinitiveguide\\data\\flight-data\\csv\\2010-summary.csv")
      .selectExpr("split(value, ',') as rows").show()

### Writing Text Files

When you write a text file, you need to be sure to have only one string column; otherwise, the write will fail

    // text files writer
    csvDF.select("DEST_COUNTRY_NAME").write.text("output/my-text-files/no-partition.txt")

If you perform some partitioning when performing your write (we’ll discuss partitioning in the next couple of pages),
you can write more columns. However, those columns will manifest as directories in the folder to which you’re writing
out to, instead of columns on every single file

    csvDF.limit(10).select("DEST_COUNTRY_NAME", "count")
      .write.partitionBy("count").text("output/my-text-files/partitions.txt")

## Advanced I/O Concepts

We saw previously that we can control the parallelism of files that we write by controlling the partitions prior to
writing. We can also control specific data layout by controlling two things: _bucketing_ and _partitioning_

### Splittable File Types and Compression

Certain file formats are fundamentally “splittable.” This can improve speed because it makes it possible for Spark to
avoid reading an entire file, and access only the parts of the file necessary to satisfy your query. Additionally if
you’re using something like Hadoop Distributed File System (HDFS), splitting a file can provide further optimization if
that file spans multiple blocks. In conjunction with this is a need to manage compression. Not all compression schemes
are splittable. How you store your data is of immense consequence when it comes to making your Spark jobs run smoothly.
We recommend Parquet with gzip compression.

### Reading Data in Parallel

Multiple executors cannot read from the same file at the same time necessarily, but they can read different files at the
same time. In general, this means that when you read from a folder with multiple files in it, each one of those files
will become a partition in your DataFrame and be read in by available executors in parallel (with the remaining queueing
up behind the others)

### Writing Data in Parallel

The number of files or data written is dependent on the number of partitions the DataFrame has at the time you write out
the data. For example, the following code

    csvFile.repartition(5).write.format("csv").save("/tmp/multiple.csv")

will end up with five files inside of that folder

**Partitioning**

Partitioning is a tool that allows you to control what data is stored (and where) as you write it. When you write a file
to a partitioned directory (or table), you basically encode a column as a folder. What this allows you to do is skip
lots of data when you go to read it in later, allowing you to read in only the data relevant to your problem instead of
having to scan the complete dataset

    // in Scala
    csvFile.limit(10).write.mode("overwrite").partitionBy("DEST_COUNTRY_NAME")
      .save("/tmp/partitioned-files.parquet")

    $ ls /tmp/partitioned-files.parquet
    ...
    DEST_COUNTRY_NAME=Costa Rica/
    DEST_COUNTRY_NAME=Egypt/
    DEST_COUNTRY_NAME=Equatorial Guinea/
    DEST_COUNTRY_NAME=Senegal/
    DEST_COUNTRY_NAME=United States/

> Each of these will contain Parquet files that contain that data where the previous predicate was true

**Bucketing**

Bucketing is another file organization approach with which you can control the data that is specifically written to each
file. This can help avoid shuffles later when you go to read the data because data with the same bucket ID will all be
grouped together into one physical partition. This means that the data is prepartitioned according to how you expect to
use that data later on, meaning you can avoid expensive shuffles when joining or aggregating

Rather than partitioning on a specific column (which might write out a ton of directories), it’s probably worthwhile to
explore bucketing the data instead. This will create a certain number of files and organize our data into those
“buckets”

    val numberBuckets = 10
    val columnToBucketBy = "count"
    csvFile.write.format("parquet").mode("overwrite")
      .bucketBy(numberBuckets, columnToBucketBy).saveAsTable("bucketedFiles")

    $ ls /user/hive/warehouse/bucketedfiles/
    part-00000-tid-1020575097626332666-8....parquet
    part-00000-tid-1020575097626332666-8....parquet
    part-00000-tid-1020575097626332666-8....parquet
    ...

> Bucketing is supported only for Spark-managed tables