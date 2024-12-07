# Chapter 12. Resilient Distributed Datasets (RDDs)

There are times when higher-level manipulation will not meet the business or engineering problem you are trying to
solve. For those cases, you might need to use Spark's lower-level APIs, specifically the Resilient Distributed Dataset (
RDD), the SparkContext, and distributed _shared variables_ like accumulators and broadcast variables.

## Low-Level APIs

There are two sets of low-level APIs:

- **RDDs** - for manipulating distributed data
- **Broadcast variables and accumulators** - for distributing and manipulating distributed shared variables
    - Broadcast Variables: Là biến toàn cục được chia sẻ cho tất cả các node trong cluster, thường dùng cho các dữ liệu
      bất biến như cấu hình hay dữ liệu tham chiếu. Các biến này giúp giảm bớt số lần truyền tải dữ liệu qua mạng.
    - Accumulators: Là biến có khả năng tích lũy giá trị từ nhiều thao tác trên nhiều node. Chúng thường được dùng để
      thu thập thông tin về các phép tính (ví dụ: đếm số lượng các lần lặp) nhưng không ảnh hưởng đến việc tính toán
      chính.

### When to use the Low-Level APIs

- Need some functionality that can not find in the higher-level APIs
- Need to maintain some legacy codebase written using RDDs
- Need to do some custom shared variable manipulation

When you’re calling a DataFrame transformation, it actually just becomes a set of RDD transformations. This
understanding can make your task easier as you begin debugging more and more complex workloads

### How to use the Low-Level APIs

A `SparkContext` is the entry point for low-level API functionality. You access it through the `SparkSession`, which is
the tool you use to perform computation across a Spark cluster.

## About RDDs

In short, an RDD represents an immutable, partitioned collection of records that can be operated on in parallel. Unlike
DataFrames though, where each record is a structured row containing fields with a known schema, in RDDs the records are
just Java, Scala, or Python objects of the programmer’s choosing.

RDDs give you complete control because every record in an RDD is just a Java or Python object. You can store anything
you want in these object, in any format you want. Every manipulation and interaction between values must be defined by
hand, meaning that you must “reinvent the wheel” for whatever task you are trying to carry out. Also, optimizations are
going to require much more manual work, because Spark does not understand the inner structure of your records as it does
with the Structured APIs. For instance, Spark’s Structured APIs automatically store data in an optimized, compressed
binary format, so to achieve the same space-efficiency and performance, you’d also need to implement this type of format
inside your objects and all the low-level operations to compute over it. Likewise, optimizations like reordering filters
and aggregations that occur automatically in Spark SQL need to be implemented by hand. For this reason and others, we
highly recommend **using the Spark Structured APIs when possible**

The RDD API is similar to the `Dataset` except that RDDs are not stored in, or manipulated with, the structured data
engine. However, it is trivial to convert back and forth between RDDs and Datasets, so you can use both APIs to take
advantage of each API’s strengths and weaknesses

### Types of RDDs

As a user, you will likely only be creating two types of RDDs

- The "generic" RDD type
- The key-value RDD that provides additional functions, such as aggregating by key

Each RDD is characterized by five main properties:

- A list of partitions
- A function for computing each split
- A list of dependencies on other RDDs
- Optionally, a `Partitioner` for key-value RDDs (partitioning with key)
- Optionally, a list of preferred locations on which to compute each split

RDDs follow the exact same Spark programming paradigms that we saw in earlier chapters. They provide transformations,
which evaluate lazily, and actions, which evaluate eagerly, to manipulate data in a distributed fashion

The is no concept of "rows" in RDDs, individual records are just raw Java/Scala/Python objects, and you manipulate those
manually instead of tapping into the repository of functions that you have in the Structured APIs

> Python < Scala/Java. Python can lose a substantial amount of performance when using RDDs.

## Creating RDDs

### Interoperating Between DataFrames, Datasets, and RDDs

One of the easiest ways to get RDDs is from an existing DataFrame or Dataset: just use the `rdd` method on any of these
data types

    // in Scala: converts a Dataset[Long] to RDD[Long]
    spark.range(500).rdd

To operate on this data, you will need to convert this `Row` object to the correct data type or extract values out of it

    // in Scala
    spark.range(10).toDF().rdd.map(rowObject => rowObject.getLong(0))

    # in Python
    spark.range(10).toDF("id").rdd.map(lambda row: row[0])

Create a DataFrame or Dataset from a RDD

    spark.range(10).rdd.toDF()

### From a Local Collection

To create an RDD from a collection, you will need to use the `parallelize` method on a `SparkContext` (within a
SparkSession). This turns a single node collection into a parallel collection. When creating this parallel collection,
you can also explicitly state the number of partitions into which you would like to distribute this array

    val myCollection = "Spark The Definitive Guide: Big Data Processing Made Simple"
      .split(" ")
    val words = spark.sparkContext.parallelize(myCollection, 2)
    words.setName("myWords")
    println(words.name)

### From Data Source

Read a text file line by line

    spark.sparkContext.textFile("/some/path/withTextFiles")

This creates an RDD for which each record in the RDD represents a line in that text file or files. Alternatively, you
can read in data for which each text file should become a single record. The use case here would be where each file is a
file that consists of a large JSON object or some document that you will operate on as an individual

    spark.sparkContext.wholeTextFiles("/some/path/withTextFiles")

## Manipulating RDDs

To demonstrate some data manipulation, let’s use the simple RDD (words) we created previously to define some more
details.

## Transformations

For the most part, many transformations mirror the functionality that you find in the Structured APIs. Just as you do
with DataFrames and Datasets, you specify _transformations_ on one RDD to create another.

### distinct

    words.distinct().count()

### filter

    // in Scala
    private def startsWithS(a: String): Boolean = {
        a.startsWith("S") // return True/False
    }

    // in Scala
    words.filter(word => startsWithS(word)).collect().foreach(println)

### map

Mapping is the same operation in Chapter 11. You specify a function that returns the value that you want, given the
correct input. You then apply that, record by record.

    // in Scala
    val words2 = words.map(word => (word, word(0), word.startsWith("S")))
    words2.collect().foreach(println)

    /*
        (Spark,S,true)
        (The,T,false)
        (Definitive,D,false)
        (Guide:,G,false)
        (Big,B,false)
        (Data,D,false)
        (Processing,P,false)
        (Made,M,false)
        (Simple,S,true)
    */

    # in Python
    words2 = words.map(lambda word: (word, word[0], word.startswith("S")))

Subsequently filter on this by selecting the relevant Boolean value in a new function

    // get only true row
    // in Scala
    words2.filter(record => record._3).take(5)

    # in Python
    words2.filter(lambda record: record[2]).take(5)

#### flatmap

Each current row should return multiple rows. `flatMap` requires that the output of the map function be an iterable that
can be expanded:

    words.flatMap(word => word.toSeq).collect().foreach(println)
    words.flatMap(lambda word: list(word)).take(5)

### sort

To sort an RDD you must use the `sortBy` method, and just like any other RDD operation, you do this by specifying a
function to extract a value from the objects in your RDDs and then sort based on that

    // in Scala
    words.sortBy(word => word.length() * -1)

### Random Splits

Randomly split an RDD into an Array of RDDs by using the `randomSplit` method, which accepts an Array of weights and a
random seed

    // random split
    val splits = words.randomSplit(Array(0.5, 0.5))
    splits.zipWithIndex.foreach { case (rdd, index) =>
      println(s"Contents of split $index:")
      rdd.collect().foreach(println)
    }

## Actions

### reduce

You can use the `reduce` method to specify a function to "reduce" an RDD of any kind of value to one value.

    // in scala
    spark.sparkContext.parallelize(1 to 20).reduce(_ + _)

    println(s"Longest word: ${words.reduce(wordLengthReducer)}")
    private def wordLengthReducer(leftWord:String, rightWord:String): String = {
        if (leftWord.length > rightWord.length)
          leftWord
        else
          rightWord
    }

This reducer is a good example because you can get one of two outputs ("definitive" or "processing) because the
`reducer` operation on the partitions is not deterministic.

### count

    words.count()

#### countApprox

This is an approximation of the `count` method we just looked at, but it must execute within a timeout

The confidence is the probability that the error bounds of the result will contain the true value. That is, if
countApprox were called repeatedly with confidence 0.9, we would expect 90% of the results to contain the true count.

    println(s"Count Approximation: ${words.countApprox(timeout = 400, confidence = 0.95)}")

#### countApproxDistinct

There are two implementation:

- First implementation: The argument passed into the function is the relative accuracy
- Second implementation: Two arguments are `p` and `sp` where `p` is precision and `sp` is sparse precision

            println(s"countApproxDistinct first implementation: ${words.countApproxDistinct(relativeSD = 0.05)}")
            println(s"countApproxDistinct second implementation: ${words.countApproxDistinct(p = 4, sp = 10)}")

#### countByValue

You should use this method only if the resulting map is expected to be small because the entire
thing is loaded into the driver’s memory

    words.countByValue()

#### countByValueApprox

    println(s"countByValueApprox: ${words.countByValueApprox(timeout = 400, confidence = 0.95)}")

### first

Return the first value in the dataset

    words.first()

### max and min

Return the maximum values and minimum values

    spark.sparkContext.parallelize(1 to 20).max()
    spark.sparkContext.parallelize(1 to 20).min()

### take

`take` and its derivative methods take a number of values from your RDD. This works by first scanning one partition and
then using the results from that partition to estimate the number of additional partitions needed to satisfy the limit.

    words.take(5)
    words.takeOrdered(5)
    words.top(5)
    val withReplacement = true
    val numberToTake = 6
    val randomSeed = 100L
    words.takeSample(withReplacement, numberToTake, randomSeed)

## Saving Files

Saving files means writing to plain-text files. With RDDs, you cannot actually "save" to a data source in the
conventional sense. You must iterate over the partitions in order to save the contents of each partition to some
external database. This is a low-level approach that reveals the underlying operation that is being performed in the
higher-level APIs.

### saveAsTextFile

    // saveAsTextFile
    words.saveAsTextFile("output/words_text_file")
    // with codec
    words.saveAsTextFile("output/words_compressed", classOf[BZip2Codec])

### SequenceFiles

A `sequenceFile` is a flat file consisting of binary key-value pairs. It is extensively used in MapReduce as
input/output formats

    words.saveAsObjectFile("path")

### Hadoop Files

There are a variety of different Hadoop file formats to which you can save. These allow you to specify classes, output
formats, Hadoop configurations, and compression schemes. (For information on these formats, read Hadoop: The Definitive
Guide [O’Reilly, 2015].)

## Caching

By default, cache and persist only handle data in memory

    words.cache()

We can specify a storage level as any of the storage levels in the singleton object:
org.apache.spark.storage.StorageLevel, which are combinations of memory only; disk only; and separately, off heap.

     // in Scala
    words.getStorageLevel
    # in Python
    words.getStorageLevel()

## Checkpointing

One feature not available in the DataFrame API is the concept of _checkpointing_. Checkpointing is the act of saving an
RDD to disk so that future references to this RDD point to those intermediate partitions on disk rather than recomputing
the RDD from its original source.

    spark.sparkContext.setCheckpointDir("/some/path/for/checkpointing")
    words.checkpoint()

Now, when we reference this RDD, it will derive from the checkpoint instead of the source data. This can be a helpful
optimization

## Pipe RDDs to System Commands

With pipe, you can return an RDD created by piping elements to a forked external process

    words.pipe("find /c /v \"\"").collect().foreach(println) // windows
    words.pipe("wc -l").collect() // linux

### mapPartitions

The previous command revealed that Spark operates on a per-partition basis when it comes to actually executing code.
`map` is a row-wise alias for `mapPartitions`, which makes it possible for you to map an individual partition

    // mapPartitions
    words.mapPartitions(_ => Iterator[Int](1)).sum() // create value "1" for every partition in our data

Other functions similar to `mapPartitions` include `mapPartitionsWithIndex`

    // in Scala
    def indexedFunc(partitionIndex:Int, withinPartIterator: Iterator[String]) = {
        withinPartIterator.toList.map(
        value => s"Partition: $partitionIndex => $value").iterator
    }
    words.mapPartitionsWithIndex(indexedFunc).collect()

    # in Python
    def indexedFunc(partitionIndex, withinPartIterator):
        return ["partition: {} => {}".format(partitionIndex,
        x) for x in withinPartIterator]
    words.mapPartitionsWithIndex(indexedFunc).collect()

### foreachPartition

`foreachPartition` simply iterates over all the partitions of the data, no return value. You can create our own text
file source if you want by specifying outputs to the temp directory with a random ID:

    words.foreachPartition { iter =>
        import java.io._
        import scala.util.Random
        val randomFileName = new Random().nextInt()
        val pw = new PrintWriter(new File(s"/tmp/random-file-${randomFileName}.txt"))
        while (iter.hasNext) {
            pw.write(iter.next())
        }
        pw.close()
    }

### glom

Take every partition in your dataset and converts them to arrays. This can be useful if you're going to collect the data
to the driver and want to have an array for each partition. Large partitions or large number of partitions will crash
the driver

    println(spark.sparkContext.parallelize(Seq("Hello", "World"), 2).glom().collect()
      .map(_.mkString("[", ", ", "]"))
      .mkString("[", ", ", "]"))

