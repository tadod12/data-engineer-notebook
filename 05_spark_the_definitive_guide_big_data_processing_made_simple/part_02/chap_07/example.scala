package spark.chap07

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions.{approx_count_distinct, asc_nulls_first, avg, col, collect_list, collect_set, corr, count, countDistinct, covar_pop, covar_samp, dense_rank, expr, first, grouping_id, kurtosis, last, max, min, rank, skewness, stddev_pop, stddev_samp, sum, sum_distinct, to_date, var_pop, var_samp}

object Main {
  def main(args: Array[String]): Unit = {
    // create spark session
    val spark = SparkSession.builder()
      .appName("spark-chap07")
      .master("local[*]")
      .getOrCreate()

    // create DataFrame
    val df = spark.read.format("csv")
      .option("header", "true")
      .option("inferSchema", "true")
      .load("D:\\repo_books\\book_sparkthedefinitiveguide\\data\\retail-data\\all")
      .coalesce(5)
    df.cache()
    df.createOrReplaceTempView("dfTable")

    df.show(10, truncate=false)

    // count
    df.select(count("StockCode").alias("count")).show()

    // countDistinct
    df.select(countDistinct("StockCode").alias("countDistinct")).show()

    // approx_count_distinct
    df.select(approx_count_distinct("StockCode", 0.1).alias("approx_count_distinct")).show()

    // first and last
    df.select(
      first("StockCode").alias("first"),
      last("StockCode").alias("last")
    ).show()

    // min and max
    df.select(
      min("Quantity").alias("min"),
      max("Quantity").alias("max")
    ).show()

    // sum
    df.select(sum("Quantity")).show()

    // sumDistinct
    df.select(sum_distinct(col("Quantity")).alias("sumDistinct")).show()

    // avg
    df.select(avg("Quantity").alias("avg_purchases")).show()

    // variance and standard deviation
    df.select(
      var_pop("Quantity"),
      var_samp("Quantity"),
      stddev_pop("Quantity"),
      stddev_samp("Quantity")
    ).show(truncate=false)

    // skewness and kurtosis
    df.select(
      skewness("Quantity"),
      kurtosis("Quantity")
    ).show(truncate=false)

    // covariance and correlation
    df.select(
      corr("InvoiceNo", "Quantity"),
      covar_samp("InvoiceNo", "Quantity"),
      covar_pop("InvoiceNo", "Quantity")
    ).show()

    // aggregation to complex types
    df.agg(collect_set("Country"), collect_list("Country")).show(truncate=false)

    // basic grouping
    // 1 - specify the column(s)
    // 2 - specify the aggregation(s)
    df.groupBy("InvoiceNo", "CustomerId").count().show()

    // grouping with expressions
    df.groupBy("InvoiceNo").agg(
      count("Quantity").alias("quan"),
      expr("count(Quantity)")
    ).show()

    // grouping with maps
    df.groupBy("InvoiceNo").agg("Quantity"->"avg", "Quantity"->"stddev_pop").show()

    // window functions
    // add a date column from invoice date
    val dfWithDate = df.withColumn("date", to_date(col("InvoiceDate"), "M/d/yyyy H:m"))
    dfWithDate.createOrReplaceTempView("dfWithDate")

    // step 1 - create window specification
    val windowSpec = Window
      .partitionBy("CustomerId", "date")
      .orderBy(col("Quantity").desc)
      .rowsBetween(Window.unboundedPreceding, Window.currentRow)

    // step 2 - aggregation
    val maxPurchaseQuantity = max(col("Quantity")).over(windowSpec)
    val purchaseDenseRank = dense_rank().over(windowSpec)
    val purchaseRank = rank().over(windowSpec)

    // step 3 - select
    dfWithDate.where("CustomerId IS NOT NULL").orderBy("CustomerId")
      .select(
        col("CustomerId"),
        col("date"),
        col("Quantity"),
        purchaseRank.alias("quantityRank"),
        purchaseDenseRank.alias("quantityDenseRank"),
        maxPurchaseQuantity.alias("maxPurchaseQuantity")
      ).show(truncate=false)

    // Grouping sets
    val dfNoNull = dfWithDate.drop()
    dfNoNull.createOrReplaceTempView("dfNoNull")

    // rollup - treating element hierarchically date is country's dad
    val rolledUpDF = dfNoNull.rollup("date", "Country").agg(sum("Quantity"))
      .selectExpr("date", "Country", "`sum(Quantity)` as total_quantity")
      .orderBy(asc_nulls_first("Date"))
    rolledUpDF.show(truncate=false)
    // 1 row full null is total over all
    // row with country null is total on that day

    // cube - same thing but all dimensions
    val cubeDF = dfNoNull.cube("Date", "Country").agg(sum(col("Quantity")))
      .select("date", "Country", "sum(Quantity)")
      .orderBy(asc_nulls_first("Date"))
    cubeDF.show(truncate=false)

    // Grouping Metadata
    dfNoNull.cube("CustomerId", "stockCode").agg(grouping_id(), sum("Quantity"))
      .orderBy(expr("grouping_id()").desc)
      .show(truncate=false)

    // pivot
    val pivoted = dfWithDate.groupBy("date").pivot("Country").sum()
    pivoted.where("date > '2011-12-05'").select("date", "`USA_sum(Quantity)`").show()
  }
}