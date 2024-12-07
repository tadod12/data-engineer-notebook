# Chapter 3. A Tour of Spark's Toolset

Spark is composed of these primitives—the lower-level APIs and the Structured APIs—and then a series of standard
libraries for additional functionality.

## Running Production Applications with spark-submit

`spark-submit` does one thing: it lets you send your application code to a cluster and launch it to execute there.
`spark-submit` offers several controls with which you can specify the resources your application needs as well as how it
should be run and its command-line arguments. You can write applications in any of Spark’s supported languages and then
submit them for execution

The simplest example is running an application on your local machine

    spark-submit --class org.apache.spark.examples.SparkPi --master local C:\spark\examples\jars\spark-examples_2.12-3.1.2.jar 10

![spark submit sparkpi.png](spark%20submit%20sparkpi.png)

![spark submit sparkpi (1).png](spark%20submit%20sparkpi%20%281%29.png)

We’ve told `spark-submit` that we want to run on our local machine, which class and which JAR we would like to run, and
some command-line arguments for that class.

Run a Python version of the application

    spark-submit --master local C:\spark\examples\src\main\python\pi.py 10

## Datasets: Type-Safe Structured APIs

Datasets is a type-safe version of Spark's structured API, for writing statically typed code in Java and Scala. The
Dataset API is not available in Python and R, because those language are dynamically typed.

Recall that DataFrames are a distributed collection of objects of type `Row` that can hold various types of tabular
data. The Dataset API gives users the ability to assign a Java/Scala class to the records within a DataFrame and
manipulate it as a collection of typed projects, similar to a Java `ArrayList` or Scala `Seq`.

> The APIs available on Datasets are `type-safe`, meaning that you cannot accidentally view the objects in a Dataset as
> being of another class than the class you put in initially. This makes Datasets especially attractive for writing
> large applications, with which multiple software engineers must interact through well-defined interfaces.

The Dataset class is parameterized with the type of object contained inside: `Dataset<T>` in Java and `Dataset[T]` in
Scala. The supported types are classes following the JavaBean pattern in Java and case classes in Scala

    // in Scala
    case class Flight(DEST_COUNTRY_NAME: String,
                      ORIGIN_COUNTRY_NAME: String,
                      count: BigInt)

    val flightsDF = spark
        .read
        .parquet("/data/flight-data/parquet/2010-summary.parquet/")

    val flights = flightsDF.as[Flight]

When you call `collect` or `take` on a Dataset, it will collect objects of the proper type in your Dataset, not
DataFrame `Rows`. This makes it easy to get type safety and securely perform manipulation in a distributed and a local
manner without code changes:

    // in Scala
    flights
        .filter(flight_row => flight_row.ORIGIN_COUNTRY_NAME != "Canada")
        .map(flight_row => flight_row)
        .take(5)

    flights
        .take(5)
        .filter(flight_row => flight_row.ORIGIN_COUNTRY_NAME != "Canada")
        .map(fr => Flight(fr.DEST_COUNTRY_NAME, fr.ORIGIN_COUNTRY_NAME, fr.count + 5))

## Structured Streaming

Structured Streaming is a high-level API for stream processing. With Structured Streaming, you can take the same
operations that you perform in batch mode using Spark’s structured APIs and run them in a streaming fashion.

The best thing about Structured Streaming is that it allows you to rapidly and quickly extract value out of streaming
systems with virtually no code changes.

    // in Scala 
    val staticDataFrame = spark.read.format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .load("/data/retail-data/by-day/*.csv")

    staticDataFrame.createOrReplaceTempView("retail_data")
    val staticSchema = staticDataFrame.schema

In this example we’ll take a look at the sale hours during which a given customer (identified by `CustomerId`) makes a
large purchase. For example, let’s add a total cost column and see on what days a customer spent the most.

    // in Scala
    import org.apache.spark.sql.functions.{window, column, desc, col}
    staticDataFrame
        .selectExpr(
            "CustomerId",
            "(UnitPrice * Quantity) as total_cost",
            "InvoiceDate")
        .groupBy(
            col("CustomerId"), window(col("InvoiceDate"), "1 day"))
        .sum("total_cost")
        .show(5)

> The window function will include all data from each day in the aggregation. It’s simply a window over the time–series
> column in our data
> Thay vì chỉ gộp theo customerID rồi tính tổng thì còn gộp thêm theo ngày

Good practice for local run:

    spark.conf.set("spark.sql.shuffle.partitions", "5")

The streaming code

    val streamingDataFrame = spark.readStream
        .schema(staticSchema)
        .option("maxFilesPerTrigger", 1)  // number of files read in at once to make demonstration more "streaming"
        .format("csv")
        .option("header", "true")
        .load("/data/retail-data/by-day/*.csv")

    streamingDataFrame.isStreaming // returns true

    // in Scala
    val purchaseByCustomerPerHour = streamingDataFrame
        .selectExpr(
            "CustomerId",
            "(UnitPrice * Quantity) as total_cost",
            "InvoiceDate")
        .groupBy(
            $"CustomerId", window($"InvoiceDate", "1 day"))
        .sum("total_cost")

This is still a lazy operation, so we will need to call a streaming action to start the execution of this data flow

Streaming actions are a bit different from our conventional static action because we’re going to be populating data
somewhere instead of just calling something like count. The action we will use will output to an in-memory table that we
will update after each _trigger_. In this case, each trigger is based on an individual file (the read option that we
set). Spark will mutate the data in the in-memory table such that we will always have the highest value as specified in
our previous aggregation

    // in Scala
    purchaseByCustomerPerHour.writeStream
        .format("memory")  // memory = store in-memory table
        .queryName("customer_purchases")  // the name of the in-memory table
        .outputMode("complete")  // complete = all the counts should be in the table
        .start()

Debug what our result will look like

    spark.sql("""
        SELECT
        FROM customer_purchases
        ORDER BY `sum(total_cost)` DESC
    """)
        .show(5)

Write the results out to the console

    purchaseByCustomerPerHour.writeStream
        .format("console")
        .queryName("customer_purchase_2")
        .outputMode("complete")
        .start()

## Machine Learning and Advanced Analytics

Spark performs large-scale machine learning with a built-in library of machine learning algorithms called MLlib. MLlib
allows for preprocessing, munging, training of models, and making predictions at scale on data. You can even use models
trained in MLlib to make predictions in Structured Streaming. Spark provides a sophisticated machine learning API for
performing a variety of machine learning tasks, from classification to regression, and clustering to deep learning.

### Example: K-means

Spark includes a number of preprocessing methods out of the box. To demonstrate these methods, we will begin with some
raw data, build up transformations before getting the data into the right format, at which point we can actually train
our model and then serve predictions:

    // from above
    staticDataFrame.printSchema()

    root
    |-- InvoiceNo: string (nullable = true)
    |-- StockCode: string (nullable = true)
    |-- Description: string (nullable = true)
    |-- Quantity: integer (nullable = true)
    |-- InvoiceDate: timestamp (nullable = true)
    |-- UnitPrice: double (nullable = true)
    |-- CustomerID: double (nullable = true)
    |-- Country: string (nullable = true)

Machine learning algorithms in MLlib require that data is represented as numerical values. Our current data is
represented by a variety of different types, including timestamps, integers, and strings. Therefore, we need to
transform this data into some numerical representation. In this instance, we’ll use several DataFrame transformations to
manipulate our date data:

    import org.apache.spark.sql.functions.date_format
    val preppedDataFrame = staticDataFrame
        .na.fill(0)  // na -> 0
        .withColumn("day_of_week", date_format($"InvoiceDate", "EEEE"))  // date to Monday, Friday, ...
        .coalesce(5)

Split the data into training and test sets

    val trainDataFrame = preppedDataFrame
        .where("InvoiceDate < '2011-07-11'")
    val testDataFrame = preppedDataFrame
        .where("InvoiceDate >= '2011-07-11'")

Spark’s MLlib also provides a number of transformations with which we can automate some of our general transformations.
One such transformer is a `StringIndexer`:

    import org.apache.spark.ml.feature.StringIndexer
    val indexer = new StringIndexer()
        .setInputCol("day_of_week")
        .setOutputCol("day_of_week_index")

This will turn our days of weeks into corresponding numerical values. For example, Spark might represent Saturday as 6,
and Monday as 1. However, with this numbering scheme, we are implicitly stating that Saturday is greater than Monday (by
pure numerical values). This is obviously incorrect. To fix this, we therefore need to use a OneHotEncoder to encode
each of these values as their own column. These Boolean flags state whether that day of week is the relevant day of the
week:

    import org.apache.spark.ml.feature.OneHotEncoder
    val encoder = new OneHotEncoder()
        .setInputCol("day_of_week_index")
        .setOutputCol("day_of_week_encoded"

Each of these will result in a set of columns that we will “assemble” into a vector. All machine learning algorithms in
Spark take as input a Vector type, which must be a set of numerical values:

    // in Scala
    import org.apache.spark.ml.feature.VectorAssembler

    val vectorAssembler = new VectorAssembler()
        .setInputCols(Array("UnitPrice", "Quantity", "day_of_week_encoded"))
        .setOutputCol("features")

Here, we have three key features: the price, the quantity, and the day of week. Next, we’ll set this up into a pipeline
so that any future data we need to transform can go through the exact same process:

    // in Scala
    import org.apache.spark.ml.Pipeline

    val transformationPipeline = new Pipeline()
        .setStages(Array(indexer, encoder, vectorAssembler))

Preparing for training is a two-step process:

    val fittedPipeline = transformationPipeline.fit(trainDataFrame) // fit tranformer to the dataset
    // StringIndexer needs to know how many unique values there are to be indexed

    val transformedTrainning = fittedPipeline.transform(trainDataFrame)

We’ll use caching, an optimization that we discuss in more detail in Part IV. This will put a copy of the intermediately
transformed dataset into memory, allowing us to repeatedly access it at much lower cost than running the entire pipeline
again.

    transformedTraining.cache()

Train the model

    // in Scala
    import org.apache.spark.ml.clustering.KMeans
    val kmeans = new KMeans()
        .setK(20)
        .setSeed(1L)

    // in Scala
    val kmModel = kmeans.fit(transformedTraining)

    kmModel.computeCost(transformedTraining)

    // in Scala
    val transformedTest = fittedPipeline.transform(testDataFrame)

    # in Python
    transformedTest = fittedPipeline.transform(testDataFrame)

    kmModel.computeCost(transformedTest)

## Lower-Level APIs

Spark includes a number of lower-level primitives to allow for arbitrary Java and Python object manipulation via
Resilient Distributed Datasets (RDDs). Virtually everything in Spark is built on top of RDDs. There are some things that
you might use RDDs for, especially when you’re reading or manipulating raw data, but for the most part you should stick
to the Structured APIs. RDDs are lower level than DataFrames because they reveal physical execution characteristics (
like partitions) to end users.

Parallelize raw data and create a DataFrame

    spark.sparkContext.parallelize(Seq(1, 2, 3)).toDF()

## SparkR

## Spark's Ecosystem and Packages

https://spark-packages.org/
