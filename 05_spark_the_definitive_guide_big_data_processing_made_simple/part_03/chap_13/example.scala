package spark.chap13

import org.apache.spark.sql.SparkSession
import org.apache.spark.rdd.RDD

object Main {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("SparkChap13")
      .master("local")
      .getOrCreate()

    val myCollection = "Spark The Definitive Guide : Big Data Processing Made Simple"
      .split(" ")
    val words = spark.sparkContext.parallelize(myCollection, 2)

    // key-value format
    words.map(word => (word.toLowerCase, 1)).collect().foreach(print)
    println

    // keyBy
    val keyword = words.keyBy(word => word.toLowerCase.toSeq(0).toString)
    keyword.foreach(print)
    println

    // mapping over values
    keyword.mapValues(word => word.toUpperCase).collect().foreach(print)
    println

    keyword.flatMapValues(word => word.toUpperCase).collect().foreach(print)
    println

    // extracting keys and values
    keyword.keys.collect().foreach(print)
    println
    keyword.values.collect().foreach(print)
    println

    // sampleByKey
    val distinctChars = words.flatMap(word => word.toLowerCase.toSeq)
      .distinct
      .collect()
    import scala.util.Random
    val sampleMap = distinctChars.map(c => (c, new Random().nextDouble())).toMap
    words.map(word => (word.toLowerCase.toSeq(0), word))
      .sampleByKey(withReplacement = true, fractions = sampleMap, seed = 6L)
      .collect().foreach(print)
    println

    // sampleByKeyExact
    words.map(word => (word.toLowerCase.toSeq(0), word))
      .sampleByKeyExact(withReplacement = true, fractions = sampleMap, seed = 6L)
      .collect().foreach(print)
    println

    // aggregations

    // data init
    val chars = words.flatMap(word => word.toLowerCase.toSeq)
    val KVCharacters = chars.map(letter => (letter, 1))
    val nums = spark.sparkContext.parallelize(1 to 30, numSlices = 5)

    // countByKey
    KVCharacters.countByKey().foreach(print)
    println
    KVCharacters.countByKeyApprox(timeout = 1000L, confidence = 0.95)

    // groupByKey
    KVCharacters.groupByKey().map(row => (row._1, row._2.reduce(addFunc))).collect().foreach(print)
    println

    KVCharacters.reduceByKey(addFunc).collect().foreach(print)
    println

    // other aggregation methods
    // aggregation
    println(nums.aggregate(0)(maxFunc, addFunc))

    // treeAggregation
    println(nums.treeAggregate(0)(maxFunc, addFunc, depth = 3))

    // aggregateByKey
    KVCharacters.aggregateByKey(0)(addFunc, maxFunc).collect().foreach(print)
    println

    // combineByKey
    val valToCombiner = (value: Int) => List(value)
    val mergeValuesFunc = (vals: List[Int], valToAppend: Int) => valToAppend :: vals // :: append Int to List[Int]
    val mergeCombinerFunc = (vals1: List[Int], vals2: List[Int]) => vals1 ::: vals2 // ::: append List[Int] to List[Int]
    val outputPartitions = 6
    KVCharacters
      .combineByKey(
        createCombiner = valToCombiner,
        mergeValue = mergeValuesFunc,
        mergeCombiners = mergeCombinerFunc,
        numPartitions = outputPartitions)
      .collect().foreach(println)
    println

    // foldByKey
    KVCharacters.foldByKey(0)(addFunc).collect().foreach(println)
    println

    // CoGroups
    val distinctChar = words.flatMap(word => word.toLowerCase.toSeq).distinct
    val charRDD = distinctChar.map(c => (c, new Random().nextDouble()))
    val charRDD2 = distinctChar.map(c => (c, new Random().nextDouble()))
    val charRDD3 = distinctChar.map(c => (c, new Random().nextDouble()))
    charRDD.cogroup(charRDD2, charRDD3).take(5).foreach(println)
  }

  private def maxFunc(left: Int, right: Int): Int = math.max(left, right)

  private def addFunc(left: Int, right: Int): Int = left + right
}