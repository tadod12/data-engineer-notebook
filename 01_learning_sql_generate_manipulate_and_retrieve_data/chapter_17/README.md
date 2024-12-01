# Chapter 17. Working with Large Databases

While relational databases face various challenges as data volumes continue to grow, there are strategies such as
partitioning, clustering, and sharding that allow companies to continue to utilize relational databases by spreading
data across multiple storage tiers and servers. Other companies have decided to move to big data platforms such as
Hadoop in order to handle huge data volumes.

## Partitioning

The following tasks become more difficult and/or time-consuming as a table grows past a few million rows:

- Query execution requiring full table scans

- Index creation/rebuild

- Data archival/deletion

- Generation of table/index statistics

- Table relocation (e.g., move to a different tablespace)

- Database backups

The best way to prevent administrative issues from occurring in the future is to break large tables into pieces, or
partitions, when the table is first created (although tables can be partitioned later, it is easier to do so initially)

Administrative tasks can be performed on individual partitions, often in parallel, and some tasks can skip one or more
partitions entirely

### Partitioning Concepts

When a table is partitioned, two or more table partitions are created, each having the exact same definition but with
non-overlapping subsets of data. For example, a table containing sales data could be partitioned by month using the
column containing the sale date, or it could be partitioned by geographic region using the state/province code

Once a table has been partitioned, the table itself becomes a virtual concept; the partitions hold the data, and any
indexes are built on the data in the partitions

> The database users can still interact with the table without knowing that the table had been partitioned (similar to a
> view, users interact with schema objects that are interfaces rather than actual tables)

While every partition must have the same schema definition (columns, column types, etc.), there are several
administrative features that can differ for each partition

- Partitions may be stored on different tablespaces, which can be on different physical storage tiers

- Partitions can be compressed using different compression schemes

- Local indexed can be dropped for some partitions

- Table statistics can be frozen on some partitions, while being periodically refreshed on others

- Individual partitions can be pinned into memory or stored in the database's flash storage tier

### Table Partitioning

The partitioning scheme available in most relational databases is _horizontal partitioning_, which assigns entire rows
to exactly one partition. When partitioning a table horizontally, you must choose a _partition key_, which is the column
whose values are used to assign row to a particular partition

In most cases, a table’s partition key consists of a single column, and a partitioning function is applied to this
column to determine in which partition each row should reside

### Index Partitioning

If your partitioned table has indexes, you will get to choose

- _global index_: A particular index stay intact (useful for queries that do not specify a value for the partition key)

- _local index_: A particular index be broken into pieces such that each partition has its own index

Example

    SELECT sum(amount) FROM sales WHERE geo_region_cd = 'US'

Since this query does not include a filter condition on the sale_date column, the server will need to search every
partition in order to find the total US sales. If a global index is built on the geo_region_cd column, however, then the
server could use this index to quickly find all the rows containing US sales

### Partitioning Methods

#### Range Partitioning

    CREATE TABLE sales (
        sale_id INT NOT NULL, 
        cust_id INT NOT NULL, 
        store_id INT NOT NULL, 
        sale_date INT NOT NULL, 
        amount DECIMAL(9, 2)
    )
    PARTITION BY RANGE (yearweek(sale_date)) (
        PARTITION s1 VALUES LESS THAN (202002), 
        PARTITION s2 VALUES LESS THAN (202003), 
        PARTITION s3 VALUES LESS THAN (202004), 
        PARTITION s4 VALUES LESS THAN (202005), 
        PARTITION s5 VALUES LESS THAN (202006), 
        PARTITION s999 VALUES LESS THAN (MAXVALUE)
    );

Check partition through metadata

    SELECT partition_name, partition_method, partition_expression
    FROM information_schema.partitions
    WHERE table_name = 'sales'
    ORDER BY partition_ordinal_position;

Generating new partitions (split from exist partition)

    ALTER TABLE sales REORGANIZE PARTITION s999 INTO (
        PARTITION s6 VALUES LESS THAN (202007),
        PARTITION s7 VALUES LESS THAN (202008), 
        PARTITION s999 VALUES LESS THAN (MAXVALUE)
    );

Count number of rows (data) in each partition

    SELECT concat('# of rows in S1 = ', count(*)) partition_rowcount
        FROM sales PARTITION (s1) 
    UNION ALL
    SELECT concat('# of rows in S2 = ', count(*)) partition_rowcount
        FROM sales PARTITION (s2) 
    UNION ALL
    SELECT concat('# of rows in S3 = ', count(*)) partition_rowcount
        FROM sales PARTITION (s3) 
    UNION ALL
    SELECT concat('# of rows in S4 = ', count(*)) partition_rowcount
        FROM sales PARTITION (s4) 
    UNION ALL
    SELECT concat('# of rows in S5 = ', count(*)) partition_rowcount
        FROM sales PARTITION (s5) 
    UNION ALL
    SELECT concat('# of rows in S6 = ', count(*)) partition_rowcount
        FROM sales PARTITION (s6) 
    UNION ALL
    SELECT concat('# of rows in S7 = ', count(*)) partition_rowcount
        FROM sales PARTITION (s7) 
    UNION ALL
    SELECT concat('# of rows in S999 = ', count(*)) partition_rowcount
        FROM sales PARTITION (s999);

#### List Partitioning

    CREATE TABLE sales (
        sale_id INT NOT NULL,
        cust_id INT NOT NULL, 
        store_id INT NOT NULL, 
        sale_date DATE NOT NULL, 
        geo_region_cd VARCHAR(6) NOT NULL, 
        amount DECIMAL(9, 2)
    )
    PARTITION BY LIST COLUMNS (geo_region_cd) (
        PARTITION NORTHAMERICA VALUES IN ('US_NE', 'US_SE', 'US_MW', 'US_NW', 'US_SW', 'CAN', 'MEX'),
        PARTITION EUROPE VALUES IN ('EUR_E', 'EUR_W'), 
        PARTITION ASIA VALUES IN ('CHN', 'JPN', 'IND')
    );
    -- 3 partitions: NORTHAMERICA, EUROPE, ASIA

Add rows to the table

    INSERT INTO sales
    VALUES
        (1, 1, 1, '2020-01-18', 'US_NE', 2765.15),
        (2, 3, 4, '2020-02-07', 'CAN', 5322.08),
        (3, 6, 27, '2020-03-11', 'KOR', 4267.12);
    ERROR 1526 (HY000): Table has no partition for value from column_list

Fixing

    ALTER TABLE sales
    REORGANIZE PARTITION ASIA INTO (
        PARTITION ASIA VALUES IN ('CHN', 'JPN', 'IND', 'KOR')
    );

> While range partitioning allows for a maxvalue partition to catch any rows that don’t map to any other partition, it’s
> important to keep in mind that list partitioning does not provide for a spillover partition

#### Hash Partitioning

The server does this by applying a _hashing function_ to the column value, and this type of partitioning is called _hash
partitioning_. Hash partitioning works best when the partitioning key column contains a large number of distinct values

    CREATE TABLE sales (
        sale_id INT NOT NULL, 
        cust_id INT NOT NULL, 
        store_id INT NOT NULL, 
        sale_date DATE NOT NULL, 
        amount DECIMAL(9, 2)
    )
    PARTITION BY HASH (cust_id)
        PARTITION 4 (
            PARTITION H1, 
            PARTITION H2, 
            PARTITION H3, 
            PARTITION H4
        );

#### Composite Partitioning

_Composite partitioning_ allows you to use two different types of partitioning for the same table. With composite
partitioning, the first partitioning method defines the partitions, and the second partitioning method defines the
_subpartitions_

    CREATE TABLE sales (
        sale_id INT NOT NULL, 
        cust_id INT NOT NULL, 
        store_id INT NOT NULL, 
        sale_date DATE NOT NULL, 
        amount DECIMAL(9, 2)
    )
    PARTITION BY RANGE (yearweek(sale_date))
    SUBPARTITION BY HASH (cust_id) (
        PARTITION s1 VALUES LESS THAN (202002) (
            SUBPARTITION s1_h1,
            SUBPARTITION s1_h2,
            SUBPARTITION s1_h3,
            SUBPARTITION s1_h4),
        PARTITION s2 VALUES LESS THAN (202003) (
            SUBPARTITION s2_h1,
            SUBPARTITION s2_h2,
            SUBPARTITION s2_h3,
            SUBPARTITION s2_h4),
        PARTITION s3 VALUES LESS THAN (202004) (
            SUBPARTITION s3_h1,
            SUBPARTITION s3_h2,
            SUBPARTITION s3_h3,
            SUBPARTITION s3_h4),
        PARTITION s4 VALUES LESS THAN (202005) (
            SUBPARTITION s4_h1,
            SUBPARTITION s4_h2,
            SUBPARTITION s4_h3,
            SUBPARTITION s4_h4),
        PARTITION s5 VALUES LESS THAN (202006) (
            SUBPARTITION s5_h1,
            SUBPARTITION s5_h2,
            SUBPARTITION s5_h3,
            SUBPARTITION s5_h4),
        PARTITION s999 VALUES LESS THAN (MAXVALUE) (
            SUBPARTITION s999_h1,
            SUBPARTITION s999_h2,
            SUBPARTITION s999_h3,
            SUBPARTITION s999_h4)
        );

### Partitioning Benefits

_Partition pruning_: One of the biggest advantages of table partitioning, you may only need to interact with as few as
one partition, rather than the entire table

For example, if your table is range-partitioned on the sales_date column, and you execute a query that includes a filter
condition such as `WHERE sales_date BETWEEN '2019-12-01' AND '2020-01-15'`, the server will check the table’s metadata
to determine which partitions actually need to be included

_Partition-wise joins_: If you execute a query that includes a join to a partitioned table and the query includes a
condition on the partitioning column, the server can exclude any partitions that do not contain data pertinent to the
query

Quickly delete data that is no longer needed, perform updates on multiple partitions simultaneously

## Clustering

Allows multiple servers to act as a single database

With this type of architecture (shared-disk/shared-cache configurations), an application server could attach to any one
of the database servers in the cluster, with connections automatically failing over to another server in the cluster in
case of failure. With an eight-server cluster, you should be able to handle a very large number of concurrent users and
associated queries/reports/jobs

## Sharding

Partition not just individual tables but the entire database (similar to table partitioning but on a larger scale and
with far more complexity)

If you were to employ this strategy for the social media company, you might decide to implement 100 separate databases,
each one hosting the data for approximately 10 million users

Sharding's issues

- You will need to choose a _sharding key_, which is the value used to determine to which database to connect

- While large tables will be divided into pieces, with individual rows assigned to a single shard, smaller reference
  tables may need to replicated to all shards, and a strategy needs to be defined for how reference data can be modified
  and changes propagated to all shards

- If individual shards become too large, you will need a plan for adding more shards and redistributing data across the
  shards

- Making schema changes will need to have strategy for developing the changes across all the shards (all schemas stay in
  sync)

- Strategy for how to query across multiple databases and also how to implement transactions across multiple databases

## Big Data

One way to define the boundaries of big data is with the "3 Vs"

- _Volume_: generally means billions or trillions of data points

- _Velocity_: a measure of how quickly data arrives

- _Variety_: means that data is not always structured (rows and columns, ...) but can also unstructured (emails, videos,
  photos, ...)

### Hadoop

- _Hadoop Distributed File System (HDFS)_: Enables file management across a large number of servers

- MapReduce: Processes large amounts of structured and unstructured data by breaking a task into many small pieces that
  can be run in parallel across many server

- YARN: Resource manager and job scheduler for HDFS

### NoSQL and Document Databases

### Cloud Computing