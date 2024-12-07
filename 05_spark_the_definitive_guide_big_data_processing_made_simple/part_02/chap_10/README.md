# Chapter 10. Spark SQL

In a nutshell, with Spark SQL you can run SQL queries against views or tables organized into databases. You also can use
system functions or define user functions and analyze query plans in order to optimize their workloads

## What is SQL?

SQL or _Structured Query Language_ is a domain-specific language for expressing relational operations over data. It is
used in all relational databases, and many “NoSQL” databases create their SQL dialect in order to make working with
their databases easier

## Big Data and SQL: Apache Hive

Before Spark’s rise, Hive was the de facto big data SQL access layer. In many ways it helped propel Hadoop into
different industries because analysts could run SQL queries. Although Spark began as a general processing engine with
Resilient Distributed Datasets (RDDs), a large cohort of users now use Spark SQL

## Big Data and SQL: Spark SQL

The power of Spark SQL derives from several key facts: SQL analysts can now take advantage of Spark’s computation
abilities by plugging into the Thrift Server or Spark’s SQL interface, whereas data engineers and scientists can use
Spark SQL where appropriate in any data flow

### Spark's Relationship to Hive

Spark's SQL has a great relationship with Hive because it can connect to Hive metastores. The Hive metastore is the way
in which Hive maintains table information for use across sessions. With Spark SQL, you can connect to your Hive
metastore (if you already have one) and access table metadata to reduce file listing when accessing information

**The Hive metastore**

If you're connecting to Hive
metastore: https://spark.apache.org/docs/latest/sql-programming-guide.html#interacting-with-different-versions-of-hive-metastore

## How to Run Spark SQL Queries

### Spark SQL CLI

![spark sql cli.png](spark%20sql%20cli.png)

You configure Hive by placing your _hive-site.xml_, _core-site.xml_, and _hdfs-site.xml_ files in _conf/_

> For complete list of all available options: `spark-sql --help`

### Spark's Programmatic SQL Interface

In addition to setting up a server, you can also execute SQL in an ad hoc manner via any of Spark’s language APIs

    spark.sql("SELECT 1 + 1").show()

The command spark.sql("SELECT 1 + 1") returns a DataFrame that we can then evaluate programmatically. Just like other
transformations, this will not be executed eagerly but lazily. This is an immensely powerful interface because there are
some transformations that are much simpler to express in SQL code than in DataFrames.

You can completely interoperate between SQL and DataFrames

    spark.read.format("json")
      .load("D:\\repo_books\\book_sparkthedefinitiveguide\\data\\flight-data\\json\\2015-summary.json")
      .createOrReplaceTempView("some_sql_view") // DF to SQL

    spark.sql(
        """
      SELECT DEST_COUNTRY_NAME, SUM(count)
      FROM some_sql_view
      GROUP BY DEST_COUNTRY_NAME
      """)
      .where("DEST_COUNTRY_NAME LIKE 'S%'").where("`SUM(count)` > 10")
      .show()

### SparkSQL Thrift JDBC/ODBC Server

Spark provides a Java Database Connectivity (JDBC) interface by which either you or a remote program connects to the
Spark driver in order to execute Spark SQL queries. A common use case might be for a business analyst to connect
business intelligence software like Tableau to Spark

The Thrift JDBC/Open Database Connectivity (ODBC) server implemented here corresponds to the HiveServer2 in Hive 1.2.1

Start the JDBC/ODBC server

    C:\spark\bin> spark-class org.apache.spark.deploy.SparkSubmit --class org.apache.spark.sql.hive.thriftserver.HiveThriftServer2 spark-internal

![start thrift server.png](start%20thrift%20server.png)

Test connection

    beeline> !connect jdbc:hive2://localhost:10000

![connect using beeline.png](connect%20using%20beeline.png)

## Catalog

The highest level abstraction in Spark SQL is the Catalog. The Catalog is an abstraction for the storage of metadata
about the data stored in your tables as well as other helpful things like database, tables, functions, and views. The
catalog is available in the `org.apache.spark.sql.catalog.Catalog` package and contains a number of helpful functions
for doing things like listing tables, databases, and functions

## Tables

To do anything useful with Spark SQL, you first need to define tables. Tables are logically equivalent to a DataFrame in
that they are a structure of data against which you run commands. We can join tables, filter them, aggregate them, and
perform different manipulations that we saw in previous chapters.

> The core different between tables and DataFrames
> - You define DataFrame in the scope of a programming language
> - You define tables within a database. This means it will belong to the _default_ database

### Spark-Managed Tables

Tables store two important pieces of information. The data within the tables as well as the data about the tables -
_metadata_. You can have Spark manage the metadata for a set of files as well as for the data. When you define a table
from files on disk, you are defining an **unmanaged table**. When you use `saveAsTable` on a DataFrame, you are creating
a **managed table** for which Spark will track of the relevant information.

This will read your table and write it out to a new location in Spark format. You can see this reflected in the new
explain plan. In the explain plan, you will also notice that this writes to the default Hive warehouse location. You can
set this by setting the `spark.sql.warehouse.dir` configuration to the directory of your choosing when you create your
SparkSession. By default, Spark sets this to `/user/hive/warehouse`

See tables in a specific database

    SHOW TABLES IN databaseName

> If you are running on a new cluster or local mode, this should return zero results

### Creating Tables

Something fairly unique to Spark is the capability of reusing the entire Data Source API within SQL. This means that you
do not need to define a table and then load data into it; Spark lets you create one on the fly. You can even specify all
sorts of sophisticated options when you read in a file

    spark.sql("DROP TABLE IF EXISTS flights")

    // read from json, data write and read from path
    spark.sql(
      """
        CREATE TABLE flights (
          DEST_COUNTRY_NAME STRING,
          ORIGIN_COUNTRY_NAME STRING,
          count LONG COMMENT "ayo i can comment here"
        ) USING JSON
        OPTIONS (path 'D:/repo_books/book_sparkthedefinitiveguide/data/flight-data/json/2015-summary.json');
      """
    ).show()

    spark.sql("SELECT * FROM flights").show()

> Hive users can also use the STORED AS syntax to specify that this should be a Hive table.

Create a table from a query

    CREATE TABLE flights_from_select USING parquet AS SELECT * FROM flights

Create a table only if it does not currently exist

    CREATE TABLE IF NOT EXISTS flights_from_select
        AS SELECT * FROM flights

Control the layout of data by writing out a partitioned dataset

    // partitioned, output in spark-warehouse
    spark.sql(
      """
        CREATE TABLE partitioned_flights USING parquet PARTITIONED BY (DEST_COUNTRY_NAME)
          AS SELECT DEST_COUNTRY_NAME, ORIGIN_COUNTRY_NAME, count FROM flights LIMIT 5;
      """
    )

> These tables will be available in Spark even through sessions; temporary tables do not currently exist in Spark. You
> must create a temporary view, which we demonstrate later in this chapter.

### Creating External Tables

Hive was one of the first big data SQL systems, and Spark SQL is completely compatible with Hive SQL (HiveQL)
statements. One of the use cases that you might encounter is to port your legacy Hive statements to Spark SQL. Luckily,
you can, for the most part, just copy and paste your Hive statements directly into Spark SQL. For example, in the
example that follows, we create an unmanaged table. Spark will manage the table’s metadata; however, the files are not
managed by Spark at all. You create this table by using the CREATE EXTERNAL TABLE statement

You can view any files that have already been defined by running the following command

    CREATE EXTERNAL TABLE hive_flights (
        DEST_COUNTRY_NAME STRING,
        ORIGIN_COUNTRY_NAME STRING,
        count LONG
    ) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/data/flight-data-hive'

Create an external table from a select clause

    CREATE EXTERNAL TABLE hive_flights_2
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/data/flight-data-hive/' AS SELECT * FROM flights

### Inserting into Tables

    INSERT INTO flights_from_select
        SELECT DEST_COUNTRY_NAME, ORIGIN_COUNTRY_NAME, count FROM flights LIMIT 20

Provide a partition specification if you want to write only into a certain partition

    INSERT INTO partitioned_flights
        PARTITION (DEST_COUNTRY_NAME="UNITED STATES")
        SELECT count, ORIGIN_COUNTRY_NAME FROM flights
        WHERE DEST_COUNTRY_NAME='UNITED STATES' LIMIT 12

### Describing Table Metadata

    DESCRIBE TABLE flights;

The partitioning scheme for the data

    SHOW PARTITIONS partitioned_flights

### Refreshing Table Metadata

Maintaining table metadata is an important task to ensure that you’re reading from the most recent set of data. There
are two commands to refresh table metadata. REFRESH TABLE refreshes all cached entries (essentially, files) associated
with the table. If the table were previously cached, it would be cached lazily the next time it is scanned

    REFRESH table partitioned_flights

Another related command is REPAIR TABLE, which refreshes the partitions maintained in the catalog for that given table

    MSCK REPAIR TABLE partitioned_flights

### Dropping Tables

If you drop a managed table, both the data and the table definition will be removed

    DROP TABLE flights_csv;

Only delete a table if it already exists

    DROP TABLE IF EXISTS flights_csv;

If you are dropping unmanaged table, no data will be removed, but you will no longer be able to refer to this data by
the table name

### Caching Tables

    CACHE TABLE flights

    UNCACHE TABLE flights

## Views

A view specifies a set
of transformations on top of an existing table—basically just saved query plans, which can be convenient for organizing
or reusing your query logic. Spark has several different notions of views. Views can be global, set to a database, or
per session.

### Creating Views

    CREATE VIEW just_use_views AS
        SELECT * FROM flights WHERE DEST_COUNTRY_NAME = 'United States'

Create temporary views that are available only during the current session and are not registered to a database

    CREATE TEMP VIEW just_use_view_temp AS
        SELECT * FROM flights WHERE DEST_COUNTRY_NAME = 'United States'

Global temp views are resolved regardless of database and are viewable across the entire Spark application, but they are
removed at the end of the session

    CREATE GLOBAL TEMP VIEW just_usa_global_view_temp AS
        SELECT * FROM flights WHERE DEST_COUNTRY_NAME = 'United States'

    SHOW TABLES

Overwrite a view (both temp and regular)

    CREATE OR REPLACE TEMP VIEW just_use_view_temp AS
        SELECT * FROM flights WHERE DEST_COUNTRY_NAME = 'United States'

Query view just as if it were another table

    SELECT * FROM just_usa_view_temp

A view is effectively a transformation and Spark will perform it only at query time. This means that it will only apply
that filter after you actually go to query the table (and not earlier). Effectively, views are equivalent to creating a
new DataFrame from an existing DataFrame.

### Dropping Views

    DROP VIEW IF EXISTS just_usa_view;

## Databases

Databases are a tool for organizing tables. As mentioned earlier, if you do not define one, Spark will use the default
database. Any SQL statements that you run from within Spark (including DataFrame commands) execute within the context of
a database. This means that if you change the database, any user-defined tables will remain in the previous database and
will need to be queried differently

    SHOW DATABASES

### Creating Databases

    CREATE DATABASE some_db

### Setting the Database

    USE some_db

After you set this database, all queries will try to resolve table names to this database. Queries that were working
just fine might now fail or yield different results because you are in a different database:

    SHOW tables

    SELECT * FROM default.flights -- because USE some_db earlier

See what database you're currently using

    SELECT current_database()

Switch back to the default database

    USE default;

### Dropping Databases

    DROP DATABASE IF EXISTS some_db;

## Select Statements

Queries in Spark support the following ANSI SQL requirements

    SELECT [ALL|DISTINCT] named_expression[, named_expression, ...]
        FROM relation[, relation, ...]
        [lateral_view[, lateral_view, ...]]
        [WHERE boolean_expression]
        [aggregation [HAVING boolean_expression]]
        [ORDER BY sort_expressions]
        [CLUSTER BY expressions]
        [DISTRIBUTE BY expressions]
        [SORT BY sort_expressions]
        [WINDOW named_window[, WINDOW named_window, ...]]
        [LIMIT num_rows]
        
    named_expression:
        : expression [AS alias]
    
    relation:
        | join_relation
        | (table_name|query|relation) [sample] [AS alias]
        : VALUES (expressions)[, (expressions), ...]
        [AS (column_name[, column_name, ...])]
    
    expressions:
        : expression[, expression, ...]

    sort_expressions:
        : expression [ASC|DESC][, expression [ASC|DESC], ...]

### case...when...then Statements

    SELECT
        CASE WHEN DEST_COUNTRY_NAME = 'United States' THEN 1
             WHEN DEST_COUNTRY_NAME = 'Egypt' THEN 0
             ELSE -1 END
    FROM partitioned_flights

## Advanced Topics

### Complex Types

**Structs**

    CREATE VIEW IF NOT EXISTS nested_data AS
        SELECT (DEST_COUNTRY_NAME, ORIGIN_COUNTRY_NAME) AS country, count FROM flights

    SELECT * FROM nested_data

    SELECT country.DEST_COUNTRY_NAME FROM nested_data

**Lists**

If you’re familiar with lists in programming languages, Spark SQL lists will feel familiar. There are several ways to
create an array or list of values. You can use the collect_list function, which creates a list of values. You can also
use the function collect_set, which creates an array without duplicate values

    SELECT DEST_COUNTRY_NAME as new_name,
        collect_list(count) as flight_counts,
        collect_set(ORIGIN_COUNTRY_NAME) as origin_set
    FROM flights
    GROUP BY DEST_COUNTRY_NAME

Create an array manually

    SELECT DEST_COUNTRY_NAME, ARRAY(1, 2, 3) FROM flights

Convert an array back into rows using `explode` function. To demonstrate, let’s create a new view as our aggregation

    CREATE OR REPLACE TEMP VIEW flights_agg AS
        SELECT DEST_COUNTRY_NAME, collect_list(count) AS collected_counts
        FROM flights GROUP BY DEST_COUNTRY_NAME

Now let’s explode the complex type to one row in our result for every value in the array. The DEST_COUNTRY_NAME will
duplicate for every value in the array, performing the exact opposite of the original collect and returning us to the
original DataFrame

    SELECT explode(collected_counts), DEST_COUNTRY_NAME FROM flights_agg

### Functions

List of functions in Spark SQL

    SHOW FUNCTIONS

System functions

    SHOW SYSTEM FUNCTIONS

User functions (defined by users)

    SHOW USER FUNCTIONS

Filter by passing a string with wildcard (*) characters

    SHOW FUNCTIONS "s*";  -- all functions that begin with "s"

    -- OR
    SHOW FUNCTIONS LIKE "collect*";

### Subqueries

With subqueries, you can specify queries within other queries. This makes it possible for you to specify some
sophisticated logic within your SQL. In Spark, there are two fundamental subqueries. Correlated subqueries use some
information from the outer scope of the query in order to supplement information in the subquery. Uncorrelated
subqueries include no information from the outer scope. Each of these queries can return one (scalar subquery) or more
values. Spark also includes support for predicate subqueries, which allow for filtering based on
values.

**Uncorrelated predicate subqueries**

    SELECT * FROM flights
    WHERE origin_country_name IN (
        SELECT dest_country_name FROM flights
        GROUP BY dest_country_name ORDER BY sum(count) DESC LIMIT 5
    )

**Correlated predicate subqueries**

    SELECT * FROM flights f1
    WHERE EXISTS (
        SELECT 1 FROM flights f2
        WHERE f1.dest_country_name = f2.origin_country_name)
    AND EXISTS (
        SELECT 1 FROM flights f2
        WHERE f2.dest_country_name = f1.origin_country_name)

**Uncorrelated scalar queries**

    SELECT *, (SELECT max(count) FROM flights) AS maximum FROM flights

## Miscellaneous Features

### Configurations

https://spark.apache.org/docs/latest/configuration.html

### Setting Configuration Values in SQL

    SET spark.sql.shuffle.partitions=20
