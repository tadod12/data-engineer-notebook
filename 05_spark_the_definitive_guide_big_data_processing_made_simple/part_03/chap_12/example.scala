package spark.chap12

import org.apache.spark.sql.SparkSession
//import org.apache.hadoop.io.compress.BZip2Codec

object Main {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("chap12-example")
      .master("local")
      .getOrCreate()

    println(spark.range(10).toDF().rdd.map(rowObject => rowObject.getLong(0)))

    val myCollection = "Spark The Definitive Guide: Big Data Processing Made Simple"
      .split(" ")
    val words = spark.sparkContext.parallelize(myCollection, 2)
    words.setName("myWords")
    println(words.name)

    // distinct
    println(words.distinct().count())

    // filtering
    words.filter(word => startsWithS(word)).collect().foreach(println)

    // map
    val words2 = words.map(word => (word, word(0), word.startsWith("S")))
    words2.collect().foreach(println) // tuple

    words2.filter(record => record._3).collect().foreach(println)

    // flatmap
    words.flatMap(word => word.toSeq).collect().foreach(println)

    // sort
    words.sortBy(word => word.length * -1).collect().foreach(println)

    // random split
    val splits = words.randomSplit(Array(0.5, 0.5))
    splits.zipWithIndex.foreach { case (rdd, index) =>
      println(s"Contents of split $index:")
      rdd.collect().foreach(println)
    }

    // reduce
    println(s"Longest word: ${words.reduce(wordLengthReducer)}")

    // count
    println(s"Number of words: ${words.count()}")

    // countApprox
    println(s"Count Approximation: ${words.countApprox(timeout = 400, confidence = 0.95)}")

    // countApproxDistinct
    println(s"countApproxDistinct first implementation: ${words.countApproxDistinct(relativeSD = 0.05)}")
    println(s"countApproxDistinct second implementation: ${words.countApproxDistinct(p = 4, sp = 10)}")

    // countByValue
    println(s"countByValue: ${words.countByValue()}")

    // countByValueApprox
    println(s"countByValueApprox: ${words.countByValueApprox(timeout = 400, confidence = 0.95)}")

    // saveAsTextFile
    //    words.saveAsTextFile("output/words_text_file")
    // with codec
    //    words.saveAsTextFile("output/words_compressed", classOf[BZip2Codec])

    // pipe
    words.pipe("find /c /v \"\"").collect().foreach(println)

    // mapPartitions
    words.mapPartitions(_ => Iterator[Int](1)).sum()

    // glom
    println("glom")
    words.glom().collect().foreach(println)

    println(spark.sparkContext.parallelize(Seq("Hello", "World"), 2).glom().collect()
      .map(_.mkString("[", ", ", "]"))
      .mkString("[", ", ", "]"))
  }

  private def startsWithS(a: String): Boolean = {
    a.startsWith("S") // return True/False
  }

  private def wordLengthReducer(leftWord: String, rightWord: String): String = {
    if (leftWord.length > rightWord.length)
      leftWord
    else
      rightWord
  }
}