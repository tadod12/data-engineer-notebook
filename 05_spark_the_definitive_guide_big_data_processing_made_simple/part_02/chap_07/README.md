# Chapter 7. Aggregations

Aggregating is the act of collecting something together and is a cornerstone of big data analytics. In an aggregation,
you will specify a _key_ or _grouping_ and an _aggregation function_ that specifies how you should transform one or two
columns. This function must produce one result for each group, given multiple input values

Spark allows us to create the following groupings types

- Simplest grouping: Summarize a complete DataFrame by performing an aggregation in a select statement
- A "group by" to specify one or more keys as well as one or more aggregation functions to transform the value columns
- A "window" same as "group by". However, the rows input to the functions are somehow related to the current row
- A “grouping set,” which you can use to aggregate at multiple different levels. Grouping sets are available as a
  primitive in SQL and via rollups and cubes in DataFrames.
- A “rollup” makes it possible for you to specify one or more keys as well as one or more aggregation functions to
  transform the value columns, which will be summarized hierarchically.
- A “cube” allows you to specify one or more keys as well as one or more aggregation functions to transform the value
  columns, which will be summarized across all combinations of columns.

## Aggregation Functions

You can find most aggregation functions in the org.apache.spark.sql.functions package

### count

    df.select(count("StockCode")).show()

### countDistinct

The number of unique groups

    df.select(countDistinct("StockCode")).show()

### approx_count_distinct

Often, exact distinct count with large datasets is irrelevant. There are times when an approximation to a certain degree
of
accuracy will work just fine, and for that, you can use the approx_count_distinct function

    df.select(approx_count_distinct("StockCode", 0.1)).show()

Another parameter specify the maximum estimation error allowed

### first and last

Get the first and last values from a DataFrame

    df.select(first("StockCode"), last("StockCode")).show()

### min and max

    df.select(
      min("Quantity").alias("min"),
      max("Quantity").alias("max")
    ).show()

### sum

Add all the values in a row

    df.select(sum("Quantity")).show()

### sumDistinct

    df.select(sum_distinct(col("Quantity"))).show()

### avg

    df.select(avg("Quantity").alias("avg_purchases")).show()

### Variance and Standard Deviation

Spark performs the formula for the sample standard deviation or variance if you use the `variance` or `stddev` functions

    df.select(
      var_pop("Quantity"),
      var_samp("Quantity"),
      stddev_pop("Quantity"),
      stddev_samp("Quantity")
    ).show(truncate=false)

### skewness and kurtosis

Skewness measures the asymmetry of the values in your data around the mean, whereas kurtosis is a measure of the tail of
data

    df.select(
      skewness("Quantity"),
      kurtosis("Quantity")
    ).show(truncate=false)

### Covariance and Correlation

Compare the interactions of the values in two difference columns together

- `cov` function for covariance
- `corr` function for correlation

      df.select(
        corr("InvoiceNo", "Quantity"),
        covar_samp("InvoiceNo", "Quantity"),
        covar_pop("InvoiceNo", "Quantity")
      ).show()

> Correlation measures the Pearson correlation coefficient, which is scaled between –1 and +1. The covariance is scaled
> according to the inputs in the data.

## Aggregating to Complex Types

For example, we can collect a list of values present in a given column or only the unique values by collecting to a set.

    df.agg(collect_set("Country"), collect_list("Country")).show(truncate=false)

## Grouping

First we specify the column(s) on which we would like to group, and then we specify the aggregation(s). The first step
returns a `RelationalGroupedDataset`, and the second step returns a `DataFrame`

    df.groupBy("InvoiceNo", "CustomerId").count().show()

### Grouping with Expressions

Usually we prefer to use the count function. Rather than passing that function as an expression into a select statement,
we specify it as within agg. This makes it possible for you to pass-in arbitrary expressions that just need to have some
aggregation specified

    df.groupBy("InvoiceNo").agg(
      count("Quantity").alias("quan"),
      expr("count(Quantity)")
    ).show()

### Grouping with Maps

Sometimes, it can be easier to specify your transformations as a series of Maps for which the key is the column, and the
value is the aggregation function (as a string) that you would like to perform. You can reuse multiple column names if
you specify them inline

    // in Scala
    df.groupBy("InvoiceNo").agg("Quantity"->"avg", "Quantity"->"stddev_pop").show()

    # in Python
    df.groupBy("InvoiceNo").agg(expr("avg(Quantity)"), expr("stddev_pop(Quantity)")).show()

## Window Functions

You can also use _window functions_ to carry out some unique aggregations by either computing some aggregation on a
specific "window" of data, which you define by using a reference to the current data

A group-by takes data, and every row can go only into one grouping. A window function calculates a return value for
every input row of a table based on a group of rows, called a frame. Each row can fall into one or more frames

First step: Create a window specification. The `partitionBy` is unrelated to the partitioning scheme concept we've
covered thus far. It's just a similar concept that describes how we will be breaking up our group. The ordering
determines the ordering within a given partition, and, finally, the frame specification (the rowsBetween statement)
states which rows will be included in the frame based on its reference to the current input row. In the following
example, we look at all previous rows up to the current row

    // step 1 - create window specification
    val windowSpec = Window
      .partitionBy("CustomerId", "date")
      .orderBy(col("Quantity").desc)  // rank will rank this
      .rowsBetween(Window.unboundedPreceding, Window.currentRow)

    // step 2 - create aggregations
    val maxPurchaseQuantity = max(col("Quantity")).over(windowSpec)  // a column (or expressions)
    val purchaseDenseRank = dense_rank().over(windowSpec)  // use dense_rank as opposed to rank to avoid gaps in the ranking
    val purchaseRank = rank().over(windowSpec)    

Perform a `select`

    dfWithDate.where("CustomerId IS NOT NULL").orderBy("CustomerId")
      .select(
        col("CustomerId"),
        col("date"),
        col("Quantity"),
        purchaseRank.alias("quantityRank"),
        purchaseDenseRank.alias("quantityDenseRank"),
        maxPurchaseQuantity.alias("maxPurchaseQuantity")
      ).show(truncate=false)

## Grouping Sets

Sometimes we want something a bit more complete—an aggregation across multiple groups. We achieve this by using grouping
sets. Grouping sets are a low-level tool for combining sets of aggregations together. They give you the ability to
create arbitrary aggregation in their group-by statements.

> Grouping sets depend on null values for aggregation levels. If you do not filter-out null values, you will get
> incorrect results. This applies to cubes, rollups, and grouping sets.

    SELECT CustomerId, stockCode, sum(Quantity) FROM dfNoNull
    GROUP BY customerId, stockCode GROUPING SETS((customerId, stockCode),())
    ORDER BY CustomerId DESC, stockCode DESC

> The GROUPING SETS operator is only available in SQL. To perform the same in DataFrames, you use the rollup and cube
> operators—which allow us to get the same results

### Rollups

When we set our grouping keys of multiple columns, Spark looks at those as well as the actual combinations that are
visible in the dataset. A rollup is a multidimensional aggregation that performs a variety of group-by style
calculations for us.

    // rollup - treating element hierarchically date is country's dad
    val rolledUpDF = dfNoNull.rollup("date", "Country").agg(sum("Quantity"))
      .selectExpr("date", "Country", "`sum(Quantity)` as total_quantity")
      .orderBy(asc_nulls_first("Date"))
    rolledUpDF.show(truncate=false)
    // 1 row full null is total over all
    // row with country null is total on that day

## Cube

A cube takes the rollup to a level deeper. Rather than treating elements hierarchically, a cube does the same thing
across all dimensions.

- The total across all dates and countries
- The total for each date across all countries
- The total for each country on each date
- The total for each country across all dates

      // cube - same thing but all dimensions
      val cubeDF = dfNoNull.cube("Date", "Country").agg(sum(col("Quantity")))
      .select("date", "Country", "sum(Quantity)")
      .orderBy(asc_nulls_first("Date"))
      cubeDF.show(truncate=false)

### Grouping Metadata

Sometimes when using cubes and rollups, you want to be able to query the aggregation levels so that you can easily
filter them down accordingly. We can do this by using the `grouping_id`, which gives us a column specifying the level of
aggregation that we have in our result set

Grouping ID:

- 3: This will appear for the highest-level aggregation, which will gives us the total quantity regardless of customerId
  and stockCode.
- 2: This will appear for all aggregations of individual stock codes. This gives us the total quantity per stock code,
  regardless of customer.
- 1: This will give us the total quantity on a per-customer basis, regardless of item purchased
- 0: This will give us the total quantity for individual customerId and stockCode combinations

Example

    // in Scala
    import org.apache.spark.sql.functions.{grouping_id, sum, expr}
    dfNoNull.cube("customerId", "stockCode").agg(grouping_id(), sum("Quantity"))
    .orderBy(expr("grouping_id()").desc)
    .show()
    +----------+---------+-------------+-------------+
    |customerId|stockCode|grouping_id()|sum(Quantity)|
    +----------+---------+-------------+-------------+
    |      null|     null|            3|      5176450|
    |      null|    23217|            2|         1309|
    |      null|   90059E|            2|           19|
    ...
    +----------+---------+-------------+-------------+

### Pivot

Pivots make it possible for you to convert a row into a column. For example, in our current data we have a Country
column. With a pivot, we can aggregate according to some function for each of those given countries and display them in
an easy-to-query way

    // pivot
    val pivoted = dfWithDate.groupBy("date").pivot("Country").sum()
    pivoted.where("date > '2011-12-05'").select("date", "`USA_sum(Quantity)`").show()

This DataFrame will now have a column for every combination of country, numeric variable, and a column specifying the
date. For example, for the USA we have the following columns: USA_sum(Quantity), USA_sum(UnitPrice), USA_sum(CustomerID)

## User-Defined Aggregation Functions

I ain't that good
