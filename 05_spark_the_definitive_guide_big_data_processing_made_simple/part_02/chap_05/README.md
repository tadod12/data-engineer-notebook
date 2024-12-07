# Chapter 5. Basic Structured Operations

This chapter focuses exclusively on fundamental DataFrame operations and avoids aggregations, window functions, and
joins

Definitionally, a DataFrame consists of a series of _records_, that are of type `Row`, and a number of _columns_ that
present a computation expression that can be performed on each individual record in the Dataset. _Schemas_ define the
name as well as the type of data in each column. _Partitioning_ of the DataFrame defines the layout of the DataFrame or
Dataset's physical distribution across the cluster. The _partitioning scheme_ defines how that is allocated

Create DataFrame

    // in Scala
    val df = spark.read.format("json")
        .load("/data/flight-data/json/2015-summary.json")

    # in Python
    df = spark.read.format("json").load("/data/flight-data/json/2015-summary.json")

Check schema

    scala> df.printSchema()
    root
    |-- DEST_COUNTRY_NAME: string (nullable = true)
    |-- ORIGIN_COUNTRY_NAME: string (nullable = true)
    |-- count: long (nullable = true)

## Schemas

A schema defines the column names and types of a DataFrame

> For ad hoc analysis, schema-on-read usually works just fine (although at times it can be a bit slow with plain-text
> file formats like CSV or JSON). However, this can also lead to precision issues like a long type incorrectly set as an
> integer when reading in a file. When using Spark for production Extract, Transform, and Load (ETL), it is often a good
> idea to define your schemas manually, especially when working with untyped data sources like CSV and JSON because
> schema inference can vary depending on the type of data that you read in.

Get schema type

    df.schema

- Scala

        org.apache.spark.sql.types.StructType = ...
        StructType(
            StructField(DEST_COUNTRY_NAME,StringType,true),
            StructField(ORIGIN_COUNTRY_NAME,StringType,true),
            StructField(count,LongType,true)
        )

- Python

        StructType(List(StructField(DEST_COUNTRY_NAME,StringType,true),
        StructField(ORIGIN_COUNTRY_NAME,StringType,true),
        StructField(count,LongType,true)))

A schema is a `StructType` made up of a number of fields, `StructFields`, that have a name, type, a Boolean flag which
specifies whether that column can contain missing or `null` values. Users can optionally specify associated metadata
with that column.

Schemas can contain other `StructType`s (Spark's complex types). If the types in the data (at runtime) do not match the
schema, Spark will throw an error.

Example create and enforce a specific schema

![scala specific schema.png](scala%20specific%20schema.png)

In Python

    # in Python
    from pyspark.sql.types import StructField, StructType, StringType, LongType

    myManualSchema = StructType([
      StructField("DEST_COUNTRY_NAME", StringType(), True),
      StructField("ORIGIN_COUNTRY_NAME", StringType(), True),
      StructField("count", LongType(), False, metadata={"hello":"world"})
    ])

    df = spark.read.format("json").schema(myManualSchema)\
      .load("/data/flight-data/json/2015-summary.json")

## Columns and Expressions

You can select, manipulate, and remove columns from DataFrames and these operations are represented as expressions.

### Columns

    import org.apache.spark.sql.functions.{col, column} // Scala
    from pyspark.sql.functions import col, column

    col("someColumnName")
    // or
    column("someColumnName")

Refer to a specific DataFrame's column

    df.col("count")

### Expressions

An `expression` is a set of transformations on one or more values in a record in a DataFrame. Think of it like a
function that takes as input one or more column names, resolves them, and then potentially applies more expressions to
create a single value for each record in the dataset. Importantly, this “single value” can actually be a complex type
like a `Map` or `Array`.

Simplest expression, create via the `expr` function: `expr("someCol")` is equivalent to `col("someCol")`

#### Columns as expressions

    // in Scala
    import org.apache.spark.sql.functions.expr
    expr("(((someCol + 5) * 200) - 6) < otherCol")  // SQL expression

    // Expression as DataFrame code
    (((col("someCol") + 5) * 200) - 6) < col("otherCol")

#### Accessing a DataFrame's columns

Sometimes, you’ll need to see a DataFrame’s columns, which you can do by using something like printSchema; however, if
you want to programmatically access columns, you can use the columns property to see all columns on a DataFrame:

    spark.read.format("json").load("...").columns

## Records and Rows

In Spark, each row in a DataFrame is a single record. Spark represents this record as an object of type Row. Spark
manipulates `Row` objects using column expressions in order to produce usable values

    df.first()

### Creating Rows

It’s important to note that only DataFrames have schemas. Rows themselves do not have schemas. This means that if you
create a Row manually, you must specify the values in the same order as the schema of the DataFrame to which they might
be appended

    // in Scala
    import org.apache.spark.sql.Row
    val myRol = Row("Hello", null, 1, false)

    # in Python
    from pyspark.sql import Row
    myRow = Row("Hello", None, 1, False)

Accessing data in rows

    // in Scala
    myRow(0) // type Any
    myRow(0).asInstanceOf[String] // String
    myRow.getString(0) // String
    myRow.getInt(2) // Int

    # in Python
    myRow[1]
    myRow[2]

## DataFrame Transformations

![transformation kinds.png](transformation%20kinds.png)

### Creating DataFrames

Previously, we can create DataFrame from raw data sources

    val df = spark.read.format("json").load("/data/flight-data/json/2015-summary.json")
    // register as temp view
    df.createOrReplaceTempView("dfTable")

We can also create DataFrames on the fly by taking a set of rows and converting them to a DataFrame

    // in Scala
    import org.apache.spark.sql.Row
    import org.apache.spark.sql.types.{StructField, StructType, StringType, LongType}

    val myManualSchema = new StructType(Array(
      StructField("some", StringType, true),
      StructField("col", StringType, true),
      StructField("names", LongType, false)))

    val myRows = Seq(Row("Hello", null, 1L))
    // create RDD
    val RDD = spark.sparkContext.parallelize(myRows)
    val myDF = spark.createDataFrame(myRDD, myManualSchema)
    myDF.show()

    
    # in Python
    from pyspark.sql import Row
    from pyspark.sql.types import StructField, StructType, StringType, LongType
    myManualSchema = StructType([
      StructField("some", StringType(), true),
      StructField("col", StringType(), true),
      StructField("names", LongType(), false)
    ])
    myRow = Row("Hello", None, 1)
    myDF = spark.createDataFrame([myRow], myManualSchema)
    myDF.show()

Create DF by running `toDF` on a `Seq` type. This does not play well with `null` types, so it's not necessarily
recommended for production use cases

    val myDF = Seq(("Hello, 2, 1L)).toDF("col1", "col2", "col3")

### select and selectExpr

Simplest, using to manipulate columns in DataFrames. The easiest way is just to use the `select` method and past in the
column names as strings with which you would like to work. You can select multiple columns by using the same style of
query, just add more column name strings to `select` method

    // both Scala and Python
    df.select("DEST_COUNTRY_NAME", "ORIGIN_COUNTRY_NAME").show(2)

    -- in SQL
    SELECT DEST_COUNTRY_NAME FROM dfTable LIMIT 2

You can refer to columns in a number of different ways

    // in Scala
    import org.apache.spark.sql.functions.{expr, col, column}
    df.select(
      df.col("DEST_COUNTRY_NAME"),
      col("DEST_COUNTRY_NAME"),
      column("DEST_COUNTRY_NAME"),
      'DEST_COUNTRY_NAME,
      $"DEST_COUNTRY_NAME",
      expr("DEST_COUNTRY_NAME"))
    .show(2)

    # in Python
    from pyspark.sql.functions import expr, col, column
    df.select(
      expr("DEST_COUNTRY_NAME"),
      col("DEST_COUNTRY_NAME"),
      column("DEST_COUNTRY_NAME"))\
    .show(2)

One common error is attempting to mix Column objects and strings:

    df.select(col("DEST_COUNTRY_NAME"), "DEST_COUNTRY_NAME")  // complier error

> `expr` is the most flexible reference that we can use

    df.select(expr("DEST_COUNTRY_NAME AS destination")).show(2)

    df.select(expr("DEST_COUNTRY_NAME as destination").alias("DEST_COUNTRY_NAME")).show(2)

    // Most convinient
    df.selectExpr("DEST_COUNTRY_NAME as destination", "DEST_COUNTRY_NAME").show(2)

We can treat selectExpr as a simple way to build up complex expressions that create new DataFrames. In fact, we can add
any valid non-aggregating SQL statement, and as long as the columns resolve, it will be valid!

    df.selectExpr(
      "*", // all original columns
      "(DEST_COUNTRY_NAME = ORIGIN_COUNTRY_NAME) as withinCountry")
    .show(2)

    -- in SQL
    SELECT *, (DEST_COUNTRY_NAME = ORIGIN_COUNTRY_NAME) as withinCountry
    FROM dfTable
    LIMIT 2

Specify aggregations over the entire DataFrame

    df.selectExpr("avg(count)", "count(distinct(DEST_COUNTRY_NAME))")

    -- in SQL
    SELECT avg(count), count(distinct(DEST_COUNTRY_NAME)) FROM dfTable

### Converting to Spark Types (Literals)

Sometimes, we need to pass explicit values into Spark that are just a value (rather than a new column). This might be a
constant value or something we’ll need to compare to later on. The way we do this is through _literals_

    // in Scala
    import org.apache.spark.sql.functions.lit
    df.select(expr("*"), lit(1).as(One)).show(2)

    -- in SQL
    SELECT *, 1 as One FROM dfTable LIMIT 2

    +-----------------+-------------------+-----+---+
    |DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|One|
    +-----------------+-------------------+-----+---+
    | United States   |            Romania|   15|  1|
    | United States   |            Croatia|    1|  1|
    +-----------------+-------------------+-----+---+

### Adding Columns

Formal way of adding a new column to a DataFrame by using `withColumn` method on our DataFrame

    // in Scala
    df.withColumn("numberOne", lit(1)).show(2)

    # in Python
    df.withColumn("numberOne", lit(1)).show(2)

    -- in SQL
    SELECT *, 1 as numberOne FROM dfTable LIMIT 2

    // same result as above

Make it an actual expression rather than literal

    df.withColumn("withinCountry", expr("ORIGIN_COUNTRY_NAME == DEST_COUNTRY_NAME")).show(2)

> `withColumn` function takes two arguments: the column name and the expression that will create the value for that
> given row in the DataFrame

### Renaming Columns

    // in Scala
    df.withColumnRenamed("DEST_COUNTRY_NAME", "dest").columns

    # in Python
    df.withColumnRenamed("DEST_COUNTRY_NAME", "dest").columns

    // result
    ... dest, ORIGIN_COUNTRY_NAME, count

### Reserved Characters and Keywords

One thing that you might come across is reserved characters like spaces or dashes in column names. Handling these means
escaping column names appropriately. In Spark, we do this by using backtick (`) characters

    val dfWithLongColName = df.withColumn(
      "This Long Column-Name",
    expr("ORIGIN_COUNTRY_NAME"))

Don't need escape because first argument to `withColumn` is a string for new column name. However:

    dfWithLongColName.selectExpr(
      "`This Long Column-Name`",
      "`This Long Column-Name` as `new col`")
    .show(2)

    -- in SQL
    SELECT `This Long Column-Name`, `This Long Column-Name` as `new col`
    FROM dfTableLong LIMIT 2

Need backticks because we're referencing a column in an expression

We can refer to columns with reserved characters (and not escape them) if we’re doing an explicit string-to-column
reference

    dfWithLongColName.select(col("This Long Column-Name")).columns
    // same
    dfWithLongColName.select(expr("`This Long Column-Name`")).columns

### Case Sensitivity

Default is case insensitive

    -- in SQL
    set spark.sql.caseSensitive true

### Remove Columns

We can do this by using `select`. However, there is also a dedicated method called `drop`

    df.drop("ORIGIN_COUNTRY_NAME").show()
    df.drop("ORIGIN_COUNTRY_NAME", "DEST_COUNTRY_NAME")

### Changing a Column's Type (cast)

    df.withColumn("count2", col("count").cast("long"))

    -- in SQL
    SELECT *, cast(count as long) AS count2 FROM dfTable

### Filtering Rows

There are two methods to perform this operation: you can use `where` or `filter` and they both will perform the same
operation and accept the same argument types when used with DataFrames.

    df.filter(col("count") < 2).show(2)
    df.where("count < 2").show(2)

If you want to specify multiple AND filter, just chain them sequentially (Spark automatically performs all filtering
operations at the same time)

    df.where(col("count") < 2)
      .where(col("ORIGIN_COUNTRY_NAME") =!= "Croatia")
      .show(2)

### Getting Unique Rows

    df.select("ORIGIN_COUNTRY_NAME", "DEST_COUNTRY_NAME").distinct().row()

### Random Samples

Using `sample` method on a DataFrame to sample random records.

    val seed = 5
    val withReplacement = false
    val fraction = 0.5  // the aproximate fraction of the dataset that will be returned
    df.sample(withReplacement, fraction, seed).count()

### Random Splits

Often used with machine learning algorithms to create training, validation, and test sets. We split our DataFrame into
two different DataFrames by setting the weights by which we will split the DataFrame

    // in Scala
    val dataFrames = df.randomSplit(Array(0.25, 0.75), seed)
    dataFrames(0).count() > dataFrames(1).count() // false

    # in Python
    dataFrames = df.randomSplit([0.25, 0.75], seed)
    dataFrames[0].count() > dataFrames[1].count() # false

### Concatenating and Appending Rows (Union)

DataFrames are immutable, so to append to a DataFrame, you must _union_ the original DataFrame along with the new
DataFrame. To union two DataFrames, you must be sure that they have the same schema and number of columns

> Unions are currently performed based on location, not on the schema. This means that columns will not automatically
> line up the way you think they might.

    // in Scala
    import org.apache.spark.sql.Row
    val schema = df.schema // df above
    val newRows = Seq(
      Row("New Country", "Other Country", 5L),
      Row("New Country 2", "Other Country 3", 1L)
    )
    val parallelizedRows = spark.sparkContext.parallelize(newRows)
    val newDF = spark.createDataFrame(parallelizedRows, schema)
    df.union(newDF)
      .where("count = 1")
      .where($"ORIGIN_COUNTRY_NAME" =!= "United States")
      .show()

> In Scala, you must use the =!= operator so that you don’t just compare the unevaluated column expression to a string
> but instead to the evaluated one

    # in Python
    from pyspark.sql import Row
    schema = df.schema
    newRows = [
      Row("New Country", "Other Country", 5L),
      Row("New Country 2", "Other Country 3", 1L)
    ]
    parallelizedRows = spark.sparkContext.parallelize(newRows)
    newDF = spark.createDataFrame(parallelizedRows, schema)

    df.union(newDF)
      .where("count = 1")
      .where(col("ORIGIN_COUNTRY_NAME") != "United States")
      .show()

### Sorting Rows

There are two equivalent operations: `sort` and `orderBy`. The default is to sort in ascending order:

    df.sort("count")
    df.orderBy("count", "DEST_COUNTRY_NAME").show()
    df.orderBy(col("count"), col("DEST_COUNTRY_NAME")).show()

To more explicitly sort direction:

    import org.apache.spark.sql.functions.{desc, asc}
    df.orderBy(expr("count desc")).show() // decending count
    df.orderBy(desc("count"), asc("DEST_COUNTRY_NAME")).show()

> An advanced tip is to use asc_nulls_first, desc_nulls_first, asc_nulls_last, or desc_nulls_last to specify where you
> would like your null values to appear in an ordered DataFrame

For optimization: Sort within each partition before another set of transformation

    spark.read.format("json").load("/data/flight-data/json/*-summary.json")
      .sortWithinPartitions("count")

### Limit

    df.limit(5)

### Repartition and Coalesce

Another important optimization opportunity is to partition the data according to some frequently filtered columns, which
control the physical layout of data across the cluster including the partitioning scheme and the number of partitions.

Repartition will incur a full shuffle of the data, regardless of whether one is necessary. You should repartition only
when the future number of partition is greater than your current number of partitions or when you are looking to
partition by a set of columns

    // in Scala
    df.rdd.getNumPartitions // 1
    df.repartition(5)

    # in Python
    df.rdd.getNumPartitions()
    df.repartition(5)

Repartition based on column:

    df.repartition(col("DEST_COUNTRY_NAME"))
    df.repartition(5, col("DEST_COUNTRY_NAME"))

Coalesce, on the other hand, will not incur a full shuffle and will try to combine partitions

    df.repartition(5, col("DEST_COUNTRY_NAME)).coalesce(2)

### Collecting Rows to the Driver

Spark maintains the state of the cluster in the driver. There are times when you’ll want to collect some of your data to
the driver in order to manipulate it on your local machine

- `collect` gets all data from the entire DataFrame
- `take` selects the first N rows
- `show` prints out a number of rows

      val collectDF = df.limit(10)
      collectDF.take(5)
      collectDF.show()
      collectDF.collect() // collect() is an action, select() is a transformation