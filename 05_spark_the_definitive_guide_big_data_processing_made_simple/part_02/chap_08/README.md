# Chapter 8. Joins

## Join Expressions

A _join_ brings together two sets of data, the _left_ and the _right_, by comparing the value of one or more _keys_ of
the left and right and evaluating the result of a _join expression_ that determines whether Spark should bring together
the left set of data with the right set of data

## Inner Joins

    // create join expression
    val joinExpression = person.col("graduate_program") === graduateProgram.col("id")

Inner joins are the default join, so we just need to specify our left DataFrame and join the right in the JOIN
expression

    // inner join
    person.join(graduateProgram, joinExpression).show()

We can also specify this explicitly by passing in a third parameter, the `joinType`

    val joinType = "inner"
    person.join(graduateProgram, joinExpression, joinType).show()

## Outer Joins

If there is no equivalent row in either the left or right DataFrame, Spark will insert `null`

    // outer join
    person.join(graduateProgram, joinExpression, joinType = "outer").show(truncate = false)

## Left Outer Joins

    // left outer join
    person.join(graduateProgram, joinExpression, joinType = "left_outer").show(truncate = false)

## Right Outer Joins

    // right outer join
    person.join(graduateProgram, joinExpression, joinType = "right_outer").show(truncate = false)

## Left Semi Joins

Left Semi Join là phép join giữa hai bảng, trong đó kết quả bao gồm tất cả các hàng từ bảng bên trái mà có ít nhất một
bản sao tương ứng trong bảng bên phải, nhưng không bao gồm bất kỳ cột nào từ bảng bên phải. Kết quả chỉ chứa các cột từ
bảng bên trái.

    // left semi join
    graduateProgram.join(person, joinExpression, joinType = "left_semi").show()

> If the value does exist, those rows will be kept in the result, even if there are duplicate keys in the left DataFrame

    val gradProgram2 = graduateProgram.union(Seq(
        (0, "Masters", "Duplicated Row", "Duplicated School")).toDF()) // duplicate col "id"
    gradProgram2.join(person, joinExpression, joinType = "left_semi").show()

    +---+-------+--------------------+-----------------+
    | id| degree|          department|           school|
    +---+-------+--------------------+-----------------+
    |  0|Masters|School of Informa...|      UC Berkeley|
    |  1|  Ph.D.|                EECS|      UC Berkeley|
    |  0|Masters|      Duplicated Row|Duplicated School|
    +---+-------+--------------------+-----------------+

## Left Anti Joins

Left anti joins are the opposite of left semi joins. Like left semi joins, they do not actually
include any values from the right DataFrame. They only compare values to see if the value exists
in the second DataFrame. However, rather than keeping the values that exist in the second
DataFrame, they keep only the values that do not have a corresponding key in the second
DataFrame. Think of anti joins as a NOT IN SQL-style filter

    // left anti join
    graduateProgram.join(person, joinExpression, joinType = "left_anti").show(truncate = false)

## Natural Joins

    // natural join
    spark.sql("SELECT * FROM graduateProgram NATURAL JOIN person").show(truncate = false) 
    // will choose "id" column for both

## Cross (Cartesian) Joins

    graduateProgram.join(person, joinExpression, joinType = "cross").show()

    person.crossJoin(graduateProgram).show()

## Challenges When Using Joins

### Joins on Complex Types

Any expression is a valid join expression, assuming that it returns a Boolean

    // join on complex types
    // Seq (array) in col "spark_status" - person dataFrames
    person.withColumnRenamed("id", "personId") // for not duplicated
      .join(sparkStatus, expr("array_contains(spark_status, id)")).show(truncate = false) // Seq spark_status contain id in sparkStatus

### Handling Duplicate Column Names

In a DataFrame, each column has a unique ID within Spark's SQL Engine, Catalyst (internal and not something that you can
directly reference). This makes it quite difficult to refer to a specific column when you have a DataFrame with
duplicate column names

Two situations
- The join expression doesn't remove one key from one of the input (keys have the same name)
- Two columns on which you are not performing the join have the same name

**Approach 1: Different join expression**

Change the join expression from a Boolean expression to a string or sequence

    person.join(gradProgramDupe, "graduate_program").select("graduate_program").show()
    // automatically remove one of the "graduate_program"

**Approach 2: Dropping the column after the join**

    person.join(gradProgramDupe, joinExpr).drop(person.col("graduate_program"))
        .select("graduate_program").show()

**Approach 3: Renaming a column before the join**

    val gradProgram3 = graduateProgram.withColumnRenamed("id", "grad_id")
    val joinExpr = person.col("graduate_program") === gradProgram3.col("grad_id")
    person.join(gradProgram3, joinExpr).show()\

## How Spark Performs Joins

