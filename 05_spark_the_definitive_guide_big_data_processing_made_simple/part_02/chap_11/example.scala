package spark.chap11

import org.apache.spark.sql.SparkSession

object Main {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("chap11-example")
      .master("local")
      .getOrCreate()

    import spark.implicits._ // for as, map

    val flightsDF = spark.read
      .format("parquet")
      .load("D:\\repo_books\\book_sparkthedefinitiveguide\\data\\flight-data\\parquet\\2010-summary.parquet")

    val flightsMeta = spark.range(500)
      .map(x => (x, scala.util.Random.nextLong()))
      .withColumnRenamed("_1", "count")
      .withColumnRenamed("_2", "randomData")
      .as[FlightMetadata]

    val flights = flightsDF.as[Flight]
    flights.show()

    val flights2 = flights
      .joinWith(flightsMeta, flights.col("count") === flightsMeta.col("count"))

    flights2.show(truncate = false)

    flights2.selectExpr("_1.DEST_COUNTRY_NAME").show(truncate = false)

    // flights2.take(2)

    flights.groupByKey(x => x.DEST_COUNTRY_NAME).flatMapGroups(grpSum).show(truncate = false)

    flights.groupByKey(x => x.DEST_COUNTRY_NAME).mapValues(grpSum2).count().take(5)

    flights.groupByKey(x => x.DEST_COUNTRY_NAME).reduceGroups((l, r) => sum2(l, r)).show(truncate = false)

  }

  case class Flight(
                     DEST_COUNTRY_NAME: String,
                     ORIGIN_COUNTRY_NAME: String,
                     count: BigInt
                   )

  case class FlightMetadata(
                             count: BigInt,
                             randomData: BigInt
                           )

  def grpSum(countryName: String, values: Iterator[Flight]): Iterator[(String, Flight)] = {
    values.dropWhile(_.count < 5).map(x => (countryName, x))
  }

  def grpSum2(f: Flight):Integer = {
    1
  }

  def sum2(left: Flight, right: Flight): Flight = {
    Flight(left.DEST_COUNTRY_NAME, null, left.count + right.count)
  }
}