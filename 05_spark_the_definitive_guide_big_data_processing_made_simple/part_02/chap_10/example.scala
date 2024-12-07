package spark.chap10

import org.apache.spark.sql.SparkSession

object Main {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("spark-chap10")
      .master("local")
      .getOrCreate()

    spark.sql("SELECT 1 + 1").show()

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

    // partitioned, output in spark-warehouse, run once
    spark.sql(
      """
        CREATE TABLE partitioned_flights USING parquet PARTITIONED BY (DEST_COUNTRY_NAME)
          AS SELECT DEST_COUNTRY_NAME, ORIGIN_COUNTRY_NAME, count FROM flights LIMIT 5;
      """
    )

    // [NOT_SUPPORTED_COMMAND_WITHOUT_HIVE_SUPPORT] CREATE Hive TABLE (AS SELECT) is not supported,
    // if you want to enable it, please set "spark.sql.catalogImplementation" to "hive".;
    //    spark.sql(
    //      """
    //        CREATE EXTERNAL TABLE IF NOT EXISTS hive_flights (
    //          DEST_COUNTRY_NAME STRING,
    //          ORIGIN_COUNTRY_NAME STRING,
    //          count LONG
    //        ) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    //        LOCATION 'D:/repo_books/book_sparkthedefinitiveguide/data/flight-data-hive'
    //      """
    //    )
    //    spark.sql("SELECT * FROM hive_flights").show()

    // insert into tables
    spark.sql(
      """
        INSERT INTO partitioned_flights
          PARTITION (DEST_COUNTRY_NAME="UNITED STATES")
          SELECT ORIGIN_COUNTRY_NAME, count FROM flights
          WHERE DEST_COUNTRY_NAME='UNITED STATES' LIMIT 12
      """
    )

    spark.sql("SELECT * FROM partitioned_flights WHERE DEST_COUNTRY_NAME='UNITED STATES'").show()

    // describe table metadata
    spark.sql("DESCRIBE TABLE flights").show(truncate = false)

    // create view
    spark.sql(
      """
        CREATE VIEW just_usa_view AS
          SELECT * FROM flights WHERE DEST_COUNTRY_NAME = 'United States'
      """
    )

    spark.sql("SHOW TABLES").show(truncate = false)

  }
}