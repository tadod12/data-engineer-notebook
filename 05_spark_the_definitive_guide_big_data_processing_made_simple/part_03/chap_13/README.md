# Chapter 13. Advanced RDDs

Dataset using in this chapter

    val myCollection = "Spark The Definitive Guide : Big Data Processing Made Simple"
        .split(" ")
    val words = spark.sparkContext.parallelize(myCollection, 2)

## Key-Value Basics (Key-Value RDDs)

There are many methods on RDDs that require you to put your data in a key-value format: `<some-operation>ByKey`.
Whenever you see `ByKey` in a method name, it means that you can perform this only for a `PairRDD` type. The easiest way
is to just map over your current RDD to a basic key-value structure

    words.map(word => (word.toLowerCase, 1)).collect().foreach(println)
    // (spark,1)(the,1)(definitive,1)(guide,1)(:,1)(big,1)(data,1)(processing,1)(made,1)(simple,1)

### keyBy

You can use the `keyBy` function to achieve the same result by specifying a function that creates the key from your
current value

    val keyword = words.keyBy(word => word.toLowerCase.toSeq(0).toString)
    keyword.foreach(print)
    // (s,Spark)(t,The)(d,Definitive)(g,Guide)(:,:)(b,Big)(d,Data)(p,Processing)(m,Made)(s,Simple)

### Mapping over Values

If we have a tuple, Spark will assume that the first element is the key, and the second is the value. When in this
format (key-value), you can explicitly choose to map-over the values (and ignore the individual keys)

    keyword.mapValues(word => word.toUpperCase).collect().foreach(print)
    // (s,SPARK)(t,THE)(d,DEFINITIVE)(g,GUIDE)(:,:)(b,BIG)(d,DATA)(p,PROCESSING)(m,MADE)(s,SIMPLE)

You can `flatMap` over the rows, to expand the number of rows that you have to make it so that each row represents a
character

    keyword.flatMapValues(word => word.toUpperCase).collect()
    // (s,S)(s,P)(s,A)(s,R)(s,K)(t,T)(t,H)(t,E)(d,D)(d,E)(d,F)(d,I)(d,N)(d,I)(d,T)(d,I)(...

### Extracting Keys and Values

    keyword.keys.collect().foreach(print)
    // stdg:bdpms
    keyword.values.collect().foreach(print)
    // SparkTheDefinitiveGuide:BigDataProcessingMadeSimple

### lookup

Look up the result for a particular key. Note that there is no enforcement mechanism with respect to there being only
one key for each input, so if we look up "s", we are going to get both values associated with that - "Spark" and "
Simple"

    keyword.lookup("s")

### sampleByKey

There are two ways to sample an RDD by a set of key

- Approximate way

        val distinctChars = words.flatMap(word => word.toLowerCase.toSeq)
          .distinct
          .collect()
        import scala.util.Random
        val sampleMap = distinctChars.map(c => (c, new Random().nextDouble())).toMap
        words.map(word => (word.toLowerCase.toSeq(0), word))
          .sampleByKey(withReplacement = true, fractions = sampleMap, seed = 6L)
          .collect().foreach(print)
        // (s,Spark)(d,Definitive)(g,Guide)(:,:)

- Exactly way: Lấy mẫu đúng theo tỉ lệ fraction generate ra

        words.map(word => (word.toLowerCase.toSeq(0), word))
          .sampleByKeyExact(withReplacement = true, fractions = sampleMap, seed = 6L)
          .collect().foreach(print)

## Aggregations

You can perform aggregations on plain RDDs or on PairRDDs, depending on the method that you are using

    // init
    val chars = words.flatMap(word => word.toLowerCase.toSeq)
    val KVCharacters = chars.map(letter => (letter, 1))
    val nums = spark.sparkContext.parallelize(1 to 30, numSlices = 5)

    def maxFunc(left: Int, right: Int): Int = math.max(left, right)
    def addFunc(left: Int, right: Int): Int = left + right

### countByKey

    KVCharacters.countByKey().foreach(print)
    // (e,7)(s,4)(n,2)(t,3)(a,4)(m,2)(i,7)(v,1)(b,1)(p,3)(r,2)(:,1)(k,1)(u,1)(f...
    KVCharacters.countByKeyApprox(timeout = 1000L, confidence = 0.95)

### Understanding Aggregation Implementations

There are several ways to create your key-value PairRDDs; however, the implementation is actually quite important for
job stability. Two fundamental choices:

- `groupBy`
- `reduce`

#### groupByKey

    KVCharacters.groupByKey().map(row => (row._1, row._2.reduce(addFunc)))
      .collect().foreach(print)

    // (d,4)(p,3)(t,3)(b,1)(h,1)(n,2)(f,1)(v,1)(:,1)(r,2)(l,1)(s,4)(e,7)(a,4)(k,1)(i,7)(u,1)(o,...

This is, for the majority of cases, the wrong way to approach the problem. The fundamental issue here is that each
executor must hold all values for a given key in memory before applying the function to them

There are use cases when `groupByKey` does make sense. If you have consistent value sizes for each key and know that
they will fit in the memory of a given executor, you’re going to be just fine.

There is a preferred approach for additive use cases: `reduceByKey`

#### reduceByKey

Perform a `reduceByKey` with a summation function in order to collect back the array. This implementation is much more
stable because the reduce happens within each partition and doesn't need to put everything in memory. Additionally,
there is no incurred shuffle during this operation; everything happens at each worker individually before performing a
final reduce

    KVCharacters.reduceByKey(addFunc).collect().foreach(print)
    (d,4)(p,3)(t,3)(b,1)(h,1)(n,2)(f,1)(v,1)(:,1)(r,2)(l,1)(s,4)(e,7)(a...

### Other Aggregation Methods

#### aggregate

This function requires a null and start value then requires you to specify two different functions. The first aggregates
within partitions, the second aggregates across partitions. The start value will be used at both aggregation levels

    println(nums.aggregate(0)(maxFunc, addFunc))

`aggregation` does have some performance implications because it performs the final aggregation on the driver. If the
results from the executors are too large, they can take down the driver with an `OutOfMemoryError`

There is another method, `treeAggregation` - pushes down some of the sub-aggregations (creating a tree from executor to
executor) before performing the final aggregation on the driver

#### aggregateByKey

This function does the same as `aggregate` but instead of doing it partition by partition, it does it by key

    KVCharacters.aggregateByKey(0)(addFunc, maxFunc).collect().foreach(print)

#### combineByKey

Instead of specifying an aggregation function, you can specify a combiner. This combiner operates on a given key and
merges the values according to some function. It then goes to merge the different outputs of the combiners to give us
our result.

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
      .collect()

#### foldByKey

`foldByKey` merges the values for each key using an associative function and a neutral "zero value", which can be added
to the result an arbitrary number of times, and must not change the result (addition uses 0, multiplication uses 1)

    KVCharacters.foldByKey(0)(addFunc).collect()

## CoGroups

CoGroups give you the ability to group together up to three key–value RDDs together in Scala and two in Python. This
joins the given values by key. This is effectively just a group-based join on an RDD. When doing this, you can also
specify a number of output partitions or a custom partitioning function to control exactly how this data is distributed
across the cluster

    val distinctChar = words.flatMap(word => word.toLowerCase.toSeq).distinct
    val charRDD = distinctChar.map(c => (c, new Random().nextDouble()))
    val charRDD2 = distinctChar.map(c => (c, new Random().nextDouble()))
    val charRDD3 = distinctChar.map(c => (c, new Random().nextDouble()))
    charRDD.cogroup(charRDD2, charRDD3).take(5).foreach(println)