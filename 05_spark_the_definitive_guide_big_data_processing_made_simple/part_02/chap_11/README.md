# Chapter 11. Datasets

Datasets are the foundational type of the Structured APIs. We already worked with DataFrames, which are Datasets of type
Row, and are available across Spark’s different languages. Datasets are a strictly Java Virtual Machine (JVM) language
feature that work only with Scala and Java. Using Datasets, you can define the object that each row in your Dataset will
consist of. In Scala, this will be a case class object that essentially defines a schema that you can use, and in Java,
you will define a Java Bean

For example, given a class Person with two fields, name (string) and age (int), an encoder directs Spark to generate
code at runtime to serialize the Person object into a binary structure. When using DataFrames or the “standard”
Structured APIs, this binary structure will be a Row. When we want to create our own domain-specific objects, we specify
a case class in Scala or a JavaBean in Java. Spark will allow us to manipulate this object (in place of a Row) in a
distributed manner.

## When to Use Datasets

- When the operation(s) you would like to perform cannot be expressed using DataFrame manipulations
- WHen you want or need type-safety, and you're willing to accept the cost of performance to achieve it

There are some operations that cannot be expressed using the Structured APIs we have seen in the previous chapters.
Although these are not particularly common, you might have a large set of business logic that you’d like to encode in
one specific function instead of in SQL or DataFrames. This is an appropriate use for Datasets. Additionally, the
Dataset API is type-safe. Operations that are not valid for their types, say subtracting two string types, will fail at
compilation time not at runtime. If correctness and bulletproof code is your highest priority, at the cost of some
performance, this can be a great choice for you. This does not protect you from malformed data but can allow you to more
elegantly handle and organize it.

> Datasets là dạng đối tượng, còn DataFrame là Datasets nhưng chuyển về dạng Row (mỗi thuộc tính của Datasets sẽ là một
> cột trong Row)

Another potential time for which you might want to use Datasets is when you would like to reuse a variety of
transformations of entire rows between single-node workloads and Spark workloads. One advantage of using Datasets is
that if you define all of your data and transformations as accepting case classes it is trivial to reuse them for both
distributed and local workloads. Additionally, when you collect your DataFrames to local disk, they will be of the
correct class and type, sometimes making further manipulation easier.

Probably the most popular use case is to use DataFrames and Datasets in tandem, manually trading off between performance
and type safety when it is most relevant for your workload. This might be at the end of a large, DataFrame-based
extract, transform, and load (ETL) transformation when you’d like to collect data to the driver and manipulate it by
using single-node libraries, or it might be at the beginning of a transformation when you need to perform per row
parsing before performing filtering and further manipulation in Spark SQL.

> Ở cuối quá trình ETL lớn: Ban đầu sử dụng DataFrame cho các thao tác ETL vì hiệu suất cao. Sau đó chuyển sang Dataset
> khi cần thu thập và xử lý dữ liệu cục bộ.

> Ở đầu quá trình biến đổi: Bắt đầu với Dataset để tận dụng tính an toàn kiểu khi phân tích cú pháp từng hàng. Sau đó
> chuyển sang DataFrame để tận dụng hiệu suất cao của Spark SQL cho các thao tác lọc và biến đổi tiếp theo.

## Creating Datasets

### In Java: Encoders

    import org.apache.spark.sql.Encoders;

    public class Flight implements Serializable {
        String DEST_COUNTRY_NAME;
        String ORIGIN_COUNTRY_NAME;
        Long DEST_COUNTRY_NAME;
    }

    Dataset<Flight> flights = spark.read
        .parquet("...")
        .as(Encoders.bean(Flight.class));

### In Scala: Case Classes

Scala `case class`

- Immutable
- Decomposable through pattern matching
- Allows for comparison based on structure instead of reference
- Easy to use and manipulate

Define a `case class`

    case class Flight(
        DEST_COUNTRY_NAME: String,
        ORIGIN_COUNTRY_NAME: String,
        count: BigInt
    )

Create Dataset

    val flightsDF = spark.read
        .parquet("...")
    val flights = flightsDF.as[Flight]  // Dataset

## Actions

Actions like `collect`, `take`, and `count` can apply to whether we are using Datasets or DataFrames

    flights.show(2)

    flights.first.DEST_COUNTRY_NAME // United States

## Transformations

Transformations on Datasets are the same as those that we saw on DataFrames

### Filtering

Let’s look at a simple example by creating a simple function that accepts a Flight and returns a Boolean value that
describes whether the origin and destination are the same

    def originIsDestination(flight_row: Flight): Boolean = {
        return flight_row.ORIGIN_COUNTRY_NAME == flight_row.DEST_COUNTRY_NAME
    }

We can now pass this function into the filter method specifying that for each row it should verify that this function
returns true and in the process will filter our Dataset down accordingly

    flights.filter(flight_row => originIsDestination(flight_row)).first()
    // Flight = Flight(United States,United States,348113)

Collect to the driver

    flights.collect().filter(flight_row => originIsDestination(flight_row))
    // Array[Flight] = Array(Flight(United States,United States,348113))

### Mapping

The simplest example is manipulating our Dataset such that we extract one value from each row. This is effectively
performing a DataFrame like select on our Dataset

    val destinations = flights.map(f => f.DEST_COUNTRY_NAME)
    // Dataset of type String

We can collect this and get back an array of strings on the driver

    val localDestinations = destinations.take(5)

## Joins

Joins, as we mentioned earlier, apply just the same as they did for DataFrames. However, Datasets also provide a more
sophisticated method, the `joinWith` method. `joinWith` is roughly equal to a co-group (in RDD terminology) and you
basically end up with two nested Datasets inside of one.

Demonstrate

    // case class
    case class FlightMetadata(count: BigInt, randomData: BigInt)

    // fake metadata
    val flightsMeta = spark.range(500)
        .map(x => (x, scala.util.Random.nextLong))
        .withColumnRenamed("_1", "count")
        .withColumnRenamed("_2", "randomData")
        .as[FlightMetadata]

    val flights2 = flights
        .joinWith(flightsMeta, flights.col("count") === flightsMeta.col("count"))

A "regular" join would work quite well, although you'll notice in this case that we end up with a DataFrame (and thus
lose our JVM type information)

    val flights2 = flights.join(flightsMeta, Seq("count"))

There are no problems joining a DataFrame and a Dataset, end up DataFrame

    val flights2 = flights.join(flightsMeta.toDF(), Seq("count"))

## Grouping and Aggregations

`groupBy`, `rollup` and `cube` still apply, but return DataFrames instead of Datasets (lose type information)

    flights.groupBy("DEST_COUNTRY_NAME").count()

If you want to keep type information around there are other groupings and aggregations that you can perform. An
excellent example is the `groupByKey` method. This allows you to group by a specific key in the Dataset and get a typed
Dataset in return.

    flights.groupByKey(x => x.DEST_COUNTRY_NAME).count()  // argument is a function (not column name)

Although this provides flexibility, it’s a trade-off because now we are introducing JVM types as well as functions that
cannot be optimized by Spark


